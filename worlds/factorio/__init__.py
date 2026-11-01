from __future__ import annotations

import collections
import logging
import math
import typing
from fractions import Fraction

import Utils
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from worlds.generic import Rules
from .Locations import location_pools, location_table
from .CraftSanity import (CRAFTSANITY_PRODUCTS, CraftContribution, MAX_CRAFTSANITY_LOCATIONS,
                          ROCKET_PARTS_PER_LAUNCH, apportion_locations, expand_product, get_product_recipe,
                          location_name, make_thresholds)
from .Mod import generate_mod
from .Options import (FactorioOptions, MaxSciencePack, Silo, Satellite, TechTreeInformation, Goal,
                      TechCostDistribution, option_groups)
from .Shapes import get_shapes
from .Technologies import base_tech_table, recipe_sources, base_technology_table, \
    all_product_sources, required_technologies, get_rocket_requirements, \
    progressive_technology_table, common_tech_table, tech_to_progressive_lookup, progressive_tech_table, \
    get_science_pack_pools, Recipe, recipes, technology_table, tech_table, factorio_base_id, useless_technologies, \
    fluids, stacking_items, valid_ingredients, progressive_rows, machine_per_category
from .settings import FactorioSettings


def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="Factorio Client", args=args)


components.append(Component("Factorio Client", func=launch_client, component_type=Type.CLIENT))


class FactorioWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Factorio software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Berserker", "Farrak Kilhn"]
    )]
    option_groups = option_groups


class FactorioItem(Item):
    game = "Factorio"


all_items = tech_table.copy()
all_items["Attack Trap"] = factorio_base_id - 1
all_items["Evolution Trap"] = factorio_base_id - 2
all_items["Teleport Trap"] = factorio_base_id - 3
all_items["Grenade Trap"] = factorio_base_id - 4
all_items["Cluster Grenade Trap"] = factorio_base_id - 5
all_items["Artillery Trap"] = factorio_base_id - 6
all_items["Atomic Rocket Trap"] = factorio_base_id - 7
all_items["Atomic Cliff Remover Trap"] = factorio_base_id - 8
all_items["Inventory Spill Trap"] = factorio_base_id - 9
all_items["Craftsanity Filler"] = factorio_base_id - 10


WOOD_RECIPE_NAMES = {
    "light-armor", "heavy-armor", "modular-armor", "power-armor", "power-armor-mk2",
    "shotgun", "submachine-gun", "rocket-launcher", "flamethrower", "pistol", "combat-shotgun",
    "nuclear-reactor", "heat-pipe", "steam-turbine", "heat-exchanger", "steam-engine", "boiler",
    "car", "tank", "spidertron",
    "wooden-chest", "steel-chest", "iron-chest", "passive-provider-chest", "active-provider-chest",
    "storage-chest", "buffer-chest",
    "locomotive", "cargo-wagon", "fluid-wagon", "artillery-wagon",
    "burner-inserter", "rocket-silo", "cargo-landing-pad",
}
FULL_RECIPE_EXCLUSIONS = {"heavy-oil-cracking", "light-oil-cracking"}
CANONICAL_FLUID_RECIPES = {
    "petroleum-gas": "basic-oil-processing",
    "heavy-oil": "advanced-oil-processing",
    "light-oil": "advanced-oil-processing",
}
RAW_COST_PRODUCTS = {"coal", "copper-ore", "iron-ore", "stone", "wood", "raw-fish", "water", "crude-oil"}


def recipe_may_use_wood(recipe: Recipe) -> bool:
    return ("wood" in recipe.ingredients or recipe.name in WOOD_RECIPE_NAMES
            or recipe.name.endswith(("-armor", "-equipment")))


