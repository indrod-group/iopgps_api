from datetime import datetime
import re

from .exceptions import (
    InvalidBatteryCode,
    InvalidDotCode,
    InvalidManufactureDate,
    InvalidVehiclePlate
)

def is_valid_vehicle_plate(plate: str) -> bool:
    """
    This function only verifies if the plate format is valid.
    It does not verify if the plate is registered in the SRI or ANT.
    """
    vehicle_pattern = r'^[A-Z]{3}\-\d{3,4}$'
    moto_pattern = r'^[A-Z]{2}\-\d{3}[A-Z]?$'
    return bool(re.match(vehicle_pattern, plate)) or bool(re.match(moto_pattern, plate))

def is_valid_dot_code(dot_code: str) -> bool:
    """
    Verifies if a DOT code has the correct format.

    A DOT code (Department of Transportation) is found
    on the side of car tires and provides
    information about the tire, including its manufacture date.
    A valid DOT code has the format `DOT-XXXX-XXXX-XXXX`,
    where `X` can be an uppercase letter or a digit.

    Args:
        - dot_code (str): The DOT code to verify.

    Returns:
        - bool: True if the DOT code has the correct format, False otherwise.
    """
    dot_pattern = r'^DOT-[A-Z0-9]{4}-[A-Z0-9]{4}-\d{4}$'
    return bool(re.match(dot_pattern, dot_code))

def is_valid_manufacture_year(year: int):
    """
    Validates if the manufacture year of a vehicle is valid.

    Args:
        - year (int): The manufacture year to validate.

    Returns:
        - bool: True if the manufacture year is valid, False otherwise.
    """
    current_year = datetime.now().year
    return 1900 < year <= current_year

def is_valid_battery_code(battery_code: str):
    """Verifies if a battery code is valid.

    Args:
        - battery_code (str): The battery code to verify.

    Returns:
        - bool: True if the battery code is valid, False otherwise.
    """
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    return bool(re.match(pattern, battery_code))

def validate_vehicle_plate(plate: str):
    """Validates if a vehicle plate is valid.

    This function takes a vehicle plate as an argument and verifies if it is valid
    using the function is_valid_vehicle_plate from the utils.py file.
    If the plate is not valid, a ValidationError exception is raised.

    Args:
        - plate (str): The vehicle plate to validate.

    Raises:
        - InvalidVehiclePlate: If the vehicle plate is not valid.
    """
    if not is_valid_vehicle_plate(plate):
        raise InvalidVehiclePlate(
            f"{plate} is not a valid vehicle plate.",
            params={'value': plate}
        )

def validate_manufacture_year(year: int) -> None:
    """Validate if the manufacture year is allowed.
    Args:
        - year (int): This is the manufacture year.

    Raises:
        - InvalidManufactureDate: if the manufacture year is invalid.
    """
    if not is_valid_manufacture_year(year):
        raise InvalidManufactureDate(
            f"The manufacture year {year} is outside the defined limits.",
            params={'value': year}
        )

def validate_battery_code(battery_code: str) -> None:
    """
    Validates if a battery code is valid.

    Args:
        - battery_code (str): The battery code to validate.

    Raises:
        - InvalidBatteryCode: If the battery code is not valid.

    """
    if not is_valid_battery_code(battery_code):
        raise InvalidBatteryCode(
            f"{battery_code} is not a valid battery code.",
            params={'value': battery_code}
        )

def validate_dot_code(dot_code: str):
    """Validates if a DOT code is valid.

    This function takes a DOT code as an argument and verifies if it is valid
    using the function is_valid_dot_code from the utils.py file.
    If the DOT code is not valid, a ValidationError exception is raised.

    Args:
        - dot_code (str): The DOT code to validate.

    Raises:
        - InvalidDotCode: If the DOT code is not valid.
    """
    if not is_valid_dot_code(dot_code):
        raise InvalidDotCode(
            f"{dot_code} is not a valid DOT code.",
            params={'value': dot_code}
        )
