from BaseClasses import Region, Location, Item, ItemClassification, Tutorial, CollectionState
from worlds.AutoWorld import World, WebWorld 
#expand this eventually
from typing import *

from .Options import MCVOptions

json_world = {
    "regions": ["Menu", "main", "grass", "upper ice", "lava", "lower ice"],
    "region_map": {
        "Menu": {
            "main": None
        },
        "main": {
            "grass": "springboards OR double jump",
            "upper ice": ["double jump"],
        },
        "grass": {
            "lava": ["double jump", "dive"]
        },
        "upper ice": {
            "lower ice": ["key"]
        },
        
    },
    
    "location_map": {
        "main": {
            "Starting Medal": None, #east of start
            "Springboards": None, #gives springboards
            "Springboards Medal": ["double jump"],
        },

        "grass": {
            "Enter Crossprings": None,
            "Double Jump": None, #gives double jump
            "Cage Medal": ["key"],
        },

        "upper ice": {
            "Enter Upper Ice": None,
            "Dive": None,
        },

        "lava": {
            "Enter Lava": None,
            "Lava Medal": None,
            "Key": None,
        },
        "lower ice": {
            "Enter Lower Ice": None,
            "Ice Medal": None,
            "victory": ["dive"],
        },
    },
    "items": {
        "prog_items": [
            "double jump",
            "dive",
            "key",
        ],
        "useful_items": [
            "springboards",
        ],
        "filler_items": [
            "starting medal",
            "springboards medal",
            "lava medal",
            "cage medal",
            "ice medal",
            "counterfeit medal",
        ],
    },
    "base_id": 19828412012,
    "game_name": "MetroCUBEvania",
    "filler_name": "counterfeit medal"
}


class MCVItem(Item):
    game = json_world["game_name"]


class MCVLocation(Location):
    game = json_world["game_name"]


class MCVWeb(WebWorld):
    theme = "stone"
    """setup_en = Tutorial(
        "setup",
        "description here",
        "en",
        "docs/setup_en.md",
        "setup/en",
        ["Amazia", "Lucas Itskin", "Zachary Itskin", "Breven Hettinger"]
    )
    tutorials = [setup_en]"""


#flatten lists of locations and items so they are indexed for name_to_id
location_list = [location for locations in json_world["location_map"].values() for location in locations.keys()]
item_list = [item for item_lists in json_world["items"].values() for item in item_lists]

class MCVWorld(World):
    game = json_world["game_name"]
    #web = MCVWeb()
    options_dataclass = MCVOptions
    location_name_to_id = {name: json_world["base_id"]+location_list.index(name) for name in location_list}
    item_name_to_id = {name: json_world["base_id"]+item_list.index(name) for name in item_list}

#basic getters for json_world data, any option based modifications can be done here; may cache these later
#expect authors to modify the return of super() per options, or fully override if their format is different
    def get_region_list(self) -> List[str]:
        return json_world["regions"]

    def get_connections(self) -> "List[Tuple(str, str, Optional[Any])]":
        er = False
        if er:
            vanilla_connections = [(region1, region2, rule) for region1, connections in json_world["region_map"].items() for region2, rule in connections.items()]
            oneways = ["Menu -> main"]
            return_connections = vanilla_connections + [(region2, region1, rule) for connection in vanilla_connections for region1, region2, rule in connection if f"{region1} -> {region2}" not in oneways]
            # then create unconnected Entrances later
        else:
            return [(region1, region2, rule) for region1, connections in json_world["region_map"].items() for region2, rule in connections.items()]

    def get_location_map(self) -> "List[Tuple(str, str, Optional[Any])]":
        exclude = []
        if not self.options.extra_checks.value:
            exclude += ["Enter Crossprings", "Enter Upper Ice", "Enter Lava", "Enter Lower Ice"]
        return [(region, location, rule) for region, placements in json_world["location_map"].items() for location, rule in placements.items() if location not in exclude]