class Factorio(World):
    """
    Factorio is a game about automation. You play as an engineer who has crash landed on the planet
    Nauvis, an inhospitable world filled with dangerous creatures called biters. Build a factory,
    research new technologies, and become more efficient in your quest to build a rocket and return home.
    """
    game = "Factorio"
    special_nodes = {"automation", "logistics", "rocket-silo"}
    custom_recipes: typing.Dict[str, Recipe]
    custom_product_recipes: typing.Dict[str, Recipe]
    custom_recipe_requirements: typing.Dict[str, frozenset[str]]
    location_pool: typing.List[FactorioScienceLocation]
    advancement_technologies: typing.Set[str]

    web = FactorioWeb()
    options_dataclass = FactorioOptions
    options: FactorioOptions

    item_name_to_id = all_items
    location_name_to_id = location_table
    item_name_groups = {
        "Progressive": set(progressive_tech_table.keys()),
    }
    required_client_version = (0, 6, 0)
    if Utils.version_tuple < required_client_version:
        raise Exception(f"Update Archipelago to use this world ({game}).")
    ordered_science_packs: typing.List[str] = MaxSciencePack.get_ordered_science_packs()
    tech_tree_layout_prerequisites: typing.Dict[FactorioScienceLocation, typing.Set[FactorioScienceLocation]]
    tech_mix: int = 0
    skip_silo: bool = False
    origin_region_name = "Nauvis"
    science_locations: typing.List[FactorioScienceLocation]
    craftsanity_locations: typing.List[FactorioCraftsanityLocation]
    removed_technologies: typing.Set[str]
    settings: typing.ClassVar[FactorioSettings]
    trap_names: tuple[str] = ("Evolution", "Attack", "Teleport", "Grenade", "Cluster Grenade", "Artillery",
                              "Atomic Rocket", "Atomic Cliff Remover", "Inventory Spill")
    want_progressives: dict[str, bool] = collections.defaultdict(lambda: False)

    def __init__(self, world, player: int):
        super(Factorio, self).__init__(world, player)
        self.removed_technologies = useless_technologies.copy()
        self.advancement_technologies = set()
        self.custom_recipes = {}
        self.custom_product_recipes = {}
        self.custom_recipe_requirements = {}
        self.custom_product_requirements: dict[str, frozenset[str]] = {}
        self.custom_product_costs: dict[str, float] = {}
        self.vanilla_product_costs: dict[str, float] = {}
        self.full_recipe_order: list[str] = []
        self.science_locations = []
        self.craftsanity_locations = []
        self.tech_tree_layout_prerequisites = {}
        self.craftsanity_contributions: dict[str, list[CraftContribution]] = {}

    generate_output = generate_mod

    def generate_early(self) -> None:
        # if max < min, then swap max and min
        if self.options.max_tech_cost < self.options.min_tech_cost:
            self.options.min_tech_cost.value, self.options.max_tech_cost.value = \
                self.options.max_tech_cost.value, self.options.min_tech_cost.value
        self.tech_mix = self.options.tech_cost_mix.value
        self.skip_silo = self.options.silo.value == Silo.option_spawn
        self.want_progressives = collections.defaultdict(
            lambda: self.options.progressive.want_progressives(self.random))

    def create_regions(self):
        player = self.player
        random = self.random
        nauvis = Region("Nauvis", player, self.multiworld)

        location_count = len(base_tech_table) - len(useless_technologies) - self.skip_silo

        for name in self.trap_names:
            name = name.replace(" ", "_").lower()+"_traps"
            location_count += getattr(self.options, name)

        location_pool = []

        for pack in sorted(self.options.max_science_pack.get_allowed_packs()):
            location_pool.extend(location_pools[pack])
        try:
            # Ensure there are two "AP-1-" locations for automation and logistics, and one max science pack location
            # for rocket-silo if it is not pre-spawned
            max_science_pack_number = len(self.options.max_science_pack.get_allowed_packs())
            science_location_names = None
            while (not science_location_names or
                   len([location for location in science_location_names if location.startswith("AP-1-")]) < 2
                    or (self.options.silo != Silo.option_spawn and len([location for location in science_location_names
                            if location.startswith(f"AP-{max_science_pack_number}")]) < 1)):
                science_location_names = random.sample(location_pool, location_count)
        except ValueError as e:
            # should be "ValueError: Sample larger than population or is negative"
            raise Exception("Too many traps for too few locations. Either decrease the trap count, "
                            f"or increase the location count (higher max science pack). (Player {self.player})") from e

        self.science_locations = [FactorioScienceLocation(player, loc_name, self.location_name_to_id[loc_name], nauvis)
                                  for loc_name in science_location_names]

        distribution: TechCostDistribution = self.options.tech_cost_distribution
        min_cost = self.options.min_tech_cost.value
        max_cost = self.options.max_tech_cost.value
        if distribution == distribution.option_even:
            rand_values = (random.randint(min_cost, max_cost) for _ in self.science_locations)
        else:
            mode = {distribution.option_low: min_cost,
                    distribution.option_middle: (min_cost+max_cost)//2,
                    distribution.option_high: max_cost}[distribution.value]
            rand_values = (random.triangular(min_cost, max_cost, mode) for _ in self.science_locations)
        rand_values = sorted(rand_values)
        if self.options.ramping_tech_costs:
            def sorter(loc: FactorioScienceLocation):
                return loc.complexity, loc.rel_cost
        else:
            def sorter(loc: FactorioScienceLocation):
                return loc.rel_cost
        for i, location in enumerate(sorted(self.science_locations, key=sorter)):
            location.count = rand_values[i]
        del rand_values
        nauvis.locations.extend(self.science_locations)
        nauvis.locations.extend(self.craftsanity_locations)
        location = FactorioLocation(player, "Rocket Launch", None, nauvis)
        nauvis.locations.append(location)
        event = FactorioItem("Victory", ItemClassification.progression, None, player)
        location.place_locked_item(event)

        for ingredient in sorted(self.options.max_science_pack.get_allowed_packs()):
            location = FactorioLocation(player, f"Automate {ingredient}", None, nauvis)
            nauvis.locations.append(location)
            event = FactorioItem(f"Automated {ingredient}", ItemClassification.progression, None, player)
            location.place_locked_item(event)

        self.multiworld.regions.append(nauvis)

    def create_items(self) -> None:
        self.custom_technologies = self.set_custom_technologies()
        self.set_custom_recipes()
        self.create_craftsanity_locations()

        self.multiworld.itempool.extend(
            FactorioItem("Craftsanity Filler", ItemClassification.filler, all_items["Craftsanity Filler"], self.player)
            for _ in self.craftsanity_locations
        )

        # Craft checks can make additional recipe unlocks logically relevant.
        for location in self.craftsanity_locations:
            recipe = self.get_product_recipe(location.crafted_item)
            if recipe:
                self.advancement_technologies |= set(self.get_recipe_requirements(recipe))
        for technology in tuple(self.advancement_technologies):
            progressive = tech_to_progressive_lookup.get(technology)
            if progressive:
                self.advancement_technologies.add(progressive)

        for trap_name in self.trap_names:
            self.multiworld.itempool.extend(self.create_item(f"{trap_name} Trap") for _ in
                                            range(getattr(self.options,
                                                          f"{trap_name.lower().replace(' ', '_')}_traps")))

        cost_sorted_locations = sorted(self.science_locations, key=lambda location: location.name)
        special_index = {"automation": 0,
                         "logistics": 1,
                         "rocket-silo": -1}
        loc: FactorioScienceLocation
        if self.options.tech_tree_information == TechTreeInformation.option_full:
            # mark all locations as pre-hinted
            for loc in self.science_locations + self.craftsanity_locations:
                loc.revealed = True
        if self.skip_silo:
            self.removed_technologies |= {"rocket-silo"}
        for tech_name in base_tech_table:
            if tech_name not in self.removed_technologies:
                progressive_item_name = tech_to_progressive_lookup.get(tech_name, tech_name)
                want_progressive = self.want_progressives[progressive_item_name]
                item_name = progressive_item_name if want_progressive else tech_name
                tech_item = self.create_item(item_name)
                index = special_index.get(tech_name, None)
                if index is None:
                    self.multiworld.itempool.append(tech_item)
                else:
                    loc = cost_sorted_locations[index]
                    if index >= 0:
                        # beginning techs - limit cost to 10
                        # as automation is not achievable yet and hand-crafting for hours is not fun gameplay
                        loc.count = min(loc.count, 10)
                    loc.place_locked_item(tech_item)
                    loc.revealed = True

    def get_filler_item_name(self) -> str:
        tech_name: str = self.random.choice(tuple(tech_table))
        progressive_item_name: str = tech_to_progressive_lookup.get(tech_name, tech_name)
        want_progressive: bool = self.want_progressives[progressive_item_name]
        return progressive_item_name if want_progressive else tech_name

    def create_craftsanity_locations(self) -> None:
        requested_count = min(self.options.craftsanity.value, MAX_CRAFTSANITY_LOCATIONS)
        if not requested_count:
            return

        contributions: dict[str, list[CraftContribution]] = collections.defaultdict(list)

        # One of every product is the base demand. Its complete contribution becomes logical when the product's
        # selected recipe (including every recursive ingredient) can be crafted.
        for product in CRAFTSANITY_PRODUCTS:
            recipe = self.get_product_recipe(product)
            required_technology_names = self.get_product_requirements(product)
            expand_product(contributions, product, Fraction(1), None, required_technology_names,
                           self.custom_recipes, recipe_resolver=self.get_product_recipe)

        # The one-of-every-product baseline already includes one Rocket Part. Add the remainder needed for the
        # mandatory launch, including the complete randomized Rocket Part ingredient chain.
        silo_recipe = self.get_recipe("rocket-silo") if self.options.silo != Silo.option_spawn else None
        part_recipe = self.custom_recipes["rocket-part"]
        satellite_recipe = self.get_recipe("satellite") if self.options.goal == Goal.option_satellite else None
        cargo_pad_recipe = self.get_recipe("cargo-landing-pad") if self.options.silo != Silo.option_spawn else None
        rocket_requirement_names = self.get_rocket_requirements(
            silo_recipe, part_recipe, satellite_recipe, cargo_pad_recipe)
        if self.options.silo != Silo.option_spawn:
            rocket_requirement_names.add("rocket-silo")
        expand_product(contributions, "rocket-part", Fraction(ROCKET_PARTS_PER_LAUNCH - 1), None,
                       frozenset(rocket_requirement_names), self.custom_recipes,
                       recipe_resolver=self.get_product_recipe)

        # Generated AP researches contribute their actual science counts through the player's randomized recipes.
        # Their contribution becomes logical when that specific research location becomes reachable.
        for science_location in self.science_locations:
            for science_pack, pack_multiplier in science_location.ingredients.items():
                expand_product(contributions, science_pack,
                               Fraction(str(science_location.count)) * pack_multiplier,
                               science_location, frozenset(),
                               self.custom_recipes, recipe_resolver=self.get_product_recipe)

        maximums = {
            product: sum((contribution.amount for contribution in contributions[product]), Fraction())
            for product in CRAFTSANITY_PRODUCTS
        }
        allocations = apportion_locations(maximums, requested_count)
        if sum(allocations.values()) != requested_count:
            raise RuntimeError(f"Could only allocate {sum(allocations.values())} of {requested_count} "
                               f"Craftsanity locations for player {self.player}")
        nauvis = self.get_region("Nauvis")
        for product in CRAFTSANITY_PRODUCTS:
            thresholds = make_thresholds(maximums[product], allocations[product])
            for ordinal, threshold in enumerate(thresholds, 1):
                name = location_name(product, ordinal)
                location = FactorioCraftsanityLocation(
                    self.player, name, self.location_name_to_id[name], nauvis, product, ordinal, threshold,
                    self.get_product_recipe(product)
                )
                self.craftsanity_locations.append(location)
                nauvis.locations.append(location)
        self.craftsanity_contributions = dict(contributions)

    def set_rules(self):
        player = self.player
        shapes = get_shapes(self)

        for ingredient in self.options.max_science_pack.get_allowed_packs():
            location = self.get_location(f"Automate {ingredient}")

            if self.options.recipe_ingredients.value == self.options.recipe_ingredients.option_full:
                custom_recipe = self.custom_recipes[ingredient]
                requirements = self.get_recipe_requirements(custom_recipe)
                location.access_rule = lambda state, requirements=requirements: state.has_all(requirements, player)

            elif self.options.recipe_ingredients:
                custom_recipe = self.custom_recipes[ingredient]
                location.access_rule = lambda state, ingredient=ingredient, custom_recipe=custom_recipe: \
                    (not technology_table[ingredient].unlocks or state.has(ingredient, player)) and \
                    all(state.has(technology.name, player) for sub_ingredient in custom_recipe.ingredients
                        for technology in required_technologies[sub_ingredient]) and \
                    all(state.has(technology.name, player)
                        for technology in required_technologies[custom_recipe.crafting_machine])

            else:
                location.access_rule = lambda state, ingredient=ingredient: \
                    all(state.has(technology.name, player) for technology in required_technologies[ingredient])

        # Compile the dynamic expected-craft logic once. Calling can_reach on every contributing AP research from
        # every Craftsanity location made sphere calculation quadratic and repeated the same recursive shape checks
        # millions of times. A science location's reachability is fully described by its Automated-pack events and
        # those of its shape prerequisites, so collapse contributions with identical item requirements and scale all
        # Fraction amounts to integer weights.
        science_requirements: dict[FactorioScienceLocation, frozenset[str]] = {}

        def get_science_requirements(location: FactorioScienceLocation) -> frozenset[str]:
            cached = science_requirements.get(location)
            if cached is not None:
                return cached
            requirements = {f"Automated {ingredient}" for ingredient in location.ingredients}
            for prerequisite in shapes.get(location, ()):
                requirements.update(get_science_requirements(prerequisite))
            result = science_requirements[location] = frozenset(requirements)
            return result

        compiled_contributions: dict[str, tuple[int, tuple[tuple[int, frozenset[str]], ...]]] = {}
        for product, contributions in self.craftsanity_contributions.items():
            grouped: dict[frozenset[str], Fraction] = collections.defaultdict(Fraction)
            for contribution in contributions:
                requirements = (contribution.required_technologies if contribution.source is None
                                else get_science_requirements(contribution.source))
                grouped[requirements] += contribution.amount
            denominator = 1
            for amount in grouped.values():
                denominator = denominator * amount.denominator // math.gcd(denominator, amount.denominator)
            compiled_contributions[product] = denominator, tuple(
                (amount.numerator * (denominator // amount.denominator), requirements)
                for requirements, amount in grouped.items()
            )

        for location in self.craftsanity_locations:
            denominator, contributions = compiled_contributions[location.crafted_item]
            cutoff = (location.count - 1) * denominator

            def expected_crafts_rule(state, contributions=contributions, cutoff=cutoff):
                return sum(amount for amount, requirements in contributions
                           if state.has_all(requirements, player)) > cutoff

            location.access_rule = expected_crafts_rule

        for location in self.science_locations:
            Rules.set_rule(location, lambda state, ingredients=frozenset(location.ingredients):
                all(state.has(f"Automated {ingredient}", player) for ingredient in ingredients))
            prerequisites = shapes.get(location)
            if prerequisites:
                Rules.add_rule(location, lambda state, locations=frozenset(prerequisites):
                    all(state.can_reach(loc) for loc in locations))

        silo_recipe = None
        cargo_pad_recipe = None
        if self.options.silo != Silo.option_spawn:
            silo_recipe = self.get_recipe("rocket-silo")
            cargo_pad_recipe = self.get_recipe("cargo-landing-pad")
        part_recipe = self.custom_recipes["rocket-part"]
        satellite_recipe = self.get_recipe("satellite")
        victory_tech_names = self.get_rocket_requirements(
            silo_recipe, part_recipe, satellite_recipe if self.options.goal == Goal.option_satellite else None,
            cargo_pad_recipe)
        if self.options.silo == Silo.option_spawn:
            victory_tech_names -= {"rocket-silo"}
        else:
            victory_tech_names |= {"rocket-silo"}
        self.get_location("Rocket Launch").access_rule = lambda state: all(state.has(technology, player)
                                                                           for technology in
                                                                           victory_tech_names)
        self.multiworld.completion_condition[player] = lambda state: state.has('Victory', player)

    def get_recipe(self, name: str) -> Recipe:
        recipe = self.get_product_recipe(name)
        if not recipe:
            raise KeyError(name)
        return recipe

    def get_product_recipe(self, product: str) -> Recipe | None:
        if self.options.recipe_ingredients.value == self.options.recipe_ingredients.option_full:
            return self.custom_product_recipes.get(product)
        return get_product_recipe(product, self.custom_recipes)

    def get_recipe_requirements(self, recipe: Recipe) -> frozenset[str]:
        if self.options.recipe_ingredients.value == self.options.recipe_ingredients.option_full:
            return self.custom_recipe_requirements.get(recipe.name, frozenset())
        return frozenset(technology.name for technology in recipe.recursive_unlocking_technologies)

    def get_product_requirements(self, product: str) -> frozenset[str]:
        if self.options.recipe_ingredients.value == self.options.recipe_ingredients.option_full:
            return self.custom_product_requirements.get(product, frozenset())
        recipe = self.get_product_recipe(product)
        return self.get_recipe_requirements(recipe) if recipe else frozenset()

    def get_rocket_requirements(self, *rocket_recipes: Recipe | None) -> set[str]:
        if self.options.recipe_ingredients.value == self.options.recipe_ingredients.option_full:
            return set().union(*(self.get_recipe_requirements(recipe) for recipe in rocket_recipes if recipe))
        return get_rocket_requirements(*rocket_recipes)

    def generate_basic(self):
        map_basic_settings = self.options.world_gen.value["basic"]
        if map_basic_settings.get("seed", None) is None:  # allow seed 0
            # 32 bit uint
            map_basic_settings["seed"] = self.random.randint(0, 2 ** 32 - 1)

        start_location_hints: typing.Set[str] = self.options.start_location_hints.value

        for loc in self.science_locations:
            # show start_location_hints ingame
            if loc.name in start_location_hints:
                loc.revealed = True
            # make spoiler match mod info
            elif loc.revealed:
                start_location_hints.add(loc.name)

    def collect_item(self, state, item, remove=False):
        if item.advancement and item.name in progressive_technology_table:
            prog_table = progressive_technology_table[item.name].progressive
            if remove:
                for item_name in reversed(prog_table):
                    if state.has(item_name, item.player):
                        return item_name
            else:
                for item_name in prog_table:
                    if not state.has(item_name, item.player):
                        return item_name

        return super(Factorio, self).collect_item(state, item, remove)

    @classmethod
    def stage_write_spoiler(cls, world, spoiler_handle):
        factorio_players = world.get_game_players(cls.game)
        spoiler_handle.write('\n\nFactorio Recipes:\n')
        for player in factorio_players:
            name = world.get_player_name(player)
            for recipe in world.worlds[player].custom_recipes.values():
                spoiler_handle.write(f"\n{recipe.name} ({name}): {recipe.ingredients} -> {recipe.products}")

    @staticmethod
    def get_category(category: str, liquids: int) -> str:
        categories = {1: "crafting-with-fluid",
                      2: "chemistry"}
        return categories.get(liquids, category)

    def make_quick_recipe(self, original: Recipe, pool: list, allow_liquids: int = 2,
                          ingredients_offset: int = 0) -> Recipe:
        pool = [ingredient for ingredient in pool
                if ingredient != "raw-fish" and (ingredient != "wood" or recipe_may_use_wood(original))]
        count: int = len(original.ingredients) + ingredients_offset
        assert len(pool) >= count, f"Can't pick {count} many items from pool {pool}."
        new_ingredients = {}
        liquids_used = 0
        for _ in range(count):
            new_ingredient = pool.pop()
            if new_ingredient in fluids:
                while liquids_used == allow_liquids and new_ingredient in fluids:
                    # liquids already at max for current recipe.
                    # Return the liquid to the pool and get a new ingredient.
                    pool.append(new_ingredient)
                    new_ingredient = pool.pop(0)
                liquids_used += 1 if new_ingredient in fluids else 0
            new_ingredients[new_ingredient] = 1
        return Recipe(original.name, self.get_category(original.category, liquids_used), new_ingredients,
                      original.products, original.energy)

    def make_balanced_recipe(self, original: Recipe, pool: typing.Set[str], factor: float = 1,
                             allow_liquids: int = 2, ingredients_offset: int = 0) -> Recipe:
        """Generate a recipe from pool with time and cost similar to original * factor"""
        new_ingredients = {}
        # have to first sort for determinism, while filtering out non-stacking items
        forbidden = {"raw-fish"} if recipe_may_use_wood(original) else {"raw-fish", "wood"}
        pool: typing.List[str] = sorted((pool & valid_ingredients) - forbidden)
        # then sort with random data to shuffle
        self.random.shuffle(pool)
        target_raw = int(sum((count for ingredient, count in original.base_cost.items())) * factor)
        target_energy = original.total_energy * factor
        target_num_ingredients = len(original.ingredients) + ingredients_offset
        remaining_raw = target_raw
        remaining_energy = target_energy
        remaining_num_ingredients = target_num_ingredients
        fallback_pool = []
        liquids_used = 0

        # fill all but one slot with random ingredients, last with a good match
        while remaining_num_ingredients > 0 and pool:
            ingredient = pool.pop()
            if liquids_used == allow_liquids and ingredient in fluids:
                continue  # can't use this ingredient as we already have maximum liquid in our recipe.
            ingredient_raw = 0
            if ingredient in all_product_sources:
                ingredient_recipe = min(all_product_sources[ingredient], key=lambda recipe: recipe.rel_cost)
                ingredient_raw = sum((count for ingredient, count in ingredient_recipe.base_cost.items()))
                ingredient_energy = ingredient_recipe.total_energy
            else:
                # assume simple ore TODO: remove if tree when mining data is harvested from Factorio
                ingredient_energy = 2
            if not ingredient_raw:
                ingredient_raw = 1
            if remaining_num_ingredients == 1:
                max_raw = 1.1 * remaining_raw
                min_raw = 0.9 * remaining_raw
                max_energy = 1.1 * remaining_energy
                min_energy = 0.9 * remaining_energy
            else:
                max_raw = remaining_raw * 0.75
                min_raw = (remaining_raw - max_raw) / remaining_num_ingredients
                max_energy = remaining_energy * 0.75
                min_energy = (remaining_energy - max_energy) / remaining_num_ingredients
            min_num_raw = min_raw / ingredient_raw
            max_num_raw = max_raw / ingredient_raw
            min_num_energy = min_energy / ingredient_energy
            max_num_energy = max_energy / ingredient_energy
            min_num = int(max(1, min_num_raw, min_num_energy))
            max_num = int(min(max_num_raw, max_num_energy))
            if min_num > max_num:
                fallback_pool.append(ingredient)
                continue  # can't use that ingredient
            num = self.random.randint(min_num, max_num)
            new_ingredients[ingredient] = num
            remaining_raw -= num * ingredient_raw
            remaining_energy -= num * ingredient_energy
            remaining_num_ingredients -= 1
            if ingredient in fluids:
                liquids_used += 1

        # fill failed slots with whatever we got
        pool = fallback_pool
        while remaining_num_ingredients > 0 and pool:
            ingredient = pool.pop()
            if liquids_used == allow_liquids and ingredient in fluids:
                continue  # can't use this ingredient as we already have maximum liquid in our recipe.

            ingredient_recipe = recipes.get(ingredient, None)
            if not ingredient_recipe and ingredient.endswith("-barrel"):
                ingredient_recipe = recipes.get(f"fill-{ingredient}", None)
            if not ingredient_recipe:
                logging.warning(f"missing recipe for {ingredient}")
                continue
            ingredient_raw = sum((count for ingredient, count in ingredient_recipe.base_cost.items()))
            ingredient_energy = ingredient_recipe.total_energy
            num_raw = remaining_raw / ingredient_raw / remaining_num_ingredients
            num_energy = remaining_energy / ingredient_energy / remaining_num_ingredients
            num = int(min(num_raw, num_energy))
            if num < 1:
                continue

            new_ingredients[ingredient] = num
            remaining_raw -= num * ingredient_raw
            remaining_energy -= num * ingredient_energy
            remaining_num_ingredients -= 1
            if ingredient in fluids:
                liquids_used += 1

        if remaining_num_ingredients > 1:
            logging.warning("could not randomize recipe")

        return Recipe(original.name, self.get_category(original.category, liquids_used), new_ingredients,
                      original.products, original.energy)

    def recipe_cost_multiplier(self) -> float:
        variance = self.options.recipe_cost_variance.value
        if not variance:
            return 1.0
        anchors = ((0, 0.0), (25, math.log10(2)), (50, 1.0), (75, 2.0), (100, 3.0))
        for (low, low_radius), (high, high_radius) in zip(anchors, anchors[1:]):
            if variance <= high:
                radius = low_radius + (high_radius - low_radius) * (variance - low) / (high - low)
                return 10 ** self.random.uniform(-radius, radius)
        raise ValueError(variance)

    def select_ingredients_for_cost(self, item_pool: typing.Iterable[str], item_count: int,
                                    fluid_pool: typing.Iterable[str], fluid_count: int,
                                    target_cost: float) -> list[str]:
        """Select a varied valid ingredient set before using quantities to make up the remaining cost."""
        item_pool = sorted(set(item_pool))
        fluid_pool = sorted(set(fluid_pool))
        if len(item_pool) < item_count or len(fluid_pool) < fluid_count:
            raise ValueError("not enough available ingredients")

        candidates: list[tuple[str, ...]] = []
        attempts = max(64, min(256, (len(item_pool) + len(fluid_pool)) * 2))
        for _ in range(attempts):
            selected = tuple(self.random.sample(item_pool, item_count) +
                             self.random.sample(fluid_pool, fluid_count))
            candidates.append(selected)

        # Ensure both cost extremes are considered even when the randomized search does not happen to sample them.
        for reverse in (False, True):
            selected_items = sorted(item_pool, key=self.recipe_unit_cost, reverse=reverse)[:item_count]
            selected_fluids = sorted(fluid_pool, key=self.recipe_unit_cost, reverse=reverse)[:fluid_count]
            candidates.append(tuple(selected_items + selected_fluids))

        def score(selected: tuple[str, ...]) -> float:
            selected_cost = sum(self.recipe_unit_cost(ingredient) for ingredient in selected)
            return abs(math.log(max(selected_cost, 1e-12) / max(target_cost, 1e-12)))

        return list(min(candidates, key=score))

    def compensate_recipe_cost(self, selected: typing.Iterable[str], target_cost: float) -> dict[str, int]:
        """Approach target_cost while preferring costly ingredients and therefore fewer total input units."""
        selected = list(selected)
        ingredients = {ingredient: 1 for ingredient in selected}
        realized_cost = sum(self.recipe_unit_cost(ingredient) for ingredient in selected)
        remaining_cost = target_cost - realized_cost
        if remaining_cost <= 0:
            return ingredients

        by_descending_cost = sorted(selected, key=self.recipe_unit_cost, reverse=True)
        for index, ingredient in enumerate(by_descending_cost):
            unit_cost = self.recipe_unit_cost(ingredient)
            if index == len(by_descending_cost) - 1:
                extra = max(0, round(remaining_cost / unit_cost))
            else:
                extra = max(0, int(remaining_cost // unit_cost))
            ingredients[ingredient] += extra
            remaining_cost -= extra * unit_cost
        return ingredients

    def apply_recipe_cost_variance(self, recipe: Recipe, pool: typing.Optional[typing.Iterable[str]] = None,
                                   target_recipe: typing.Optional[Recipe] = None) -> Recipe:
        multiplier = self.recipe_cost_multiplier()
        if multiplier == 1:
            return recipe
        target_recipe = target_recipe or recipe
        target_cost = max(float(len(recipe.ingredients)), self.vanilla_recipe_cost(target_recipe)) * multiplier
        selected = list(recipe.ingredients)
        if pool is not None:
            forbidden = {"raw-fish"} if recipe_may_use_wood(target_recipe) else {"raw-fish", "wood"}
            eligible = (set(pool) & valid_ingredients) - forbidden - set(recipe.products)
            item_count = sum(ingredient not in fluids for ingredient in selected)
            fluid_count = len(selected) - item_count
            selected = self.select_ingredients_for_cost(eligible - fluids, item_count, eligible & fluids,
                                                        fluid_count, target_cost)
        ingredients = self.compensate_recipe_cost(selected, target_cost)
        return Recipe(recipe.name, recipe.category, ingredients, recipe.products, recipe.energy)

    def recipe_unit_cost(self, product: str) -> float:
        generated_cost = self.custom_product_costs.get(product)
        if generated_cost is not None:
            return generated_cost
        sources = [source for source in all_product_sources.get(product, ()) if source.ingredients]
        if not sources:
            return 1.0
        return max(1.0, min(sum(source.base_cost.values()) / max(source.products.get(product, 1), 1)
                            for source in sources))

    def vanilla_product_cost(self, product: str, stack: frozenset[str] = frozenset()) -> float:
        if product in RAW_COST_PRODUCTS or product in stack:
            return 1.0
        cached = self.vanilla_product_costs.get(product)
        if cached is not None:
            return cached
        recipe = get_product_recipe(product)
        if not recipe:
            return 1.0
        next_stack = stack | {product}
        cost = sum(amount * self.vanilla_product_cost(ingredient, next_stack)
                   for ingredient, amount in recipe.ingredients.items()) / max(recipe.products[product], 1)
        self.vanilla_product_costs[product] = max(cost, 1.0)
        return self.vanilla_product_costs[product]

    def vanilla_recipe_cost(self, recipe: Recipe) -> float:
        return sum(amount * self.vanilla_product_cost(ingredient)
                   for ingredient, amount in recipe.ingredients.items())

    def make_full_recipe(self, original: Recipe, available: set[str], terminal_products: set[str],
                         smelting_ingredients: set[str]) -> Recipe:
        offset_names = set(self.ordered_science_packs) | {"rocket-part"}
        offset = self.options.recipe_ingredients_offset.value if original.name in offset_names else 0
        original_fluid_count = sum(ingredient in fluids for ingredient in original.ingredients)
        target_count = max(1, len(original.ingredients) + offset)
        fluid_count = min(original_fluid_count, target_count)
        item_count = target_count - fluid_count
        excluded = set(original.products)
        forbidden = terminal_products | {"raw-fish"}
        if original.category == "smelting":
            forbidden |= smelting_ingredients
        if not recipe_may_use_wood(original):
            forbidden.add("wood")
        item_pool = sorted((available & valid_ingredients) - fluids - excluded - forbidden)
        fluid_pool = sorted((available & valid_ingredients & fluids) - excluded - forbidden)
        if len(item_pool) < item_count or len(fluid_pool) < fluid_count:
            raise ValueError("not enough available ingredients")
        # Every distinct ingredient has a minimum integral amount of one. Added ingredient slots therefore raise
        # the minimum achievable target instead of making a zero-variance recipe mathematically impossible.
        target_raw = max(float(target_count), self.vanilla_recipe_cost(original)) * self.recipe_cost_multiplier()
        if not self.options.recipe_cost_variance.value:
            per_slot = target_raw / target_count
            affordable_items = [ingredient for ingredient in item_pool
                                if self.recipe_unit_cost(ingredient) <= per_slot]
            affordable_fluids = [ingredient for ingredient in fluid_pool
                                 if self.recipe_unit_cost(ingredient) <= per_slot]
            if len(affordable_items) < item_count or len(affordable_fluids) < fluid_count:
                raise ValueError("not enough affordable ingredients")
            selected = (self.random.sample(affordable_items, item_count) +
                        self.random.sample(affordable_fluids, fluid_count))
            ingredients = {
                ingredient: max(1, int(per_slot / self.recipe_unit_cost(ingredient)))
                for ingredient in selected
            }
        else:
            selected = self.select_ingredients_for_cost(item_pool, item_count, fluid_pool, fluid_count, target_raw)
            ingredients = self.compensate_recipe_cost(selected, target_raw)
        return Recipe(original.name, original.category, ingredients, original.products, original.energy)

    def set_full_custom_recipes(self) -> None:
        natural_resources = {"coal", "copper-ore", "iron-ore", "stone", "wood", "raw-fish"}
        available = natural_resources | set(self.options.starting_items.value) | {"character"}
        self.custom_product_requirements = {product: frozenset() for product in available}
        self.custom_product_costs = {product: 1.0 for product in natural_resources}
        self.custom_product_costs.update({product: self.vanilla_product_cost(product)
                                          for product in self.options.starting_items.value})
        usable = {
            recipe.name: recipe for recipe in recipes.values()
            if recipe.ingredients and recipe.products and not recipe.name.startswith(("mining-", "empty-"))
            and recipe.category != "parameters" and recipe.name not in FULL_RECIPE_EXCLUSIONS
        }
        start_names = {name for name in usable if not recipe_sources.get(name)}
        pending = dict(usable)
        terminal_products: set[str] = set()
        smelting_ingredients: set[str] = set()

        while pending:
            restricted_to_start = bool(start_names & pending.keys())
            candidates: list[tuple[str, Recipe]] = []
            for name, original in sorted(pending.items()):
                if restricted_to_start and name not in start_names:
                    continue
                machine = machine_per_category[original.category]
                if machine not in available:
                    continue
                offset_names = set(self.ordered_science_packs) | {"rocket-part"}
                offset = self.options.recipe_ingredients_offset.value if name in offset_names else 0
                target_count = max(1, len(original.ingredients) + offset)
                fluid_count = min(sum(ingredient in fluids for ingredient in original.ingredients), target_count)
                excluded = set(original.products)
                forbidden = terminal_products | {"raw-fish"}
                if original.category == "smelting":
                    forbidden |= smelting_ingredients
                if not recipe_may_use_wood(original):
                    forbidden.add("wood")
                available_items = len((available & valid_ingredients) - fluids - excluded - forbidden)
                available_fluids = len((available & valid_ingredients & fluids) - excluded - forbidden)
                if available_items < target_count - fluid_count or available_fluids < fluid_count:
                    continue
                if not self.options.recipe_cost_variance.value:
                    per_slot = max(float(target_count), self.vanilla_recipe_cost(original)) / target_count
                    affordable_items = sum(self.recipe_unit_cost(ingredient) <= per_slot
                                           for ingredient in (available & valid_ingredients) - fluids - excluded - forbidden)
                    affordable_fluids = sum(self.recipe_unit_cost(ingredient) <= per_slot
                                            for ingredient in (available & valid_ingredients & fluids) - excluded - forbidden)
                    if affordable_items < target_count - fluid_count or affordable_fluids < fluid_count:
                        continue
                candidates.append((name, original))
            if not candidates:
                blocked = ", ".join(sorted(pending)[:20])
                raise RuntimeError(f"Full recipe randomization became stuck with {len(pending)} recipes: {blocked}")

            name, original = self.random.choice(candidates)
            custom = self.make_full_recipe(original, available, terminal_products, smelting_ingredients)
            machine = machine_per_category[custom.category]
            self.custom_recipes[name] = custom
            self.full_recipe_order.append(name)
            requirements = set()
            for ingredient in custom.ingredients:
                requirements.update(self.custom_product_requirements.get(ingredient, ()))
            requirements.update(self.custom_product_requirements.get(machine_per_category[custom.category], ()))
            sources = sorted(recipe_sources.get(name, ()))
            if sources:
                requirements.add(sources[0])
            frozen_requirements = self.custom_recipe_requirements[name] = frozenset(requirements)
            if "wood" in custom.ingredients:
                terminal_products.update(custom.products)
            if custom.category == "smelting":
                smelting_ingredients.update(custom.ingredients)
            total_cost = sum(amount * self.recipe_unit_cost(ingredient)
                             for ingredient, amount in custom.ingredients.items())
            for product in custom.products:
                # Raw resources deliberately have no canonical recipe. For every crafted product, retain the first
                # dependency-safe producer; alternate recipes must not retroactively change its recursive cost.
                canonical_recipe = CANONICAL_FLUID_RECIPES.get(product)
                is_canonical = canonical_recipe == name if canonical_recipe else product not in natural_resources
                if is_canonical and product not in self.custom_product_recipes:
                    self.custom_product_recipes[product] = custom
                    self.custom_product_requirements[product] = frozen_requirements
                    self.custom_product_costs[product] = total_cost / max(custom.products[product], 1)
                if canonical_recipe is None or canonical_recipe == name:
                    available.add(product)
            del pending[name]

            if "offshore-pump" in available and "water" not in available:
                available.add("water")
                self.custom_product_requirements["water"] = self.custom_product_requirements["offshore-pump"]
                self.custom_product_costs["water"] = 1.0
            if "pumpjack" in available and "crude-oil" not in available:
                available.add("crude-oil")
                self.custom_product_requirements["crude-oil"] = self.custom_product_requirements["pumpjack"]
                self.custom_product_costs["crude-oil"] = 1.0
            if {"electric-mining-drill", "sulfuric-acid"} <= available and "uranium-ore" not in available:
                available.add("uranium-ore")
                self.custom_product_requirements["uranium-ore"] = frozenset(
                    self.custom_product_requirements["electric-mining-drill"] |
                    self.custom_product_requirements["sulfuric-acid"])
                uranium_mining = recipes["mining-uranium-ore"]
                self.custom_product_costs["uranium-ore"] = sum(
                    amount * self.recipe_unit_cost(ingredient)
                    for ingredient, amount in uranium_mining.ingredients.items()
                ) / max(uranium_mining.products["uranium-ore"], 1)

    def set_custom_technologies(self):
        custom_technologies = {}
        allowed_packs = self.options.max_science_pack.get_allowed_packs()
        for technology_name, technology in base_technology_table.items():
            custom_technologies[technology_name] = technology.get_custom(self, allowed_packs, self.player)
        return custom_technologies

    def set_custom_recipes(self):
        ingredients_offset = self.options.recipe_ingredients_offset
        if self.options.recipe_ingredients.value == self.options.recipe_ingredients.option_full:
            self.custom_recipes = {}
            self.set_full_custom_recipes()
        else:
            self.set_legacy_custom_recipes(ingredients_offset)

        science_pack_pools = get_science_pack_pools()
        bridge = "ap-energy-bridge"
        new_recipe = self.make_quick_recipe(
            Recipe(bridge, "crafting", {"replace_1": 1, "replace_2": 1, "replace_3": 1,
                                        "replace_4": 1, "replace_5": 1, "replace_6": 1},
                   {bridge: 1}, 10),
            sorted(science_pack_pools[self.options.max_science_pack.get_ordered_science_packs()[0]]),
            ingredients_offset=ingredients_offset.value)
        for ingredient_name in new_recipe.ingredients:
            new_recipe.ingredients[ingredient_name] = self.random.randint(50, 500)
        self.custom_recipes[bridge] = new_recipe

        needed_recipes = self.options.max_science_pack.get_allowed_packs() | {"rocket-part"}
        if self.options.silo != Silo.option_spawn:
            needed_recipes |= {"rocket-silo", "cargo-landing-pad"}
        if self.options.goal.value == Goal.option_satellite:
            needed_recipes |= {"satellite"}

        for recipe_name in needed_recipes:
            recipe = self.custom_recipes.get(recipe_name, recipes[recipe_name])
            self.advancement_technologies |= set(self.get_recipe_requirements(recipe))

        prog_add = {tech_to_progressive_lookup[tech] for tech in self.advancement_technologies
                    if tech in tech_to_progressive_lookup}
        self.advancement_technologies |= prog_add

    def set_legacy_custom_recipes(self, ingredients_offset) -> None:
        original_rocket_part = recipes["rocket-part"]
        science_pack_pools = get_science_pack_pools()
        valid_pool = sorted(science_pack_pools[self.options.max_science_pack.get_max_pack()]
                            & valid_ingredients)
        self.random.shuffle(valid_pool)
        rocket_recipe = Recipe("rocket-part", original_rocket_part.category,
                               {valid_pool[x]: 10 for x in range(3 + ingredients_offset)},
                               original_rocket_part.products, original_rocket_part.energy)
        self.custom_recipes = {"rocket-part": self.apply_recipe_cost_variance(
            rocket_recipe, valid_pool, original_rocket_part)}

        if self.options.recipe_ingredients:
            valid_pool = []
            for pack in self.options.max_science_pack.get_ordered_science_packs():
                valid_pool += sorted(science_pack_pools[pack])
                self.random.shuffle(valid_pool)
                if pack in recipes:  # skips over space science pack
                    new_recipe = self.make_quick_recipe(recipes[pack], valid_pool, ingredients_offset=
                                                        ingredients_offset.value)
                    self.custom_recipes[pack] = self.apply_recipe_cost_variance(
                        new_recipe, valid_pool, recipes[pack])

        if self.options.silo.value == Silo.option_randomize_recipe \
                or self.options.satellite.value == Satellite.option_randomize_recipe:
            valid_pool = set()
            for pack in sorted(self.options.max_science_pack.get_allowed_packs()):
                valid_pool |= science_pack_pools[pack]

            if self.options.silo.value == Silo.option_randomize_recipe:
                new_recipe = self.make_balanced_recipe(
                    recipes["rocket-silo"], valid_pool,
                    factor=(self.options.max_science_pack.value + 1) / 7,
                    ingredients_offset=ingredients_offset.value)
                self.custom_recipes["rocket-silo"] = self.apply_recipe_cost_variance(
                    new_recipe, valid_pool, recipes["rocket-silo"])

            if self.options.satellite.value == Satellite.option_randomize_recipe:
                new_recipe = self.make_balanced_recipe(
                    recipes["satellite"], valid_pool,
                    factor=(self.options.max_science_pack.value + 1) / 7,
                    ingredients_offset=ingredients_offset.value)
                self.custom_recipes["satellite"] = self.apply_recipe_cost_variance(
                    new_recipe, valid_pool, recipes["satellite"])

    def create_item(self, name: str) -> FactorioItem:
        if name in tech_table:  # is a Technology
            if name in self.advancement_technologies:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler
            return FactorioItem(name,
                                classification,
                                tech_table[name], self.player)

        item = FactorioItem(name,
                            ItemClassification.trap if name.endswith("Trap") else ItemClassification.filler,
                            all_items[name], self.player)
        return item


class FactorioLocation(Location):
    game: str = Factorio.game


class FactorioCraftsanityLocation(FactorioLocation):
    ingredients = {}
    count = 0
    revealed = False

    crafted_item: str
    ordinal: int
    production_statistic: bool

    def __init__(self, player: int, name: str, address: int, parent: Region,
                 crafted_item: str, ordinal: int, count: int, recipe: Recipe | None):
        super(FactorioCraftsanityLocation, self).__init__(player, name, address, parent)
        self.crafted_item = crafted_item
        self.ordinal = ordinal
        self.count = count
        # Mining and pumping do not satisfy Factorio's native craft-item/craft-fluid research triggers. Track their
        # production statistics from control.lua so ingredient-chain checks for ores, crude oil, water, etc. work.
        self.production_statistic = recipe is None or recipe.name.startswith("mining-")


class FactorioScienceLocation(FactorioLocation):
    complexity: int
    revealed: bool = False
    crafted_item = None
    production_statistic = False

    # Factorio technology properties:
    ingredients: typing.Dict[str, int]
    count: int = 0

    def __init__(self, player: int, name: str, address: int, parent: Region):
        super(FactorioScienceLocation, self).__init__(player, name, address, parent)
        # "AP-{Complexity}-{Cost}"
        self.complexity = int(self.name[3]) - 1
        self.rel_cost = int(self.name[5:])

        self.ingredients = {Factorio.ordered_science_packs[self.complexity]: 1}
        for complexity in range(self.complexity):
            if (parent.multiworld.worlds[self.player].options.tech_cost_mix >
                    parent.multiworld.worlds[self.player].random.randint(0, 99)):
                self.ingredients[Factorio.ordered_science_packs[complexity]] = 1

    @property
    def factorio_ingredients(self) -> typing.List[typing.Tuple[str, int]]:
        return [(name, count) for name, count in self.ingredients.items()]
