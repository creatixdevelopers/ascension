from datetime import datetime, timezone
import nanoid


def current_datetime() -> datetime:
    """
    Returns the current datetime in UTC.

    :return: The current datetime in UTC.
    """
    return datetime.now(tz=timezone.utc)


def generate_uid(n: int = 17) -> str:
    """
    Generates a unique ID.

    :param n: The length of the ID.
    :return: A unique ID.
    """
    return nanoid.generate(size=n)
