from __future__ import annotations

import collections
import math
import typing
from fractions import Fraction

from .Technologies import Recipe, all_product_sources, recipes


MAX_CHECKS_PER_PRODUCT = 100
MAX_CRAFTSANITY_LOCATIONS = 3000
# This world excludes Space Age. The base-game silo requires 100 completed Rocket Part crafts per launch.
ROCKET_PARTS_PER_LAUNCH = 100
SCIENCE_PACKS = (
    "automation-science-pack",
    "logistic-science-pack",
    "military-science-pack",
    "chemical-science-pack",
    "production-science-pack",
    "utility-science-pack",
)

# Avoid recycling recipes and select the same practical source consistently.
PRODUCT_RECIPE_OVERRIDES: dict[str, str | None] = {
    "barrel": "barrel",
    "crude-oil": "mining-crude-oil",
    "heavy-oil": "advanced-oil-processing",
    "light-oil": "advanced-oil-processing",
    "petroleum-gas": "basic-oil-processing",
    "solid-fuel": "solid-fuel-from-light-oil",
    "lubricant": "lubricant",
    "sulfuric-acid": "sulfuric-acid",
    "uranium-235": "uranium-processing",
    "uranium-238": "uranium-processing",
    "water": None,
}

UNCOUNTABLE_PRODUCTS = {
    "coal", "concrete", "copper-ore", "crude-oil", "heavy-oil", "iron-ore", "light-oil", "lubricant",
    "petroleum-gas", "raw-fish", "refined-concrete", "stone", "sulfur", "sulfuric-acid", "uranium-235",
    "uranium-238", "uranium-ore", "water", "wood",
}


def get_product_recipe(product: str, custom_recipes: typing.Mapping[str, Recipe] | None = None) -> Recipe | None:
    if custom_recipes and product in custom_recipes:
        return custom_recipes[product]

    override = PRODUCT_RECIPE_OVERRIDES.get(product, ...)
    if override is None:
        return None
    if override is not ...:
        return recipes[override]
    if product in recipes and product in recipes[product].products:
        return recipes[product]
    mining_recipe = recipes.get(f"mining-{product}")
    if mining_recipe:
        return mining_recipe

    sources = sorted(
        (recipe for recipe in all_product_sources.get(product, ())
         if not recipe.name.startswith("empty-")
         and recipe.name != "kovarex-enrichment-process"
         and not recipe.name.endswith("-reprocessing")),
        key=lambda recipe: recipe.name,
    )
    if not sources:
        return None
    return sources[0]


def get_craftsanity_products() -> tuple[str, ...]:
    """All products that may receive one of the statically reserved checks."""
    initial_products: list[str] = []
    for recipe_name, recipe in recipes.items():
        if not recipe_name.endswith(("-barrel", "-science-pack")):
            for product in recipe.products:
                if product not in initial_products:
                    initial_products.append(product)
    for science_pack in SCIENCE_PACKS:
        if science_pack not in initial_products:
            initial_products.append(science_pack)

    products = set(initial_products)
    pending = list(initial_products)
    while pending:
        recipe = get_product_recipe(pending.pop())
        if not recipe:
            continue
        for ingredient in recipe.ingredients:
            if ingredient not in products:
                products.add(ingredient)
                pending.append(ingredient)
    return tuple(sorted(products))


CRAFTSANITY_PRODUCTS = get_craftsanity_products()
assert len(CRAFTSANITY_PRODUCTS) == 192


def product_display_name(product: str) -> str:
    display = product.replace("-", " ").title()
    if product not in UNCOUNTABLE_PRODUCTS:
        if display.endswith("y") and not display.endswith(("ay", "ey", "oy")):
            display = display[:-1] + "ies"
        elif not display.endswith("s"):
            display += "s"
    return display


def location_name(product: str, ordinal: int) -> str:
    return f"Craft {product_display_name(product)} #{ordinal}"


class CraftContribution(typing.NamedTuple):
    amount: Fraction
    source: object
    required_technologies: frozenset[str]


def expand_product(contributions: dict[str, list[CraftContribution]], product: str, amount: Fraction,
                   source: object, required_technologies: frozenset[str],
                   custom_recipes: typing.Mapping[str, Recipe], stack: frozenset[str] = frozenset()) -> None:
    contributions[product].append(CraftContribution(amount, source, required_technologies))
    if product in stack:
        return
    recipe = get_product_recipe(product, custom_recipes)
    if not recipe:
        return
    executions = amount / Fraction(recipe.products[product])
    next_stack = stack | {product}
    for ingredient, ingredient_amount in recipe.ingredients.items():
        expand_product(contributions, ingredient, executions * ingredient_amount, source,
                       required_technologies, custom_recipes, next_stack)


def apportion_locations(maximums: typing.Mapping[str, Fraction], count: int) -> dict[str, int]:
    """Hamilton apportionment with one check per product and a 100-check product cap."""
    count = min(count, MAX_CRAFTSANITY_LOCATIONS)
    allocations = {product: 0 for product in CRAFTSANITY_PRODUCTS}
    ranked_products = sorted(CRAFTSANITY_PRODUCTS, key=lambda product: (maximums[product], product), reverse=True)
    if count <= len(ranked_products):
        for product in ranked_products[:count]:
            allocations[product] = 1
        return allocations

    for product in ranked_products:
        allocations[product] = 1
    remaining = count - len(ranked_products)

    while remaining:
        available = [product for product in ranked_products
                     if allocations[product] < min(MAX_CHECKS_PER_PRODUCT, math.ceil(maximums[product]))]
        if not available:
            break
        weights = {product: max(Fraction(), maximums[product] - allocations[product]) for product in available}
        weight_total = sum(weights.values())
        if not weight_total:
            break
        exact = {product: Fraction(remaining) * weights[product] / weight_total for product in available}
        additions = {
            product: min(int(exact[product]), MAX_CHECKS_PER_PRODUCT - allocations[product],
                         math.ceil(maximums[product]) - allocations[product])
            for product in available
        }
        added = sum(additions.values())
        for product, addition in additions.items():
            allocations[product] += addition
        remaining -= added
        if not remaining:
            break
        order = sorted(available, key=lambda product: (exact[product] - int(exact[product]),
                                                       maximums[product], product), reverse=True)
        progressed = False
        for product in order:
            if not remaining:
                break
            capacity = min(MAX_CHECKS_PER_PRODUCT, math.ceil(maximums[product]))
            if allocations[product] < capacity:
                allocations[product] += 1
                remaining -= 1
                progressed = True
        if not progressed and not added:
            break
    return allocations


def make_thresholds(maximum: Fraction, count: int) -> tuple[int, ...]:
    if not count:
        return ()
    final = max(1, math.ceil(maximum))
    if count == 1:
        return (final,)
    # count is capped to final by apportion_locations, so these are unique.
    return tuple(1 + ((final - 1) * index) // (count - 1) for index in range(count))

