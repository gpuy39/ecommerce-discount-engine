import pytest

from discount_calculator.calculator import DiscountCalculator
from discount_calculator.currency import Currency
from discount_calculator.discounts.fixed import FixedDiscount
from discount_calculator.discounts.percentage import PercentageDiscount
from discount_calculator.discounts.volume import VolumeDiscount
from discount_calculator.exceptions.currency_errors import CurrencyMismatchError
from discount_calculator.exceptions.validation_errors import ValidationError
from discount_calculator.models.cart_item import CartItem
from discount_calculator.models.money import Money


def test_calculate_total_returns_sum_without_discounts() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=2),
        CartItem(code="B", price=Money(amount=500, currency=Currency.EUR), quantity=3),
    ]
    calculator = DiscountCalculator()

    result = calculator.calculate_total(items)

    assert result == Money(amount=3500, currency=Currency.EUR)


def test_calculate_total_applies_best_discount_per_cart_line() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=10),
    ]
    discounts = [
        PercentageDiscount(percentage=10),
        FixedDiscount(discount_amount=Money(amount=50, currency=Currency.EUR)),
        VolumeDiscount(
            min_quantity=10,
            discount_amount=Money(amount=500, currency=Currency.EUR),
        ),
    ]
    calculator = DiscountCalculator(discounts=discounts)

    result = calculator.calculate_total(items)

    assert result == Money(amount=9000, currency=Currency.EUR)


def test_calculate_total_does_not_stack_multiple_discounts_for_one_line() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=2),
    ]
    discounts = [
        PercentageDiscount(percentage=10),
        FixedDiscount(discount_amount=Money(amount=100, currency=Currency.EUR)),
    ]
    calculator = DiscountCalculator(discounts=discounts)

    result = calculator.calculate_total(items)

    assert result == Money(amount=1800, currency=Currency.EUR)


def test_calculate_total_applies_different_discounts_to_different_lines() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=10),
        CartItem(code="B", price=Money(amount=500, currency=Currency.EUR), quantity=2),
    ]
    discounts = [
        VolumeDiscount(
            min_quantity=10,
            discount_amount=Money(amount=500, currency=Currency.EUR),
            applicable_codes=["A"],
        ),
        FixedDiscount(
            discount_amount=Money(amount=50, currency=Currency.EUR),
            applicable_codes=["B"],
        ),
    ]
    calculator = DiscountCalculator(discounts=discounts)

    result = calculator.calculate_total(items)

    assert result == Money(amount=10400, currency=Currency.EUR)


def test_calculate_total_raises_error_for_empty_cart() -> None:
    calculator = DiscountCalculator()

    with pytest.raises(ValidationError):
        calculator.calculate_total([])


def test_calculate_total_raises_error_for_mixed_cart_currencies() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=1),
        CartItem(code="B", price=Money(amount=500, currency=Currency.USD), quantity=1),
    ]
    calculator = DiscountCalculator()

    with pytest.raises(ValidationError):
        calculator.calculate_total(items)


def test_calculate_total_selects_best_discount_between_global_and_scoped() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=2),
    ]
    discounts = [
        PercentageDiscount(percentage=10),
        FixedDiscount(
            discount_amount=Money(amount=150, currency=Currency.EUR),
            applicable_codes=["A"],
        ),
    ]
    calculator = DiscountCalculator(discounts=discounts)

    result = calculator.calculate_total(items)

    assert result == Money(amount=1700, currency=Currency.EUR)


def test_calculate_total_raises_error_for_discount_currency_mismatch() -> None:
    items = [
        CartItem(code="A", price=Money(amount=1000, currency=Currency.EUR), quantity=2),
    ]
    discounts = [
        FixedDiscount(
            discount_amount=Money(amount=100, currency=Currency.USD),
        ),
    ]
    calculator = DiscountCalculator(discounts=discounts)

    with pytest.raises(CurrencyMismatchError):
        calculator.calculate_total(items)
