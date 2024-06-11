class AdnexusError(BaseException):
    """
    XDI base exception
    """
    pass


class ImproperlyConfigured(AdnexusError):
    """
    Exception for when the framework config has errors
    """

    def __init__(self, msg) -> None:
        super().__init__("Framework config error: " + msg)


class InjectionError(AdnexusError):
    """
    Exception for errors occurring in the injection process
    """
    pass


class WiringError(AdnexusError):
    """
    Exception for errors occurring in the wiring process
    """
    pass


class CircularDependencyError(AdnexusError):
    """
    Exception for detected circular dependencies
    """
    pass
