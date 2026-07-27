from collections.abc import Iterable, Sequence

from BaseClasses import CollectionState, ItemClassification
from test.bases import WorldTestBase

from .. import SM64World


class SM64TestBase(WorldTestBase):
    game = SM64World.game
    world: SM64World

    def run_location_tests(
            self,
            access_pool: Sequence[Sequence],
            starting_regions: Iterable[str] = (),
    ) -> None:
        """Run ALttP-style ``[location, access, items, all_except?]`` logic cases."""
        for location_name, expected_access, *item_pool in access_pool:
            item_names = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            with self.subTest(
                    location=location_name,
                    access=expected_access,
                    items=item_names,
                    all_except=all_except,
            ):
                if all_except:
                    items = [
                        item
                        for item in self.multiworld.get_items()
                        if item.name not in all_except
                    ]
                    items.extend(self.world.create_item(item_name) for item_name in item_names)
                else:
                    items = [self.world.create_item(item_name) for item_name in item_names]

                state = CollectionState(self.multiworld)
                state.reachable_regions[self.player].add(self.multiworld.get_region("Menu", self.player))
                for region_name in starting_regions:
                    region = self.multiworld.get_region(region_name, self.player)
                    state.reachable_regions[self.player].add(region)
                    for entrance in region.exits:
                        if entrance.connected_region is not None:
                            state.blocked_connections[self.player].add(entrance)

                for item in items:
                    item.classification = ItemClassification.progression
                    state.collect(item, prevent_sweep=True)
                state.sweep_for_advancements()

                location = self.multiworld.get_location(location_name, self.player)
                self.assertEqual(
                    location.can_reach(state),
                    expected_access,
                    f"failed {location} with: {item_pool}",
                )
