from __future__ import annotations

from typing import Optional

from discount_calculator.discounts.base import Discount
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


class PercentageDiscount(Discount):
    """
    Percentage discount applied per item.
    """

    def __init__(
        self,
        percentage: int,
        applicable_codes: Optional[list[str]] = None,
    ) -> None:
        super().__init__(applicable_codes=applicable_codes)
        self.percentage = self._validate_percentage(percentage)

    def apply(self, item: CartItem) -> Money:
        """
        Returns cart line total after applying percentage discount.

        This method assumes the discount is applicable to the item.
        """
        # Since Money.amount is modeled as an integer, percentage discounts require a rounding decision.
        # Integer floor division was used to keep the implementation simple and consistent.
        discounted_unit_amount = item.price.amount * (100 - self.percentage) // 100

        discounted_unit_price = Money(
            amount=discounted_unit_amount,
            currency=item.price.currency,
        )

        return discounted_unit_price.multiply(item.quantity)

    @staticmethod
    def _validate_percentage(percentage: int) -> int:
        """
        Validates percentage discount value.
        """
        if percentage < 0 or percentage > 100:
            raise ValidationError("Percentage discount must be between 0 and 100.")
        return percentage
