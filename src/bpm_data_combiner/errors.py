class DoubleSubmissionError(AssertionError):
    """Data submitted twice"""

class UnknownDeviceNameError(AssertionError):
    """Device name unknown
    """


__all__ = ["DoubleSubmissionError", "UnknownDeviceNameError"]
