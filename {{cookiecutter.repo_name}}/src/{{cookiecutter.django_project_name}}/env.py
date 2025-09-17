import builtins
import os
import pathlib

UNSET = object()


def get(key) -> builtins.str | None:
    return os.environ.get(key)


def str(key, default=UNSET) -> builtins.str:
    if default is UNSET:
        if bool("__strict_env__", True):
            return os.environ[key]
        else:
            return os.environ.get(key)
    else:
        return os.environ.get(key, default)


def list(key, default=None, separator=",") -> builtins.list:
    value = str(key, default)
    if value is None:
        return []
    else:
        return value.split(separator)


def int(key, default) -> builtins.int:
    return builtins.int(str(key, default))


def float(key, default) -> builtins.float:
    return builtins.float(str(key, default))


def bool(key, default) -> builtins.bool:
    if key in os.environ:
        return os.environ.get(key).lower() in ("yes", "true", "y", "1")
    else:
        return default


def path(key, default=UNSET) -> pathlib.Path:
    value = str(key, default)
    value = pathlib.Path(value)
    assert value.exists(), f"{value!r} does not exist"
    return value
