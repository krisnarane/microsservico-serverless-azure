"""
CPF (Cadastro de Pessoas Físicas) validation utility for Brazilian tax IDs.

CPF validation rules:
1. Must have exactly 11 digits
2. Cannot be all the same digit (like 11111111111)
3. Must pass the check digit algorithm
"""

import re


def clean_cpf(cpf):
    """
    Remove all non-digit characters from CPF string.
    
    Args:
        cpf (str): CPF string that may contain formatting characters
        
    Returns:
        str: CPF with only digits
    """
    if not cpf:
        return ""
    return re.sub(r'[^0-9]', '', str(cpf))


def is_valid_format(cpf):
    """
    Check if CPF has valid format (11 digits, not all same digit).
    
    Args:
        cpf (str): Cleaned CPF string (digits only)
        
    Returns:
        bool: True if format is valid, False otherwise
    """
    # Must have exactly 11 digits
    if len(cpf) != 11:
        return False
    
    # Cannot be all the same digit
    if cpf == cpf[0] * 11:
        return False
    
    return True


def calculate_check_digit(cpf_digits, position):
    """
    Calculate check digit for CPF validation.
    
    Args:
        cpf_digits (str): First 9 or 10 digits of CPF
        position (int): Position of check digit (10 for first, 11 for second)
        
    Returns:
        int: Calculated check digit
    """
    weight = position
    total = 0
    
    for digit in cpf_digits:
        total += int(digit) * weight
        weight -= 1
    
    remainder = total % 11
    
    if remainder < 2:
        return 0
    else:
        return 11 - remainder


def validate_check_digits(cpf):
    """
    Validate both check digits of CPF using the official algorithm.
    
    Args:
        cpf (str): Complete 11-digit CPF string
        
    Returns:
        bool: True if both check digits are valid, False otherwise
    """
    # Extract the digits
    first_nine = cpf[:9]
    first_check_digit = int(cpf[9])
    second_check_digit = int(cpf[10])
    
    # Calculate and validate first check digit
    calculated_first = calculate_check_digit(first_nine, 10)
    if calculated_first != first_check_digit:
        return False
    
    # Calculate and validate second check digit
    first_ten = cpf[:10]
    calculated_second = calculate_check_digit(first_ten, 11)
    if calculated_second != second_check_digit:
        return False
    
    return True


def validate_cpf(cpf):
    """
    Complete CPF validation function.
    
    Performs all validation steps:
    1. Clean the input (remove formatting)
    2. Check format (11 digits, not all same)
    3. Validate check digits using official algorithm
    
    Args:
        cpf (str): CPF string (may contain formatting)
        
    Returns:
        bool: True if CPF is valid, False otherwise
        
    Examples:
        >>> validate_cpf("123.456.789-09")
        True
        >>> validate_cpf("11111111111")
        False
        >>> validate_cpf("123.456.789-00")
        False
    """
    # Clean the CPF (remove formatting)
    cleaned_cpf = clean_cpf(cpf)
    
    # Check format
    if not is_valid_format(cleaned_cpf):
        return False
    
    # Validate check digits
    return validate_check_digits(cleaned_cpf)


# Known valid CPFs for testing
VALID_TEST_CPFS = [
    "12345678909",
    "11144477735",
    "52998224725"
]

# Known invalid CPFs for testing
INVALID_TEST_CPFS = [
    "11111111111",  # All same digits
    "12345678900",  # Invalid check digits
    "123456789",    # Too short
    "123456789012", # Too long
    "abc.def.ghi-jk" # Non-numeric
]