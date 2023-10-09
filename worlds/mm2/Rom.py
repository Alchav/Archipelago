import pkgutil
from typing import Optional
import hashlib
import Utils
import os
from BaseClasses import MultiWorld
from worlds.Files import APDeltaPatch
from . import Names
from .Text import MM2TextEntry, get_colors_for_item

MM2LCHASH = "19de63834393b5988d41441f83a36df5"
PROTEUSHASH = "9ff045a3ca30018b6e874c749abb3ec4"
MM2NESHASH = "302761a666ac89c21f185052d02127d3"
MM2VCHASH = "77b51417eb66e8119c85689a093be857"


class RomData:
    def __init__(self, file: bytes, name: str = None):
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset):
        return self.file[offset]

    def read_bytes(self, offset, length):
        return self.file[offset:offset + length]

    def write_byte(self, offset, value):
        self.file[offset] = value

    def write_bytes(self, offset, values):
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)


def patch_rom(multiworld: MultiWorld, player: int, rom: RomData):
    rom.write_byte(0x3403C, 0x8A)  # Read for setting robot master face tiles
    rom.write_byte(0x34083, 0x8A)  # Read for setting robot master face sprites
    rom.write_bytes(0x340DD, [0x9B, 0xC9, 0x07])  # Dr. Wily checking for Items
    rom.write_byte(0x340ED, 0x8A)  # Check for allowing access to stage
    rom.write_bytes(0x3806C, [0xFF, 0x85, 0x8A])  # initialize starting robot master
    rom.write_bytes(0x38076, [0xA9, 0x00])  # Block auto-Wily
    rom.write_bytes(0x3C264, [0xA9, 0x00])  # Block auto-Wily
    rom.write_bytes(0x3C24D, [0x8B, 0x85, 0x8B])  # Write stage completion to $8B
    rom.write_bytes(0x3C254, [0x8C, 0x85, 0x8C])  # Write item checks to $8C
    rom.write_bytes(0x3C1CC, [0xEA, 0xEA])  # Remove e-tank loss on game over
    rom.write_bytes(0x36325, [0xEA, 0xEA, 0xEA, 0xEA])  # Remove weapon loss on startup

    # Store Wily Progress, and stage completion
    rom.write_bytes(0x37B18, [0x20, 0x2F, 0xF4,
                              0xEA,
                              ])
    rom.write_bytes(0x340E2, [0x20, 0x80, 0xF3, 0xEA, ])
    rom.write_bytes(0x3C271, [0x20, 0xA0, 0xF3, 0xEA, ])
    rom.write_bytes(0x3F390, [0xA5, 0x23,
                              0xC9, 0x0C,
                              0xF0, 0x04,
                              0xA5, 0x8D,
                              0xD0, 0x02,
                              0xA9, 0x08,
                              0x85, 0x2A,
                              0x60,
                              ])
    rom.write_bytes(0x3F3B0, [0xA9, 0x01,
                              0x9D, 0x70, 0x0F,
                              0xE6, 0x2A,
                              0xA5, 0x2A,
                              0x85, 0x8D,
                              0x60,
                              ])
    rom.write_bytes(0x3F43F, [0x85, 0x2A,
                              0x8A,
                              0x48,
                              0xA6, 0x2A,
                              0xA9, 0x01,
                              0x9D, 0x70, 0x0F,
                              0x68,
                              0xAA,
                              0xA9, 0x17,
                              0x60,
                              ])
    # Deathlink and Soft-reset Kill
    rom.write_bytes(0x3C11E, [0x27, 0xF5])
    rom.write_bytes(0x38188, [0x20, 0x8F, 0xF3, 0xEA, ])
    rom.write_bytes(0x3E5BC, [0x85, 0x8F, 0xEA, ])  # null deathlink on death
    rom.write_bytes(0x3F39F, [0xA5, 0x23,
                              0xC9, 0x0F,
                              0xD0, 0x03,
                              0x4C, 0xA8, 0xE5,
                              0x4C, 0x1A, 0xF5,
                              0x60, ])
    rom.write_bytes(0x3F52A, [0xA5, 0x8F,
                              0xC9, 0x01,
                              0xD0, 0x03,
                              0x4C, 0xA8, 0xE5,
                              0x4C, 0xBB, 0xF3,
                              0x60, ])
    rom.write_bytes(0x3F537, [0x20, 0x51, 0xC0,
                              0xA9, 0x00,
                              0x8D, 0xC0, 0x06,
                              0x60, ])
    rom.write_bytes(0x3F3CB, [
                                  0xA5, 0x27,
                                  0x29, 0x08,
                                  0x60,
                                  0xEA,
                                  0xEA, ])

    # text writing
    # write our font
    font = pkgutil.get_data(__name__, os.path.join("data", "mm2font.bin"))
    rom.write_bytes(0x20410, font)
    rom.write_bytes(0x3F540, [
        0x84, 0x00, 0x0A, 0x0A, 0x0A, 0x0A, 0xA8, 0xA5, 0xCB, 0x69, 0x00, 0x85, 0xC8, 0xA9, 0x40, 0x85,
        0xC9, 0xA9, 0xF6, 0x18, 0x65, 0xC8, 0x85, 0xCA, 0xB1, 0xC9, 0x8D, 0xB6, 0x03, 0x98, 0x18, 0x69,
        0x01, 0xA8, 0xA5, 0xCA, 0x69, 0x00, 0x85, 0xCA, 0xB1, 0xC9, 0x8D, 0xB7, 0x03, 0x98, 0x18, 0x69,
        0x01, 0xA8, 0xA5, 0xCA, 0x69, 0x00, 0x85, 0xCA, 0x84, 0xFE, 0xA9, 0x0E, 0x85, 0xFD, 0x20, 0x34,
        0xBD, 0xA4, 0xFE, 0xC0, 0xF7, 0xD0, 0x05, 0xAD, 0x20, 0x04, 0xD0, 0x02, 0xB1, 0xC9, 0x8D, 0xB8,
        0x03, 0xE6, 0x47, 0xEE, 0xB7, 0x03, 0xA5, 0xFE, 0x18, 0x69, 0x01, 0x85, 0xFE, 0xA5, 0xCA, 0x69,
        0x00, 0x85, 0xCA, 0xC6, 0xFD, 0xD0, 0xD7, 0xA4, 0x00, 0x20, 0xAB, 0xC0, 0x60, 0xA5, 0x2A, 0xA2,
        0x00, 0xB0, 0x02, 0xA2, 0x02, 0x86, 0xCB, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0x0A, 0x0A, 0x48, 0x38,
        0x20, 0x30, 0xF5, 0x68, 0x69, 0x00, 0x48, 0x38, 0x20, 0x30, 0xF5, 0x68, 0x69, 0x00, 0x48, 0x38,
        0x20, 0x30, 0xF5, 0xA9, 0x00, 0x38, 0x20, 0x3E, 0xBD, 0x68, 0x69, 0x00, 0x38, 0x20, 0x30, 0xF5,
        0x60, 0xA9, 0x7D, 0x85, 0xFD, 0xAD, 0x20, 0x04, 0x29, 0x0F, 0x0A, 0x38, 0x69, 0x18, 0x85, 0xFF,
        0x60,
    ])
    rom.write_bytes(0x37B84, [0x20, 0x9D, 0xF5,
                              0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])
    rom.write_bytes(0x37D02, [0x07, 0x20, 0xA3, 0xF5, ])  # items text
    rom.write_bytes(0x37D06, [0x20, 0xD1, 0xF5, 0xEA, 0xA6, 0xFF, ])  # items color special casing
    rom.write_bytes(0x37E2A, MM2TextEntry("FOR           ", 0xCB).resolve())
    rom.write_bytes(0x37EAA, MM2TextEntry("GET EQUIPPED  ", 0x0B).resolve())
    rom.write_bytes(0x37EBA, MM2TextEntry("WITH          ", 0x2B).resolve())

    base_address = 0x3F650
    color_address = 0x37F6C
    for i, location in zip(range(11), [
        Names.atomic_fire_get,
        Names.air_shooter_get,
        Names.leaf_shield_get,
        Names.bubble_lead_get,
        Names.time_stopper_get,
        Names.quick_boomerang_get,
        Names.metal_blade_get,
        Names.crash_bomber_get,
        Names.item_1_get,
        Names.item_2_get,
        Names.item_3_get
    ]):
        item = multiworld.get_location(location, player).item
        if len(item.name) <= 14:
            # we want to just place it in the center
            first_str = ""
            second_str = item.name
            third_str = ""
        elif len(item.name) <= 28:
            # spread across second and third
            first_str = ""
            second_str = item.name[:14]
            third_str = item.name[14:]
        else:
            # all three
            first_str = item.name[:14]
            second_str = item.name[14:28]
            third_str = item.name[28:]
            if len(third_str) > 16:
                third_str = third_str[:16]
        player_str = multiworld.get_player_name(item.player)
        if len(player_str) > 14:
            player_str = player_str[:14]
        rom.write_bytes(base_address + (64 * i), MM2TextEntry(first_str, 0x4B).resolve())
        rom.write_bytes(base_address + (64 * i) + 16, MM2TextEntry(second_str, 0x6B).resolve())
        rom.write_bytes(base_address + (64 * i) + 32, MM2TextEntry(third_str, 0x8B).resolve())
        rom.write_bytes(base_address + (64 * i) + 48, MM2TextEntry(player_str, 0xEB).resolve())

        colors = get_colors_for_item(item.name)
        if i > 7:
            rom.write_bytes(color_address + 27 + ((i - 7) * 2), colors)
        else:
            rom.write_bytes(color_address + (i * 2), colors)




    if multiworld.quickswap[player]:
        rom.write_bytes(0x3F533, [0x4C, 0xAC, 0xF3, ])  # add jump to check for holding select
        rom.write_bytes(0x3F3BC, [0xA5, 0x27,
                                  0x29, 0x04,
                                  0xF0, 0x09,
                                  0xA6, 0xA9,
                                  0xD0, 0x02,
                                  0xA2, 0x00,
                                  0x4C, 0xC0, 0xF3,
                                  ])
        rom.write_bytes(0x3F3D0, [
            0x98,
            0x48,
            0xA6, 0xA9,
            0xE8,
            0xE0, 0x09,
            0x10, 0x1F,
            0xA9, 0x01,
            0xCA,
            0xF0, 0x05,
            0x0A,
            0xE0, 0x00,
            0xD0, 0xF8,
            0xA6, 0xA9,
            0xE8,
            0x48,
            0x25, 0x9A,
            0xD0, 0x09,
            0x68,
            0xE8,
            0xE0, 0x09,
            0x10, 0x07,
            0x0A,
            0xD0, 0xF2,
            0x68,
            0x38,
            0xB0, 0x20,
            0x8A,
            0x48,
            0x38,
            0xE9, 0x08,
            0xAA,
            0xA9, 0x01,
            0xCA,
            0xF0, 0x05,
            0x0A,
            0xE0, 0x00,
            0xD0, 0xF8,
            0xA8,
            0x68,
            0xAA,
            0x98,
            0x48,
            0x25, 0x9B,
            0xD0, 0xE3,
            0x68,
            0xE8,
            0x0A,
            0xD0, 0xF6,
            0xA2, 0x00,
            0xA9, 0x0D,
            0x20, 0x00, 0xC0,
            0xA5, 0xB5,
            0x48,
            0xA5, 0xB6,
            0x48,
            0xA5, 0xB7,
            0x48,
            0xA5, 0xB8,
            0x48,
            0xA5, 0xB9,
            0x48,
            0xA5, 0x20,
            0x48,
            0xA5, 0x1F,
            0x48,
            0x20, 0x40, 0xF4,
            0xA9, 0x0E,
            0x20, 0x00, 0xC0,
            0x68,
            0xA8,
            0x60,
        ])
        rom.write_bytes(0x3F450, [0x68,
                                  0x8D, 0xFE, 0x0F,
                                  0x68,
                                  0x8D, 0xFF, 0x0F,
                                  0x86, 0xA9,
                                  0x20, 0x6C, 0xCC,
                                  0xA5, 0x1A,
                                  0x48,
                                  0xA2, 0x00,
                                  0x86, 0xFD,
                                  0x18,
                                  0xA5, 0x52,
                                  0x7D, 0x7F, 0x95,
                                  0x85, 0x08,
                                  0xA5, 0x53,
                                  0x69, 0x00,
                                  0x85, 0x09,
                                  0xA5, 0x08,
                                  0x46, 0x09,
                                  0x6A,
                                  0x46, 0x09,
                                  0x6A,
                                  0x85, 0x08,
                                  0x29, 0x3F,
                                  0x85, 0x1A,
                                  0x18,
                                  0xA5, 0x09,
                                  0x69, 0x85,
                                  0x85, 0x09,
                                  0xA9, 0x00,
                                  0x85, 0x1B,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xA5, 0xFD,
                                  0xC9, 0x08,
                                  0xB0, 0x12,
                                  0xA6, 0xA9,
                                  0xBD, 0x64, 0x96,
                                  0xA8,
                                  0xE0, 0x09,
                                  0x90, 0x04,
                                  0xA2, 0x00,
                                  0xF0, 0x08,
                                  0xA2, 0x05,
                                  0xD0, 0x04,
                                  0xA0, 0x90,
                                  0xA2, 0x00,
                                  0x20, 0x60, 0xC7,
                                  0x20, 0xAB, 0xC0,
                                  0xA6, 0xFD,
                                  0xE8,
                                  0xE0, 0x0F,
                                  0xD0, 0xAB,
                                  0x86, 0xFD,
                                  0xA0, 0x90,
                                  0xA2, 0x00,
                                  0x20, 0x60, 0xC7,
                                  0x20, 0xED, 0xD2,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0x68,
                                  0x85, 0x1A,
                                  0xA5, 0x2A,
                                  0xC9, 0x0A,
                                  0xD0, 0x18,
                                  0xA5, 0xB1,
                                  0xF0, 0x14,
                                  0xA2, 0x02,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xCA,
                                  0x10, 0xEE,
                                  0xA2, 0x11,
                                  0xBD, 0x00, 0x07,
                                  0xEA,
                                  0xEA,
                                  0xEA,
                                  0xCA,
                                  0x10, 0xF7,
                                  0x68,
                                  0x85, 0x1F,
                                  0x68,
                                  0x85, 0x20,
                                  0x68,
                                  0x85, 0xB9,
                                  0x68,
                                  0x85, 0xB8,
                                  0x68,
                                  0x85, 0xB7,
                                  0x68,
                                  0x85, 0xB6,
                                  0x68,
                                  0x85, 0xB5,
                                  0xA9, 0x00,
                                  0x85, 0xAC,
                                  0x85, 0x2C,
                                  0x8D, 0x80, 0x06,
                                  0x8D, 0xA0, 0x06,
                                  0xA9, 0x1A,
                                  0x8D, 0x00, 0x04,
                                  0xA9, 0x03,
                                  0x85, 0xAA,
                                  0xA9, 0x30,
                                  0x20, 0x51, 0xC0,
                                  0xAD, 0xFF, 0x0F,
                                  0x48,
                                  0xAD, 0xFE, 0x0F,
                                  0x48,
                                  0x60,
                                  ])

    if multiworld.consumables[player]:
        rom.write_bytes(0x3E5F8, [0x20, 0x00, 0xF3])  # jump to our handler for consumable checks
        rom.write_bytes(0x3F310, [0x99, 0x40, 0x01,
                                  0x8A,
                                  0x48,
                                  0xA5, 0xAD,
                                  0xC9, 0x7C,
                                  0x10, 0x02,
                                  0xA9, 0x00,
                                  0x85, 0xAD,
                                  0xA5, 0x2A,
                                  0x0A,
                                  0x0A,
                                  0xAA,
                                  0x98,
                                  0xC9, 0x08,
                                  0x30, 0x05,
                                  0xE8,
                                  0xE9, 0x08,
                                  0xD0, 0xF7,
                                  0xA8,
                                  0xA9, 0x01,
                                  0xC0, 0x00,
                                  0xF0, 0x04,
                                  0x0A,
                                  0x88,
                                  0xD0, 0xF8,
                                  0x1D, 0x80, 0x0F,
                                  0x9D, 0x80, 0x0F,
                                  0x68,
                                  0xAA,
                                  0x60,
                                  ])

    # weapon palette randomization
    # 0xD304 palettes start

    from Utils import __version__
    rom.name = bytearray(f'MM2{__version__.replace(".", "")[0:3]}_{player}_{multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x3FFC0, rom.name)


class MM2DeltaPatch(APDeltaPatch):
    hash = [MM2LCHASH]
    game = "Mega Man 2"
    patch_file_ending = ".apmm2"
    result_file_ending = ".nes"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name: str = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() == PROTEUSHASH:
            base_rom_bytes = extract_mm2(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM2LCHASH, MM2NESHASH, MM2VCHASH}:
            print(basemd5.hexdigest())
            raise Exception("Supplied Base Rom does not match known MD5 for US, LC, or US VC release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["mm2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


header = b'\x4E\x45\x53\x1A\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
prg_offset = 0x8ED70
prg_size = 0x40000


def extract_mm2(proteus: bytes) -> bytes:
    mm2 = bytearray(header)
    mm2.extend(proteus[prg_offset:prg_offset+prg_size])
    return bytes(mm2)
