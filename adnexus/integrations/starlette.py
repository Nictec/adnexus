import functools
import inspect
import typing

from starlette.middleware import Middleware
from starlette.routing import Route, get_name, request_response, compile_path

from adnexus.wrappers import InjectedCallable


# this is necessary because the standard starlette route would handle our injected objects as an Endpoint (which does not work)
class InjectedRoute(Route):
    """
    Overwrites the default Route of Starlette to be compatible with starlette.
    Warning: Usage of the normal Route is not supported because of internal datastructures (InjectedCallable)
    """
    def __init__(
        self,
        path: str,
        endpoint: typing.Callable[..., typing.Any],
        *,
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
        middleware: typing.Sequence[Middleware] | None = None,
    ) -> None:
        assert path.startswith("/"), "Routed paths must start with '/'"
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.include_in_schema = include_in_schema

        endpoint_handler = endpoint
        while isinstance(endpoint_handler, functools.partial):
            endpoint_handler = endpoint_handler.func
        if inspect.isfunction(endpoint_handler) or inspect.ismethod(endpoint_handler) or isinstance(endpoint_handler, InjectedCallable):
            # Endpoint is function method or InjectedCallable. Treat it as `func(request) -> response`.
            self.app = request_response(endpoint)
            if methods is None:
                methods = ["GET"]
        else:
            # Endpoint is a class. Treat it as ASGI.
            self.app = endpoint

        if middleware is not None:
            for cls, args, kwargs in reversed(middleware):
                self.app = cls(app=self.app, *args, **kwargs)

        if methods is None:
            self.methods = None
        else:
            self.methods = {method.upper() for method in methods}
            if "GET" in self.methods:
                self.methods.add("HEAD")

        self.path_regex, self.path_format, self.param_convertors = compile_path(path)

