from __future__ import annotations

from typing import Optional

from discount_calculator.discounts.base import Discount
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


class VolumeDiscount(Discount):
    """
    Fixed discount applied to the whole cart line
    when the minimum quantity threshold is met.
    """

    def __init__(
        self,
        min_quantity: int,
        discount_amount: Money,
        applicable_codes: Optional[list[str]] = None,
    ) -> None:
        super().__init__(applicable_codes=applicable_codes)
        self.min_quantity = self._validate_min_quantity(min_quantity)
        self.discount_amount = self._validate_discount_amount(discount_amount)

    def is_applicable(self, item: CartItem) -> bool:
        """
        Returns whether this discount can be applied to the given cart item.

        In addition to product code matching, volume discount requires
        the cart line quantity to meet the minimum threshold.
        """
        return super().is_applicable(item) and item.quantity >= self.min_quantity

    def apply(self, item: CartItem) -> Money:
        """
        Returns cart line total after applying volume discount.

        This method assumes the discount is applicable to the item.
        """
        self.discount_amount.ensure_same_currency(item.price)

        discounted_amount = max(
            0,
            item.base_total.amount - self.discount_amount.amount,
        )

        return Money(
            amount=discounted_amount,
            currency=item.price.currency,
        )

    @staticmethod
    def _validate_min_quantity(min_quantity: int) -> int:
        """
        Validates minimum quantity required for the discount.
        """
        if min_quantity <= 0:
            raise ValidationError("Minimum quantity must be greater than zero.")
        return min_quantity

    @staticmethod
    def _validate_discount_amount(discount_amount: Money) -> Money:
        """
        Validates volume discount amount.
        """
        if discount_amount.amount < 0:
            raise ValidationError("Volume discount amount cannot be negative.")
        return discount_amount
