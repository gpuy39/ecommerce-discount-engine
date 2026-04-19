import pytest

from discount_calculator.currency import Currency
from discount_calculator.discounts.fixed import FixedDiscount
from discount_calculator.exceptions.currency_errors import CurrencyMismatchError
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


def test_apply_returns_discounted_line_total_for_matching_item() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=3,
    )
    discount = FixedDiscount(
        discount_amount=Money(amount=100, currency=Currency.EUR),
    )

    result = discount.apply(item)

    assert discount.is_applicable(item) is True
    assert result == Money(amount=2700, currency=Currency.EUR)


def test_is_applicable_returns_false_when_discount_does_not_apply_to_item_code() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=2,
    )
    discount = FixedDiscount(
        discount_amount=Money(amount=100, currency=Currency.EUR),
        applicable_codes=["B"],
    )

    assert discount.is_applicable(item) is False


def test_apply_does_not_reduce_price_below_zero() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=100, currency=Currency.EUR),
        quantity=3,
    )
    discount = FixedDiscount(
        discount_amount=Money(amount=200, currency=Currency.EUR),
    )

    result = discount.apply(item)

    assert result == Money(amount=0, currency=Currency.EUR)


def test_apply_raises_error_when_discount_currency_does_not_match_item_currency() -> None:
    item = CartItem(
        code="A",
        price=Money(amount=1000, currency=Currency.EUR),
        quantity=1,
    )
    discount = FixedDiscount(
        discount_amount=Money(amount=100, currency=Currency.USD),
    )

    with pytest.raises(CurrencyMismatchError):
        discount.apply(item)


def test_init_raises_error_when_applicable_codes_is_empty() -> None:
    with pytest.raises(ValidationError):
        FixedDiscount(
            discount_amount=Money(amount=100, currency=Currency.EUR),
            applicable_codes=[],
        )


def test_init_normalizes_applicable_codes() -> None:
    discount = FixedDiscount(
        discount_amount=Money(amount=100, currency=Currency.EUR),
        applicable_codes=[" A ", "B"],
    )

    assert discount.applicable_codes == {"A", "B"}


def test_init_accepts_zero_discount_amount() -> None:
    discount = FixedDiscount(
        discount_amount=Money(amount=0, currency=Currency.EUR),
    )

    assert discount.discount_amount == Money(amount=0, currency=Currency.EUR)
