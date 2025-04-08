import functools
import inspect
from typing import Any, Callable

from starlette._utils import is_async_callable
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.services.exceptions import Forbidden, Unauthorized
from app.utils.auth import verify_jwt


def has_required_scopes(user_scopes: list, required_scopes: list) -> bool:
    """
    Check if all required scopes are present in the user's scopes.
    :param user_scopes: The scopes of the user.
    :param required_scopes: The required scopes.
    :return: True if all required scopes are present, False otherwise.
    """
    user_scopes_set = set(user_scopes)
    for required_scope in required_scopes:
        if required_scope in user_scopes_set:
            continue
        scope_category = required_scope.split(".")[0] + ".*"
        if scope_category in user_scopes_set:
            continue
        return False
    return True


def requires(
    scopes: str | list[str],
) -> Callable:
    required_scopes = [scopes] if isinstance(scopes, str) else list(scopes)

    def decorator(
        func: Callable,
    ) -> Callable:
        # verify existence of and get signature of request/websocket parameter
        sig = inspect.signature(func)
        for idx, parameter in enumerate(sig.parameters.values()):
            if parameter.name == "request" or parameter.name == "websocket":
                type_ = parameter.name
                break
        else:
            raise Exception(
                f'No "request" or "websocket" argument on function "{func}"'
            )

        def _set_auth(request) -> None:
            assert isinstance(request, Request)

            access_token = ""
            # Check for access token in the Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_token = auth_header.removeprefix("Bearer ").strip()

            # If no access token in the header, check for it in cookies
            if not access_token:
                access_token = request.cookies.get("access_token")

            # If no access token in the header or cookies, raise Unauthorized error
            if not access_token:
                print("Access token missing or invalid")
                raise Unauthorized("Access token missing or invalid")

            claims = verify_jwt(access_token)
            user_scopes = claims.get("scopes")
            if not has_required_scopes(user_scopes, required_scopes):
                print("Insufficient scopes")
                raise Forbidden("Insufficient scopes")

            request.state.sub = claims.get("sub")
            request.state.role = claims.get("role")
            request.state.scopes = claims.get("scopes")

        if is_async_callable(func):
            # Handle async request/response functions.
            @functools.wraps(func)
            async def async_wrapper(*args: list, **kwargs: dict) -> Any:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                _set_auth(request)
                return await func(*args, **kwargs)

            return async_wrapper
        else:
            # Handle sync request/response functions.
            @functools.wraps(func)
            def sync_wrapper(*args: list, **kwargs: dict) -> Any:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                _set_auth(request)
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator


def web_requires(
    scopes: str | list[str],
    optional: bool = False,
) -> Callable:
    required_scopes = [scopes] if isinstance(scopes, str) else list(scopes)

    def decorator(
        func: Callable,
    ) -> Callable:
        # verify existence of and get signature of request/websocket parameter
        sig = inspect.signature(func)
        for idx, parameter in enumerate(sig.parameters.values()):
            if parameter.name == "request" or parameter.name == "websocket":
                type_ = parameter.name
                break
        else:
            raise Exception(
                f'No "request" or "websocket" argument on function "{func}"'
            )

        def _set_auth(request: Request):
            assert isinstance(request, Request)
            access_token = request.cookies.get("access_token", " ")
            if not access_token:
                raise Unauthorized("Access token missing")

            try:
                claims = verify_jwt(access_token)
            except Exception as e:
                raise Unauthorized("Invalid access token") from e

            user_scopes = claims.get("scopes")
            if not has_required_scopes(user_scopes, required_scopes):
                raise Forbidden("Insufficient scopes")

            request.state.sub = claims.get("sub")
            request.state.role = claims.get("role")
            request.state.scopes = claims.get("scopes")

        if is_async_callable(func):
            # Handle async request/response functions.
            @functools.wraps(func)
            async def async_wrapper(*args: list, **kwargs: dict) -> Any:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                try:
                    _set_auth(request)
                    return await func(*args, **kwargs)
                except Unauthorized:
                    if optional:
                        return await func(*args, **kwargs)
                    print("Unauthorized")
                    return RedirectResponse("/login")
                except Forbidden:
                    if optional:
                        return await func(*args, **kwargs)
                    print("Forbidden")
                    return RedirectResponse("/403")
                except Exception as e:
                    if optional:
                        return await func(*args, **kwargs)
                    print(e)
                    return RedirectResponse("/login")

            return async_wrapper
        else:
            # Handle sync request/response functions.
            @functools.wraps(func)
            def sync_wrapper(*args: list, **kwargs: dict) -> Any:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                try:
                    _set_auth(request)
                    return func(*args, **kwargs)
                except Unauthorized:
                    if optional:
                        return func(*args, **kwargs)
                    return RedirectResponse("/login")
                except Forbidden:
                    if optional:
                        return func(*args, **kwargs)
                    return RedirectResponse("/403")
                except Exception:
                    if optional:
                        return func(*args, **kwargs)
                    return RedirectResponse("/login")

            return sync_wrapper

    return decorator
