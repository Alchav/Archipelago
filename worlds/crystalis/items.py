import logging

import orjson
from typing import Dict, List, Optional
import pkgutil
from BaseClasses import Item, ItemClassification, LocationProgressType
from .types import CrystalisItemData, CRYSTALIS_BASE_ID, convert_enum_to_item_classification, CrystalisItemCategoryEnum
from .locations import CrystalisLocation
from Fill import fast_fill


basic_key_names: List[str] = []
all_key_names: List[str] = []
basic_flute_names: List[str] = []
all_flute_names: List[str] = []
basic_lamp_names: List[str] = []
all_lamp_names: List[str] = []
basic_statue_names: List[str] = []
all_statue_names: List[str] = []
basic_bow_names: List[str] = []
all_bow_names: List[str] = []


def load_item_data_from_json() -> Dict[str, CrystalisItemData]:
    return orjson.loads(pkgutil.get_data(__name__, "data/items.json").decode("utf-8-sig"))


items_data_json = load_item_data_from_json()
items_data: Dict[str, CrystalisItemData] = {}
items_data_by_id: Dict[int, CrystalisItemData] = {}
# convert to actual type
for key, value in items_data_json.items():
    item_data = CrystalisItemData(value["name"], value["rom_id"], value["ap_id_offset"], value["unique"],
                                  value["losable"], value["prevent_loss"], value["community"], value["default_count"],
                                  value["groups"], value["palette"],  value["category"])
    items_data[key] = item_data
    items_data_by_id[item_data.ap_id_offset + CRYSTALIS_BASE_ID] = item_data
    if item_data.default_count == 0 and "Key Item" in item_data.groups:
        if "Key" in item_data.groups:
            all_key_names.append(item_data.name)
            if not item_data.community:
                basic_key_names.append(item_data.name)
        elif "Flute" in item_data.groups:
            all_flute_names.append(item_data.name)
            if not item_data.community:
                basic_flute_names.append(item_data.name)
        elif "Lamp" in item_data.groups:
            all_lamp_names.append(item_data.name)
            if not item_data.community:
                basic_lamp_names.append(item_data.name)
        elif "Statue" in item_data.groups:
            all_statue_names.append(item_data.name)
            if not item_data.community:
                basic_statue_names.append(item_data.name)
        elif "Bow" in item_data.groups:
            all_bow_names.append(item_data.name)
            if not item_data.community:
                basic_bow_names.append(item_data.name)


class CrystalisItem(Item):
    game: str = "Crystalis"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super(CrystalisItem, self).__init__(name, classification, code, player)


