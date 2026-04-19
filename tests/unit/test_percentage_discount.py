import pytest

from discount_calculator.currency import Currency
from discount_calculator.discounts.percentage import PercentageDiscount
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


def test_apply_returns_discounted_line_total_for_matching_item() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=3,
    )
    discount = PercentageDiscount(percentage=10)

    result = discount.apply(item)

    assert discount.is_applicable(item) is True
    assert result == Money(amount=2700, currency=Currency.EUR)


def test_is_applicable_returns_false_when_discount_does_not_apply_to_item_code() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=2,
    )
    discount = PercentageDiscount(
        percentage=10,
        applicable_codes=["B"],
    )

    assert discount.is_applicable(item) is False


def test_apply_uses_floor_rounding_for_percentage_discount() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=999, currency=Currency.EUR),
        quantity=1,
    )
    discount = PercentageDiscount(percentage=10)

    result = discount.apply(item)

    assert result == Money(amount=899, currency=Currency.EUR)


def test_apply_returns_zero_for_hundred_percent_discount() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=4,
    )
    discount = PercentageDiscount(percentage=100)

    result = discount.apply(item)

    assert result == Money(amount=0, currency=Currency.EUR)


@pytest.mark.parametrize("percentage", [-1, 101])
def test_init_raises_error_for_invalid_percentage_values(percentage: int) -> None:
    with pytest.raises(ValidationError):
        PercentageDiscount(percentage=percentage)


def test_init_raises_error_when_applicable_codes_is_empty() -> None:
    with pytest.raises(ValidationError):
        PercentageDiscount(
            percentage=10,
            applicable_codes=[],
        )
