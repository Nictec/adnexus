from typing import TypeVar, Generic

I = TypeVar("I")


class Provide(Generic[I]): # pragma: no cover
    """
    Marker for marking an attribute to be injected by XDI
    """
    pass
