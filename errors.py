class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class TaskError(Error):
    """Exception raised for errors when a task failed.

    Attributes:
        message -- short description of the error
        details -- details, e.g. stacktrace
    """

    def __init__(self, message, details):
        self.message = message
        self.details = details