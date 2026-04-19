from __future__ import annotations

from typing import Optional

from discount_calculator.discounts.base import Discount
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


class FixedDiscount(Discount):
    """
    Fixed discount applied per item.
    """

    def __init__(
        self,
        discount_amount: Money,
        applicable_codes: Optional[list[str]] = None,
    ) -> None:
        super().__init__(applicable_codes=applicable_codes)
        self.discount_amount = self._validate_discount_amount(discount_amount)

    def apply(self, item: CartItem) -> Money:
        """
        Returns cart line total after applying fixed discount.

        This method assumes the discount is applicable to the item.
        """
        self.discount_amount.ensure_same_currency(item.price)

        discounted_unit_amount = max(0, item.price.amount - self.discount_amount.amount)

        discounted_unit_price = Money(
            amount=discounted_unit_amount,
            currency=item.price.currency,
        )

        return discounted_unit_price.multiply(item.quantity)

    @staticmethod
    def _validate_discount_amount(discount_amount: Money) -> Money:
        """
        Validates fixed discount amount.
        """
        if discount_amount.amount < 0:
            raise ValidationError("Fixed discount amount cannot be negative.")
        return discount_amount