def unidentify_items(self) -> Dict[str, str]:
    keys: List[str] = []
    flutes: List[str] = []
    lamps: List[str] = []
    statues: List[str] = []
    bows: List[str] = []
    for item in items_data.values():
        if "Key" in item.groups and item.default_count > 0:
            keys.append(item.name)
        elif "Flute" in item.groups and item.default_count > 0:
            flutes.append(item.name)
        elif "Lamp" in item.groups and item.default_count > 0:
            lamps.append(item.name)
        elif "Statue" in item.groups and item.default_count > 0:
            statues.append(item.name)
        elif "Bow" in item.groups and item.default_count > 0:
            bows.append(item.name)
    all_key_items: List[str] = keys + flutes + lamps + statues + bows
    if not self.options.unidentified_key_items:
        return dict(zip(all_key_items, all_key_items))
    basic_key_options: List[str] = basic_key_names.copy()
    basic_flute_options: List[str] = basic_flute_names.copy()
    basic_lamp_options: List[str] = basic_lamp_names.copy()
    basic_statue_options: List[str] = basic_statue_names.copy()
    basic_bow_options: List[str] = basic_bow_names.copy()
    all_key_options: List[str] = all_key_names.copy()
    all_flute_options: List[str] = all_flute_names.copy()
    all_lamp_options: List[str] = all_lamp_names.copy()
    all_statue_options: List[str] = all_statue_names.copy()
    all_bow_options: List[str] = all_bow_names.copy()
    key_item_map: Dict[str, str] = {}
    for original_item_name, new_item_name in self.options.key_item_name_plando.value.items():
        key_item_map[original_item_name] = new_item_name
        if original_item_name in keys:
            keys.remove(original_item_name)
            all_key_options.remove(new_item_name)
            if new_item_name in basic_key_options:
                basic_key_options.remove(new_item_name)
        elif original_item_name in flutes:
            flutes.remove(original_item_name)
            all_flute_options.remove(new_item_name)
            if new_item_name in basic_flute_options:
                basic_flute_options.remove(new_item_name)
        elif original_item_name in lamps:
            lamps.remove(original_item_name)
            all_lamp_options.remove(new_item_name)
            if new_item_name in basic_lamp_options:
                basic_lamp_options.remove(new_item_name)
        elif original_item_name in statues:
            statues.remove(original_item_name)
            all_statue_options.remove(new_item_name)
            if new_item_name in basic_statue_options:
                basic_statue_options.remove(new_item_name)
        elif original_item_name in bows:
            bows.remove(original_item_name)
            all_bow_options.remove(new_item_name)
            if new_item_name in basic_bow_options:
                basic_bow_options.remove(new_item_name)
    # need to rebuild the overall list
    all_key_items = keys + flutes + lamps + statues + bows
    key_choices: List[str]
    flute_choices: List[str]
    lamp_choices: List[str]
    statue_choices: List[str]
    bow_choices: List[str]
    if self.options.no_community_jokes:
        key_choices = self.random.sample(basic_key_options, k=len(keys))
        flute_choices = self.random.sample(basic_flute_options, k=len(flutes))
        lamp_choices = self.random.sample(basic_lamp_options, k=len(lamps))
        statue_choices = self.random.sample(basic_statue_options, k=len(statues))
        bow_choices = self.random.sample(basic_bow_options, k=len(bows))
    else:
        key_choices = self.random.sample(all_key_options, k=len(keys))
        flute_choices = self.random.sample(all_flute_options, k=len(flutes))
        lamp_choices = self.random.sample(all_lamp_options, k=len(lamps))
        statue_choices = self.random.sample(all_statue_options, k=len(statues))
        bow_choices = self.random.sample(all_bow_options, k=len(bows))
    all_choices: List[str] = key_choices + flute_choices + lamp_choices + statue_choices + bow_choices
    return dict(zip(all_key_items, all_choices)) | key_item_map


def create_item(self, name: str) -> "Item":
    item_data: CrystalisItemData = items_data[name]
    actual_category: CrystalisItemCategoryEnum = item_data.category
    if actual_category == CrystalisItemCategoryEnum.CONDITIONAL:
        if "Upgrades" in item_data.groups[0]:
            actual_category = CrystalisItemCategoryEnum.USEFUL if self.options.orbs_not_required and \
                                                                  self.options.battle_magic_not_guaranteed and \
                                                                  not self.options.randomize_tradeins \
                                                                  else CrystalisItemCategoryEnum.PROGRESSION
        elif item_data.name == "Shield Ring":
            actual_category = CrystalisItemCategoryEnum.USEFUL if not self.options.barrier_not_guaranteed \
                                                                  else CrystalisItemCategoryEnum.PROGRESSION
        elif item_data.name == "Refresh":
            actual_category = CrystalisItemCategoryEnum.USEFUL if not self.options.barrier_not_guaranteed and \
                                                                  not self.options.gas_mask_not_guaranteed and \
                                                                  not self.options.guarantee_refresh \
                                                                  else CrystalisItemCategoryEnum.PROGRESSION
    return CrystalisItem(name, convert_enum_to_item_classification(actual_category), item_data.ap_id_offset +
                         CRYSTALIS_BASE_ID, self.player)


