from enum import Enum


class Currency(str, Enum):
    """Supported currency codes."""

    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    PLN = "PLN"
