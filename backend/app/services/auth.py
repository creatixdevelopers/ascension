import functools
import inspect
from typing import Any, Callable

from starlette._utils import is_async_callable
from starlette.requests import Request
from starlette.websockets import WebSocket

from app.services.exceptions import Unauthorized, Forbidden
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

        # Handle websocket functions. (Always async)
        if type_ == "websocket":

            @functools.wraps(func)
            async def websocket_wrapper(*args: list, **kwargs: dict) -> None:
                websocket = kwargs.get(
                    "websocket", args[idx] if idx < len(args) else None
                )
                assert isinstance(websocket, WebSocket)

                # todo: Implement websocket authorization
                # if not has_required_scope(websocket, scopes_list):
                #     await websocket.close()
                # else:
                #     await func(*args, **kwargs)
                await func(*args, **kwargs)

            return websocket_wrapper

        elif is_async_callable(func):
            # Handle async request/response functions.
            @functools.wraps(func)
            async def async_wrapper(*args: list, **kwargs: dict) -> Any:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                assert isinstance(request, Request)

                auth_header = request.headers.get("Authorization", " ")
                if not auth_header.startswith("Bearer "):
                    raise Unauthorized("Invalid Authorization header format")
                access_token = auth_header.split(" ", 1)[1]
                if not access_token:
                    raise Unauthorized("Access token missing")

                claims = verify_jwt(access_token)
                user_scopes = claims.get("scopes")
                if not has_required_scopes(user_scopes, required_scopes):
                    raise Forbidden("Insufficient scopes")

                request.state.sub = claims.get("sub")
                request.state.role = claims.get("role")
                request.state.scopes = claims.get("scopes")
                return await func(*args, **kwargs)

            return async_wrapper

        else:
            # Handle sync request/response functions.
            @functools.wraps(func)
            def sync_wrapper(*args: list, **kwargs: dict) -> Any:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                assert isinstance(request, Request)

                auth_header = request.headers.get("Authorization", " ")
                if not auth_header.startswith("Bearer "):
                    raise Unauthorized("Invalid Authorization header format")
                access_token = auth_header.split(" ", 1)[1]
                if not access_token:
                    raise Unauthorized("Access token missing")

                claims = verify_jwt(access_token)
                user_scopes = claims.get("scopes")
                if not has_required_scopes(user_scopes, required_scopes):
                    raise Forbidden("Insufficient scopes")

                request.state.sub = claims.get("sub")
                request.state.role = claims.get("role")
                request.state.scopes = claims.get("scopes")
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator
