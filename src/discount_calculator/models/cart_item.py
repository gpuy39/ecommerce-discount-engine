from dataclasses import dataclass

from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.money import Money


@dataclass
class CartItem:
    """
    Represents a single product in the cart.
    """

    code: str
    price: Money
    quantity: int

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValidationError("Cart item code cannot be empty.")

        if self.quantity < 0:
            raise ValidationError("Cart item quantity cannot be negative.")

    @property
    def base_total(self) -> Money:
        """
        Total price for this item (before any discounts).
        """
        return self.price.multiply(self.quantity)
