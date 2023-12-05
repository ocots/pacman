class InternalException(Exception):
    """
        This exception is the generic class
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)