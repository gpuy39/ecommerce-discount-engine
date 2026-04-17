from discount_calculator.exceptions.base import DiscountCalculatorError


class ValidationError(DiscountCalculatorError):
    """Raised when provided data is invalid."""
