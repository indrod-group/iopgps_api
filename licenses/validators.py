from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_license_validity(expiry_date: str):
    """
    Validates the validity of a license based on its expiry date.

    Args:
        - expiry_date (str): The expiry date of the license in 'YYYY-MM-DD' format.

    Raises:
        - ValidationError: If the license has expired.
    """
    if datetime.fromisoformat(expiry_date) <= date.today():
        raise ValidationError(
            f"{expiry_date} is not a valid date",
            params={'value': expiry_date}
        )

def validate_issue_date(issue_date: str):
    """
    Validates the issue date of a license.

    Args:
        - issue_date (str): The issue date of the license in 'YYYY-MM-DD' format.

    Raises:
        - ValidationError: If the issue date is in the future.
    """
    if datetime.fromisoformat(issue_date) >= date.today():
        raise ValidationError(
            f"{issue_date} is not a valid date. The issue date cannot be in the future.",
            params={'value': issue_date}
        )
