from __future__ import annotations
from dataclasses import dataclass

from discount_calculator.currency import Currency
from discount_calculator.exceptions.currency_errors import CurrencyMismatchError
from discount_calculator.exceptions.validation_errors import ValidationError


@dataclass(frozen=True)
class Money:
    """
    Simple value object representing money (amount in smallest unit + currency).
    """

    amount: int
    currency: Currency

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValidationError("Money amount cannot be negative.")

    def add(self, other: Money) -> Money:
        """
        Adds two money values (same currency required).
        """
        self.ensure_same_currency(other)
        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )

    def multiply(self, multiplier: int) -> Money:
        """
        Multiplies amount by a given integer (e.g. quantity).
        """
        if multiplier < 0:
            raise ValidationError("Multiplier cannot be negative.")
        return Money(
            amount=self.amount * multiplier,
            currency=self.currency,
        )

    def ensure_same_currency(self, other: Money) -> None:
        """
        Ensures both values use the same currency.
        """
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Currency mismatch: {self.currency} != {other.currency}."
            )
