# Discount Calculator

A small system for calculating discounts on a shopping cart.

## What needs to be solved

We have a cart with items (price + quantity) and a set of discounts.

Supported discounts:

- percentage discount (per item)
- fixed discount (per item)
- volume discount (applied to the whole cart line if quantity threshold is met)

Rules:

- discounts can apply to all products or only selected product codes
- only one discount can be applied per cart line
- discounts are not combined
- we always pick the best one (lowest final price)

## Approach

The solution is based on a simple domain model with clear responsibilities.

Each discount:

- defines whether it is applicable (`is_applicable`)
- calculates the final price assuming it is applicable (`apply`)

The calculator:

- iterates over cart lines (`CartItem`)
- evaluates all applicable discounts
- selects the best result per line

The selection logic is isolated in a single place, so the calculator does not need to know anything about specific discount types.

## Key decisions

- **Separation of responsibility**
  - `is_applicable()` handles eligibility
  - `apply()` handles price calculation only
  - the calculator orchestrates which discounts are executed

- **Explicit business rule**
  - best discount per cart line is selected
  - implemented in `_select_best_discount(...)`
  - this can be extracted into a dedicated `DiscountPolicy` if rules become more complex

- **Money as a value object**
  - implemented as `@dataclass(frozen=True)`
  - immutable and compared by value (amount + currency)
  - prevents accidental mutation and simplifies testing

- **No floats in pricing**
  - all amounts are stored as integers (smallest currency unit)
  - percentage discount uses deterministic floor division

- **Currency safety**
  - operations on `Money` require matching currencies
  - mismatches raise explicit exceptions

- **No unnecessary work**
  - non-applicable discounts are skipped before calculation

## Project structure

```
src/discount_calculator/
    calculator.py
    currency.py
    models/
    discounts/
    exceptions/

tests/
    unit/
    functional/
```

## Running tests

From project root:

```
pytest tests/ -v
```

## Notes

- The goal was to keep the solution simple but structured and extensible
- The current model supports a single-discount-per-line strategy
- If discount rules grow in complexity (e.g. stacking, priorities), the selection logic can be extracted into a separate policy layer