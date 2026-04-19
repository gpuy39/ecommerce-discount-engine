from __future__ import annotations

from typing import Optional

from discount_calculator.currency import Currency
from discount_calculator.discounts.base import Discount
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


class DiscountCalculator:
    """
    Calculates cart total using the best discount per cart line.
    """

    def __init__(self, discounts: Optional[list[Discount]] = None) -> None:
        self.discounts = discounts or []

    def calculate_total(self, items: list[CartItem]) -> Money:
        """
        Calculates total cart value after applying the best discount
        for each cart line.
        """
        if not items:
            raise ValidationError("Cart items cannot be empty.")

        currency = self._get_cart_currency(items)
        total = Money(amount=0, currency=currency)

        for item in items:
            best_line_total = self._select_best_discount(item)
            total = total.add(best_line_total)

        return total

    def _select_best_discount(self, item: CartItem) -> Money:
        """
        Selects the lowest possible total for a single cart line.

        Business rule:
        - only one discount may be applied per cart line,
        - discounts are evaluated independently,
        - discounts are not combined,
        - the final line total is the lowest value among
          the original line total and all applicable discount results.

        If pricing rules become more complex in the future,
        this logic could be extracted into a dedicated DiscountPolicy.
        """
        best_total = item.base_total

        for discount in self.discounts:
            if not discount.is_applicable(item):
                continue

            discounted_total = discount.apply(item)

            if discounted_total.amount < best_total.amount:
                best_total = discounted_total

        return best_total

    @staticmethod
    def _get_cart_currency(items: list[CartItem]) -> Currency:
        """
        Ensures all cart items use the same currency and returns it.
        """
        first_currency = items[0].price.currency

        if any(item.price.currency != first_currency for item in items[1:]):
            raise ValidationError("All cart items must use the same currency.")

        return first_currency