def create_items(self) -> None:
    non_unique_items = []
    items_created: int = 0
    swords: List[CrystalisItem] = []
    for item_data in items_data.values():
        if item_data.name in self.shuffle_data.key_item_names.keys():
            self.multiworld.itempool.append(self.create_item(self.shuffle_data.key_item_names[item_data.name]))
            items_created += 1
        elif "Sword" in item_data.groups:
            swords.append(self.create_item(item_data.name))
        elif self.options.dont_buff_bonus_items and item_data.name == "Hazmat Suit":
            self.multiworld.itempool.append(self.create_item("Gas Mask"))
            items_created += 1
        elif self.options.dont_buff_bonus_items and item_data.name == "Speed Boots":
            self.multiworld.itempool.append(self.create_item("Leather Boots"))
            items_created += 1
        elif not self.options.dont_shuffle_mimics or item_data.name != "Mimic":
            if self.options.keep_unique_items_and_consumables_separate and not item_data.unique:
                for i in range(item_data.default_count):
                    non_unique_items.append(self.create_item(item_data.name))
                    items_created += 1
            else:
                for i in range(item_data.default_count):
                    self.multiworld.itempool.append(self.create_item(item_data.name))
                    items_created += 1
    if self.options.guarantee_starting_sword:
        fixed_sword = self.random.choice(swords)
        swords.remove(fixed_sword)
        # technically stand-alone doesn't do this... but I think it fits the spirit of the flag
        if self.options.shuffle_areas or self.options.shuffle_houses:
            mezame_left_location = self.get_location("Mezame Left Chest")
            mezame_left_location.place_locked_item(fixed_sword)
        else:
            leaf_elder_location = self.get_location("Leaf Elder")
            leaf_elder_location.place_locked_item(fixed_sword)
    # put the three or four swords in the itempool
    for sword in swords:
        self.multiworld.itempool.append(sword)
        items_created += 1
    locations_count = len([location for location in self.multiworld.get_locations(self.player)
                               if location.address is not None and location.item is None])
    if items_created < locations_count:
        logging.debug(f"Crystalis: Fewer items ({items_created}) than empty locations ({locations_count}).")
        logging.debug(f"Crystalis: creating {locations_count - items_created} extra Medical Herbs.")
        if self.options.keep_unique_items_and_consumables_separate:
            for i in range(locations_count - items_created):
                non_unique_items.append(self.create_item("Medical Herb"))
        else:
            for i in range(locations_count - items_created):
                self.multiworld.itempool.append(self.create_item("Medical Herb"))
    elif locations_count < items_created:
        raise Exception(f"Too many items ({items_created}) for the number of available locations ({locations_count}).")

    if self.options.keep_unique_items_and_consumables_separate:
        # fill non-unique locations with non-unique items
        non_unique_locations: List[CrystalisLocation] = []
        for location_data in self.locations_data:
            if not location_data.unique and (not self.options.dont_shuffle_mimics or "Mimic" not in location_data.name):
                non_unique_location = self.get_location(location_data.name)
                if non_unique_location.item is None:
                    non_unique_locations.append(non_unique_location)

        self.random.shuffle(non_unique_items)
        # Dear Core Maintainers: if you are looking at this code in the future because you're trying to kill fast_fill,
        # don't let this stop you; just ping @Ars-Ignis on GitHub or @CodeGorilla on Discord and I'll replace this
        remaining_items, remaining_locations = fast_fill(self.multiworld, non_unique_items, non_unique_locations)
        if len(remaining_locations) > 0:
            logging.warning("More non-unique locations than items; excluding remaining locations")
            logging.warning("Please report this to the Crystalis world maintainer, CodeGorilla")
            for remaining_location in remaining_locations:
                remaining_location.progress_type = LocationProgressType.EXCLUDED
        if len(remaining_items) > 0:
            logging.debug("More non-unique items than locations. This is expected. Adding the rest to the item pool.")
            self.multiworld.itempool += remaining_items
            for non_unique_location in non_unique_locations:
                non_unique_location.locked = True