# black box methods
    def set_victory(self) -> None:
        #current black box to set and setup victory condition, run after all region/locations have been created (but currently before items)
        victory = self.multiworld.get_location("victory", self.player)
        victory.address = None
        victory.place_locked_item(MCVItem("victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("victory", self.player)
        #currently finds victory location, adds locked victory event, and requires victory event for completion

    def create_rule(self, rule: Any) -> Callable[[CollectionState], bool]:
        #current black box to convert json_world rule format to an access_rule lambda
        if rule == "springboards OR double jump":
            return lambda state: state.has_any(["springboards", "double jump"], self.player)
        return lambda state: state.has_all(rule, self.player)
        #currently all my rule objects are None or a list of required items

    def get_item_list(self) -> List[str]:
        #current black box to creat a list of item names per count that need to be created
        return [item for item in item_list if item not in ["counterfeit medal"]]
        #currently my items in my datapackage should all be created once, so this list functions

    def get_item_classification(self, name: str) -> ItemClassification:
        if name in json_world["items"]["prog_items"]:
            return ItemClassification.progression
        elif name in json_world["items"]["filler_items"]:
            if name in ["starting medal","springboards medal","lava medal","cage medal","ice medal"] and self.options.medal_hunt.value:
                return ItemClassification.progression
            return ItemClassification.filler
        else:
            return ItemClassification.useful

    def get_filler_item_name(self) -> str:
        #filler_name should be a list and this should choose with self.random
        return json_world["filler_name"]

# common methods
    def create_regions(self) -> None:
        #create a local map of get_region_list names to region object for referencing in create_regions and adding those regions to the multiworld
        regions = {region: None for region in self.get_region_list()}
        for region in regions.keys():
            regions[region] = Region(region, self.player, self.multiworld)
            self.multiworld.regions.append(regions[region])

        #TODO - add per option GER handling
        #loop through get_region_map, adding the rules per self.create_rule(rule) if present to the connections
        for region1, region2, rule in self.get_connections():
            if rule:
                regions[region1].connect(regions[region2], rule=self.create_rule(rule))
            else:
                regions[region1].connect(regions[region2])
        er = False
        if er:
            for region, connection, rule in self.get_er_entrances():
                cons = [regions[region].create_exit(connection), regions[region].create_en_target(connection)]
                for con in cons:
                    con.er_type = EntranceType.TWO_WAY
                    # con.er_group = 
                    con.access_rule = self.create_rule(rule)


        #loop through get_location_map, adding the rules per self.create_rule(rule) if present to the location
        for region, location, rule in self.get_location_map():
            loc = MCVLocation(self.player, location, self.location_name_to_id[location], regions[region])
            if rule:
                if location == "victory" and self.options.medal_hunt.value:
                    loc.access_rule = self.create_rule(rule+["starting medal","springboards medal","lava medal","cage medal","ice medal"])
                else:
                    loc.access_rule = self.create_rule(rule)
            regions[region].locations.append(loc)

        self.set_victory()

    def create_items(self) -> None:
        #create all items in get_item_list()
        itempool = []
        for item in self.get_item_list():
            itempool.append(self.create_item(item))

        #fill in any difference in itempool with filler item and submit to multiworld
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        while len(itempool) < total_locations:
            itempool.append(self.create_filler())
        self.multiworld.itempool += itempool
        early = self.multiworld.random.choice(["springboards", "double jump"])
        self.multiworld.early_items[self.player][early] = 1

    def create_item(self, name: str) -> "Item":
        item_class = self.get_item_classification(name)
        return MCVItem(name, item_class, self.item_name_to_id.get(name, None), self.player)

    def fill_slot_data(self):
        return {
        "ExtraChecks": self.options.extra_checks.value,
        "MedalHunt": self.options.medal_hunt.value,
        "ExtraCheckpoint": self.options.extra_checkpoint.value,
        "DeathLink": self.options.death_link.value,
        "DeathLink_Amnesty": self.options.death_link_amnesty.value,
        }
