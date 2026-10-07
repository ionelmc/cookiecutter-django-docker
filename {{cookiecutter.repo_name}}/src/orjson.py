"""
Small shim to support parse_float and the sort while behaving like orjson (returning bytes).
"""

import json

loads = json.loads
JSONDecodeError = json.JSONDecodeError


def dumps(obj, **kwargs):
    return json.dumps(obj, **kwargs).encode()
