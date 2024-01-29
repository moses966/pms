import re
from django.core.exceptions import ValidationError

def validate_nin(nin):
    # Check if NIN is 14 characters long
    if len(nin) != 14:
        raise ValidationError("NIN must be 14 characters long.")

    # Check if the first character is a letter of the alphabet
    if not nin[0].isalpha():
        raise ValidationError("The first character of NIN must be a letter of the alphabet.")

    # Check if the second character is either M or F
    if nin[1] not in ['M', 'F']:
        raise ValidationError("The second character of NIN must be either M or F.")

    # Check if characters 3 to 7 are numbers
    if not re.match(r'^\d{5}$', nin[2:7]):
        raise ValidationError("Characters 3 to 7 of NIN must be numbers.")

    # No further checks for the rest of the characters

    return "Valid NIN."

def validate_contact(value):
    """
    Validator for ensuring that a contact starts with 0,
    has a total of ten characters, and all characters are digits (0-9).
    """
    if not value.startswith('0'):
        raise ValidationError('Contact must start with 0.')
    
    if len(value) != 10:
        raise ValidationError('Contact must have a total of ten characters.')
    
    if not value.isdigit():
        raise ValidationError('Contact must contain only digits (0-9).')