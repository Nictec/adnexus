
class ContainerInitializationWarning(Warning):
    """
    Warning is a senseless container config is detected
    """
    def __init__(self, msg: str):
        super().__init__(msg)
