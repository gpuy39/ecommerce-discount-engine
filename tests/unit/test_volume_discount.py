import pytest

from discount_calculator.currency import Currency
from discount_calculator.discounts.volume import VolumeDiscount
from discount_calculator.exceptions.currency_errors import CurrencyMismatchError
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


def test_apply_returns_discounted_line_total_when_quantity_meets_threshold() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=10,
    )
    discount = VolumeDiscount(
        min_quantity=10,
        discount_amount=Money(amount=500, currency=Currency.EUR),
    )

    result = discount.apply(item)

    assert result == Money(amount=9500, currency=Currency.EUR)


def test_is_applicable_returns_false_when_quantity_is_below_threshold() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=9,
    )
    discount = VolumeDiscount(
        min_quantity=10,
        discount_amount=Money(amount=500, currency=Currency.EUR),
    )

    assert discount.is_applicable(item) is False


def test_is_applicable_returns_false_when_discount_does_not_apply_to_item_code() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=10,
    )
    discount = VolumeDiscount(
        min_quantity=10,
        discount_amount=Money(amount=500, currency=Currency.EUR),
        applicable_codes=["B"],
    )

    assert discount.is_applicable(item) is False


def test_is_applicable_returns_true_when_code_matches_and_quantity_meets_threshold() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=10,
    )
    discount = VolumeDiscount(
        min_quantity=10,
        discount_amount=Money(amount=500, currency=Currency.EUR),
        applicable_codes=["A"],
    )

    assert discount.is_applicable(item) is True


def test_apply_does_not_reduce_line_total_below_zero() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=100, currency=Currency.EUR),
        quantity=10,
    )
    discount = VolumeDiscount(
        min_quantity=10,
        discount_amount=Money(amount=2000, currency=Currency.EUR),
    )

    result = discount.apply(item)

    assert result == Money(amount=0, currency=Currency.EUR)


def test_apply_raises_error_when_discount_currency_does_not_match_item_currency() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=10,
    )
    discount = VolumeDiscount(
        min_quantity=10,
        discount_amount=Money(amount=500, currency=Currency.USD),
    )

    with pytest.raises(CurrencyMismatchError):
        discount.apply(item)


@pytest.mark.parametrize("min_quantity", [0, -1])
def test_init_raises_error_for_invalid_min_quantity(min_quantity: int) -> None:
    with pytest.raises(ValidationError):
        VolumeDiscount(
            min_quantity=min_quantity,
            discount_amount=Money(amount=500, currency=Currency.EUR),
        )


def test_init_raises_error_when_applicable_codes_is_empty() -> None:
    with pytest.raises(ValidationError):
        VolumeDiscount(
            min_quantity=10,
            discount_amount=Money(amount=500, currency=Currency.EUR),
            applicable_codes=[],
        )
