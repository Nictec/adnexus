from typing import TypeVar, Generic

INJ = TypeVar("INJ")


class Provide(Generic[INJ]):
    """
    Marker for marking an attribute to be injected by XDI
    """
    pass
