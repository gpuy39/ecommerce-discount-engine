# Discount Calculator

The goal is to build a small system for discount calculation

## What needs to be solved

We have a cart with items (price + quantity) and a set of discounts.

Supported discounts:
- percentage discount (per item)
- fixed discount (per item)
- volume discount (applied to the whole cart line if quantity threshold is met)

Some rules:
- discounts can apply to all products or only selected product codes
- only one discount can be applied per cart line
- we always pick the best one (lowest final price)

## Approach (idea)

I’ll probably go with something close to a strategy-like approach for discounts, so each discount knows:
- if it applies to a given item
- how to calculate the final price

The calculator itself should only:
- iterate over cart items
- evaluate available discounts
- pick the best result

## Project structure (init)

    src/discount_calculator/
        calculator.py
        currency.py
        models/
        discounts/
        exceptions/
    tests/
        unit/ 
        functional/
    README.md
    pyproject.toml
    .gitignore

## Planned next steps:

- basic domain models (Money, CartItem)
- discount implementations (base abstract)
- calculator logic
- tests (unit + func)