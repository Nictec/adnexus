from typing import TypeVar, Generic

I = TypeVar("I")


class Provide(Generic[I]):
    """
    Marker for marking an attribute to be injected by XDI
    """
    pass
