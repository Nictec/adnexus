class XDIError(BaseException):
    """
    XDI base exception
    """
    pass


class ImproperlyConfigured(XDIError):
    """
    Exception for when the framework config has errors
    """
    def __init__(self, msg) -> None:
        super().__init__("Framework config error: " + msg)


class InjectionError(XDIError):
    """
    Exception for errors occurring in the injection process
    """
    pass


class WiringError(XDIError):
    """
    Exception for errors occurring in the wiring process
    """
    pass
