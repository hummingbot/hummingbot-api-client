"""Every call this client makes must exist on hummingbot-api, with the keys it sends.

The routers are hand-written wrappers around hummingbot-api's HTTP surface. Nothing
here is generated and nothing is checked at import time, so a route the API renames or
drops stays in this client as a method that looks fine and 404s the first time someone
calls it. That is how the whole rate-oracle module survived after the API stopped
serving `/rate-oracle/*`, and how `pull_image` kept sending `{name, tag}` after the
route started requiring `{image_name}` — a 422 on every call, invisible because the one
caller in the wild mocked the client in its tests.

Three checks against the vendored spec:

- Every path+method a router calls is served by the API.
- Every literal query key it sends is declared by that route.
- Every literal body key it sends is declared by that route's request model.

Calls whose path or keys are computed rather than literal are counted, not checked —
the last test fails if that count ever swamps the checked ones, which would mean these
checks had quietly stopped covering the client.

Refresh the spec when adopting an API change:

    curl -s -u <user>:<pass> http://localhost:8000/openapi.json > hummingbot-api-openapi.json
"""
import ast
import json
import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = _REPO_ROOT / "hummingbot-api-openapi.json"
ROUTERS_PATH = _REPO_ROOT / "hummingbot_api_client" / "routers"

# BaseRouter's request helpers, mapped to the HTTP method each one sends.
HELPERS = {"_get": "get", "_post": "post", "_put": "put", "_delete": "delete", "_patch": "patch"}

# Stands in for an interpolated path segment. Any value matches a spec `{param}`, so the
# placeholder only has to be something no literal segment would ever be.
PLACEHOLDER = "\x00"


def _spec() -> dict:
    return json.loads(SPEC_PATH.read_text())


def _routes(spec: dict) -> list:
    """[(method, raw_path, compiled_matcher, operation)] for every operation in the spec."""
    out = []
    for raw, operations in spec["paths"].items():
        pattern = re.compile("^" + re.sub(r"\{[^}]+\}", "[^/]+", raw) + "$")
        for method, operation in operations.items():
            if method in HELPERS.values():
                out.append((method, raw, pattern, operation))
    return out


class _Calls(ast.NodeVisitor):
    """Collects `self._get("/path", params={...}, json={...})` from a router module."""

    def __init__(self):
        self.found = []

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in HELPERS:
            keywords = {kw.arg: kw.value for kw in node.keywords}
            self.found.append({
                "line": node.lineno,
                "method": HELPERS[func.attr],
                "path": self._path(node.args[0] if node.args else None),
                "params": self._keys(keywords.get("params")),
                "json": self._keys(keywords.get("json")),
            })
        self.generic_visit(node)

    @staticmethod
    def _path(node):
        """The literal path, with interpolated segments replaced by PLACEHOLDER."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr):
            return "".join(
                part.value if isinstance(part, ast.Constant) else PLACEHOLDER
                for part in node.values
            )
        return None

    @staticmethod
    def _keys(node):
        """Literal string keys of a dict or list-of-pairs; None if not readable statically."""
        if isinstance(node, ast.Dict):
            if any(key is None for key in node.keys):  # {**spread}
                return None
            if not all(isinstance(key, ast.Constant) for key in node.keys):
                return None
            return {key.value for key in node.keys}
        if isinstance(node, ast.List):  # [("limit", ...), ("network", ...)]
            keys = set()
            for element in node.elts:
                if not isinstance(element, ast.Tuple) or not element.elts:
                    return None
                first = element.elts[0]
                if not isinstance(first, ast.Constant):
                    return None
                keys.add(first.value)
            return keys
        return None


def _client_calls() -> list:
    calls = []
    for module in sorted(ROUTERS_PATH.glob("*.py")):
        visitor = _Calls()
        visitor.visit(ast.parse(module.read_text()))
        for call in visitor.found:
            call["module"] = module.name
            calls.append(call)
    return calls


CALLS = _client_calls()
SPEC = _spec()
ROUTES = _routes(SPEC)


def _match(method: str, path: str):
    """The spec operation serving this call, or (None, None).

    BaseRouter builds `f"{base_url}/{path.lstrip('/')}"`, so a missing leading slash is
    not drift. A missing *trailing* slash is: FastAPI answers it with a 307 the client
    happens to follow, which works but turns every such call into two round trips.
    """
    path = "/" + path.lstrip("/")
    for spec_method, raw, pattern, operation in ROUTES:
        if spec_method == method and pattern.match(path):
            return raw, operation
    return None, None


def _query_names(operation: dict) -> set:
    return {p["name"] for p in operation.get("parameters", []) if p.get("in") == "query"}


def _body_names(operation: dict, spec: dict):
    """Declared body properties, or None when the route takes a free-form object."""
    body = operation.get("requestBody")
    if not body:
        return None
    schema = body["content"]["application/json"]["schema"]
    if "$ref" in schema:
        schema = spec["components"]["schemas"][schema["$ref"].split("/")[-1]]
    return set(schema["properties"]) if "properties" in schema else None


def _readable() -> list:
    return [call for call in CALLS if call["path"] is not None]


def _ids(calls):
    return [f"{c['module']}:{c['line']}:{c['method']}" for c in calls]


@pytest.mark.parametrize("call", _readable(), ids=_ids(_readable()))
def test_the_route_the_call_addresses_is_served(call):
    raw, operation = _match(call["method"], call["path"])
    assert operation is not None, (
        f"{call['module']}:{call['line']} calls {call['method'].upper()} {call['path']}, "
        f"which hummingbot-api does not serve. Either the route was renamed and this "
        f"wrapper should follow it, or the route is gone and the wrapper should be too — "
        f"a method that can only 404 is worse than no method. Spec: {SPEC_PATH.name}."
    )


@pytest.mark.parametrize("call", _readable(), ids=_ids(_readable()))
def test_the_keys_the_call_sends_are_declared(call):
    raw, operation = _match(call["method"], call["path"])
    if operation is None:
        pytest.skip("route is missing; the test above reports it")

    if call["params"] is not None:
        undeclared = sorted(call["params"] - _query_names(operation))
        assert not undeclared, (
            f"{call['module']}:{call['line']} sends query keys {raw} does not declare: "
            f"{undeclared}. FastAPI ignores an undeclared query parameter, so the filter "
            "or flag is dropped in silence and the call returns the unfiltered result."
        )

    if call["json"] is not None:
        declared = _body_names(operation, SPEC)
        if declared is not None:
            undeclared = sorted(call["json"] - declared)
            assert not undeclared, (
                f"{call['module']}:{call['line']} sends body keys {raw} does not declare: "
                f"{undeclared}. Pydantic rejects the request outright when a required "
                "field is missing, so this is a 422 on every call."
            )


def test_the_checks_above_cover_most_of_the_client():
    """A regex or visitor gone stale would leave these tests passing over nothing."""
    assert len(SPEC["paths"]) > 100, "The vendored spec looks truncated"
    assert len(CALLS) > 100, (
        f"Only {len(CALLS)} calls found across {ROUTERS_PATH.name}/ — has BaseRouter "
        "stopped using the _get/_post helpers?"
    )
    computed = [c for c in CALLS if c["path"] is None]
    assert len(computed) < len(CALLS) // 10, (
        f"{len(computed)} of {len(CALLS)} calls build their path dynamically, so these "
        "checks no longer cover most of the client: "
        + ", ".join(f"{c['module']}:{c['line']}" for c in computed)
    )
