import typing
import logging
from logging import Logger

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any
from worlds.ff6wc import Rom

snes_logger: Logger = logging.getLogger("SNES")


class FF6WCClient(SNIClient):
    game: str = "Final Fantasy 6 Worlds Collide"
    location_names: typing.List = list(Rom.event_flag_location_names)
    location_ids = None

    def __init__(self):
        super()

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name: bytes = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom_name is None or rom_name[:3] != b"6WC":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001

        ctx.rom = rom_name

        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom: bytes = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom != ctx.rom:
            ctx.rom = None
            return

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        if self.location_ids is None:
            self.location_ids = dict((v, k) for k, v in ctx.location_names.items())

        map_data = await snes_read(ctx, Rom.map_index_address, 2)
        if map_data is None:
            return
        map_index = int.from_bytes(map_data, "little")
        map_index = Rom.get_map_index(map_index)
        if map_index < 6:
            return
        for location_index in range(len(Rom.event_flag_location_names)):
            location_name = self.location_names[location_index]
            location_id = self.location_ids[location_name]
            event_byte, event_bit = Rom.get_event_flag_value(Rom.event_flag_location_names[location_name])
            event_data = await snes_read(ctx, event_byte, 1)

            if event_data is not None:
                # Have to special case these, since they work differently.
                if location_name in ["Lone Wolf 1", "Lone Wolf 2", "Narshe Weapon Shop 1", "Narshe Weapon Shop 3"]:
                    if location_name[0] == "L":
                        initial_event_done = Rom.additional_event_flags["Lone Wolf Encountered"]
                        first_reward_chosen = Rom.additional_event_flags["Lone Wolf First Reward Picked"]
                        both_rewards_obtained = Rom.additional_event_flags["Lone Wolf Both Rewards Picked"]
                        location_one = "Lone Wolf 1"
                        location_two = "Lone Wolf 2"
                    else:
                        initial_event_done = Rom.additional_event_flags["Narshe Weapon Shop Encountered"]
                        first_reward_chosen = Rom.additional_event_flags["Narshe Weapon Shop First Reward Picked"]
                        both_rewards_obtained = Rom.additional_event_flags["Narshe Weapon Shop Both Rewards Picked"]
                        location_one = "Narshe Weapon Shop 1"
                        location_two = "Narshe Weapon Shop 2"
                    event_byte, event_bit = Rom.get_event_flag_value(initial_event_done)
                    first_reward_byte, first_reward_bit = Rom.get_event_flag_value(first_reward_chosen)
                    both_rewards_byte, both_rewards_bit = Rom.get_event_flag_value(both_rewards_obtained)
                    initial_event_data = await snes_read(ctx, event_byte, 1)
                    first_reward_data = await snes_read(ctx, first_reward_byte, 1)
                    both_rewards_data = await snes_read(ctx, both_rewards_byte, 1)
                    if initial_event_data is not None \
                            and first_reward_data is not None \
                            and both_rewards_data is not None:
                        initial_event_status = initial_event_data[0] & event_bit
                        both_rewards_status = both_rewards_data[0] & both_rewards_bit
                        if initial_event_status or both_rewards_status:
                            first_reward_status = first_reward_data[0] & first_reward_bit
                            locations_cleared = []
                            if first_reward_status:
                                locations_cleared.append(location_one)
                            else:
                                locations_cleared.append(location_two)
                            if both_rewards_status:
                                locations_cleared = [location_one, location_two]
                            for location_name in locations_cleared:
                                location_id = self.location_ids[location_name]
                                if location_id not in ctx.locations_checked:
                                    ctx.locations_checked.add(location_id)
                                    snes_logger.info(
                                        f'New Check: {location_name} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])
                else:
                    event_done = event_data[0] & event_bit
                    if event_done and location_id not in ctx.locations_checked:
                        ctx.locations_checked.add(location_id)
                        snes_logger.info(
                            f'New Check: {location_name} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

        treasure_data = await snes_read(ctx, Rom.treasure_chest_base_address, 40)

        if treasure_data is not None:
            for chest in Rom.treasure_chest_data.keys():
                treasure_byte, treasure_bit = Rom.get_treasure_chest_bit(chest)
                treasure_found = treasure_data[treasure_byte] & treasure_bit
                treasure_id = self.location_ids[chest]
                if treasure_found and treasure_id not in ctx.locations_checked:
                    ctx.locations_checked.add(treasure_id)
                    snes_logger.info(
                        f'New Check: {chest} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [treasure_id]}])


        items_received_data = await snes_read(ctx, Rom.items_received_address, 2)
        if items_received_data is None:
            return
        items_received_amount = int.from_bytes(items_received_data, "little")
        if items_received_amount >= len(ctx.items_received):
            return
        else:
            item = ctx.items_received[items_received_amount]
            item_name = ctx.item_names[item.item]
            item_id = item.item
            if item_name in Rom.characters:
                character_index = Rom.characters.index(item_name)
                character_init_byte, character_init_bit = Rom.get_character_initialized_bit(character_index)
                character_init_data = await snes_read(ctx, character_init_byte, 1)
                if character_init_data is None:
                    return

                character_recruit_byte, character_recruit_bit = Rom.get_character_recruited_bit(character_index)
                character_recruit_data = await snes_read(ctx, character_recruit_byte, 1)
                if character_recruit_data is None:
                    return
                character_count = await snes_read(ctx, Rom.characters_obtained_address, 1)
                if character_count is None:
                    return
                character_count = character_count[0]
                character_initialized = character_init_data[0] & character_init_bit
                character_recruited = character_recruit_data[0] & character_recruit_bit
                if not (character_initialized and character_recruited):
                    character_name = Rom.characters[character_index]
                    character_ap_id = item_id
                    character_item = next((item for item in ctx.items_received if item.item == character_ap_id),
                                          None)
                    if character_item is not None:
                        new_init_data = character_init_data[0] | character_init_bit
                        new_recruit_data = character_recruit_data[0] | character_recruit_bit
                        snes_buffered_write(ctx, character_init_byte, bytes([new_init_data]))
                        snes_buffered_write(ctx, character_recruit_byte, bytes([new_recruit_data]))
                        snes_buffered_write(ctx, Rom.items_received_address, bytes([items_received_amount + 1]))

                        snes_buffered_write(ctx, Rom.characters_obtained_address, bytes([character_count + 1]))
                        snes_logger.info('Received %s from %s (%s)' % (
                            ctx.item_names[character_item.item],
                            ctx.player_names[character_item.player],
                            ctx.location_names[character_item.location]))
            elif item_name in Rom.espers:
                esper_index = Rom.espers.index(item_name)
                esper_byte, esper_bit = Rom.get_obtained_esper_bit(esper_index)
                esper_data = await snes_read(ctx, esper_byte, 1)
                if esper_data is None:
                    return
                esper_count = await snes_read(ctx, Rom.espers_obtained_address, 1)
                if esper_count is None:
                    return
                esper_count = esper_count[0]
                esper_obtained = esper_data[0] & esper_bit
                if esper_obtained == 0:
                    new_data = esper_data[0] | esper_bit
                    snes_buffered_write(ctx, esper_byte, bytes([new_data]))

                    snes_buffered_write(ctx, Rom.items_received_address, bytes([items_received_amount + 1]))

                    snes_buffered_write(ctx, Rom.espers_obtained_address, bytes([esper_count + 1]))
                    snes_logger.info('Received %s from %s (%s)' % (
                        ctx.item_names[item.item],
                        ctx.player_names[item.player],
                        ctx.location_names[item.location]))

            else:
                item_types_data = await snes_read(ctx, Rom.item_types_base_address, 255)
                item_quantities_data = await snes_read(ctx, Rom.item_quantities_base_address, 255)
                if item_types_data is None or item_quantities_data is None:
                    return
                reserved_slots = []
                for i in range(0, 255):
                    slot = item_types_data[i]
                    print("slot" + str(i) + ":" + str(slot))
                    quantity = item_quantities_data[i]
                    exists = False
                    if slot == Rom.item_name_id[item_name]:
                        exists = True
                    if (slot == 255 or quantity == 0 or exists == True):
                        reserved_slots.append(i)
                        type_destination = Rom.item_types_base_address + i
                        amount_destination = Rom.item_quantities_base_address + i
                        type_id = Rom.item_name_id[item_name]
                        amount = quantity + 1
                        snes_buffered_write(ctx, type_destination, bytes([type_id]))
                        snes_buffered_write(ctx, amount_destination, bytes([amount]))
                        snes_buffered_write(ctx, Rom.items_received_address, bytes([items_received_amount + 1]))
                        snes_logger.info('Received %s from %s (%s)' % (
                            item_name,
                            ctx.player_names[item.player],
                            ctx.location_names[item.location]))
                        break
        await snes_flush_writes(ctx)
