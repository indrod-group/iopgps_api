from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

class InvalidDotCode(ValidationError):
    """Raised when a DOT code is invalid.

    This exception is raised when the DOT code being validated does not meet the expected format.
    It is a subclass of DRF's `ValidationError` and can be used to
    return a 400 Bad Request response with a descriptive error message
    when using DRF to build an API.

    Args:
        detail (str): A custom error message (optional).
        params (dict): Additional context for the error message (optional).
    """
    def __init__(self, detail=None, params=None):
        if detail is None:
            detail = "The DOT code does not meet the expected format."
        super().__init__(_(detail), params)

class InvalidVehiclePlate(ValidationError):
    """Raised when a vehicle license plate is invalid.

    This exception is raised when the vehicle license plate
    being validated does not meet the expected format.
    It is a subclass of DRF's `ValidationError` and can be used to
    return a 400 Bad Request response with a descriptive error message
    when using DRF to build an API.

    Args:
        - detail (str): A custom error message (optional).
        - params (dict): Additional context for the error message (optional).
    """
    def __init__(self, detail=None, params=None):
        if detail is None:
            detail = "The vehicle plate does not meet the expected format."
        super().__init__(_(detail), params)

class InvalidBatteryCode(ValidationError):
    """Raised when a battery code is invalid.

    Args:
        - detail (str): A custom error message (optional).
        - params (dict): Additional context for the error message (optional).
    """

    def __init__(self, detail=None, params=None):
        if detail is None:
            detail = "The battery code year does not meet the expected format."
        super().__init__(_(detail), params)

class InvalidManufactureDate(ValidationError):
    """ Initializes an instance of the exception.
        Args:
            - detail (str): Optional detail that describes the manufacture date error.
            - params (dict): Optional additional parameters for the error.
    """
    def __init__(self, detail=None, params=None):
        if detail is None:
            detail = "The manufacture date is outside the defined limits."
        super().__init__(_(detail), params)

class ExpiredLicense(ValidationError):
    """
    Represents an exception that occurs when the license has expired.

    Args:
        - detail (str): Optional detail that describes the license expiration date error.
        - params (dict): Optional additional parameters for the error.
    """

    def __init__(self, detail=None, params=None):
        if detail is None:
            detail = "The license has expired."
        super().__init__(_(detail), params)
