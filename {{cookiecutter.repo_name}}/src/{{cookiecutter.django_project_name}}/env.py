import builtins
import os
import pathlib

UNSET = object()


def get(key) -> builtins.str | None:
    return os.environ.get(key)


def str(key, default=UNSET) -> builtins.str | None:
    if default is UNSET:
        if bool("__strict_env__", True):
            return os.environ[key]
        else:
            return os.environ.get(key)
    else:
        return os.environ.get(key, default)


def list(key, default=UNSET, separator=",") -> builtins.list:
    value = str(key, default)
    if value is None:
        return []
    elif isinstance(value, builtins.str):
        return value.split(separator)
    else:
        return value


def int(key, default=UNSET) -> builtins.int | None:
    value = str(key, default)
    if value is None:
        return
    else:
        return builtins.int(value)


def float(key, default=UNSET) -> builtins.float | None:
    value = str(key, default)
    if value is None:
        return
    else:
        return builtins.float(value)


def bool(key, default=UNSET) -> builtins.bool | None:
    value = str(key, default)
    if isinstance(value, builtins.str):
        return value.lower() in ("yes", "true", "y", "1")
    else:
        return value


def path(key, default=UNSET) -> pathlib.Path | None:
    value = str(key, default)
    if value is None:
        return
    else:
        value = pathlib.Path(value)
        assert value.exists(), f"{value!r} does not exist"
        return value
