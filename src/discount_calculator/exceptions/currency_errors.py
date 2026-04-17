from discount_calculator.exceptions.base import DiscountCalculatorError


class CurrencyMismatchError(DiscountCalculatorError):
    """Raised when monetary values use different currencies."""
