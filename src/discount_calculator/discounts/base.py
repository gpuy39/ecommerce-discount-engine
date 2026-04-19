from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


class Discount(ABC):
    """
    Base contract for all discounts.
    """

    def __init__(self, applicable_codes: Optional[list[str]] = None) -> None:
        self.applicable_codes = self._validate_applicable_codes(applicable_codes)

    def is_applicable(self, item: CartItem) -> bool:
        """
        Checks whether this discount can be applied to the given cart item.

        By default, a discount is applicable when the item code matches
        the configured applicable codes. Subclasses may extend this rule
        with additional business constraints.
        """
        if self.applicable_codes is None:
            return True
        return item.code in self.applicable_codes

    @abstractmethod
    def apply(self, item: CartItem) -> Money:
        """
        Returns the final cart line price after applying this discount.

        This method assumes the discount is applicable to the given item.
        Applicability should be checked separately via is_applicable().
        """
        raise NotImplementedError

    @staticmethod
    def _validate_applicable_codes(
            applicable_codes: Optional[list[str]],
    ) -> Optional[set[str]]:
        """
        Validates and normalizes product codes this discount applies to.
        """
        if applicable_codes is None:
            return None

        if not applicable_codes:
            raise ValidationError("Applicable codes cannot be empty.")

        # detect duplicates early (before normalization)
        if len(set(applicable_codes)) != len(applicable_codes):
            raise ValidationError("Duplicate product codes are not allowed.")

        cleaned_codes = {
            code.strip() for code in applicable_codes if code and code.strip()
        }

        if len(cleaned_codes) != len(applicable_codes):
            raise ValidationError("Each applicable code must be a non-empty string.")

        return cleaned_codes
