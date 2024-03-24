import struct
from .Options import KirbyFlavorPreset, GooeyFlavorPreset

kirby_flavor_presets = {
    1: {
      "1": "B50029",
      "2": "FF91C6",
      "3": "B0123B",
      "4": "630F0F",
      "5": "D60052",
      "6": "DE4873",
      "7": "D07880",
      "8": "000000",
      "9": "F770A5",
      "10": "E01784",
      "11": "CA4C74",
      "12": "A7443F",
      "13": "FF1784",
      "14": "FFA1DE",
      "15": "B03830",
    },
    2: {
      "1": "C70057",
      "2": "FF3554",
      "3": "AA0040",
      "4": "C02D47",
      "5": "E02068",
      "6": "C2183F",
      "7": "D03F80",
      "8": "872939",
      "9": "E82B47",
      "10": "E80067",
      "11": "D52F40",
      "12": "9F1C33",
      "13": "FD187F",
      "14": "F85068",
      "15": "D2386F",
    },
    3: {
        "1": "5858e2",
        "2": "e6e6fa",
        "3": "bcbcf2",
        "4": "8484e6",
        "5": "2929ec",
        "6": "b5b5f0",
        "7": "847bd6",
        "8": "3232d6",
        "9": "d6d6ef",
        "10": "4a52ef",
        "11": "c6c6e6",
        "12": "4343ad",
        "13": "6767ff",
        "14": "f6f6fd",
        "15": "3139b6",
    },
    4: {
        "1": "B01810",
        "2": "F0E08D",
        "3": "C8A060",
        "4": "A87043",
        "5": "E03700",
        "6": "EFC063",
        "7": "D07818",
        "8": "A8501C",
        "9": "E8D070",
        "10": "E2501E",
        "11": "E8C55C",
        "12": "B08833",
        "13": "E8783B",
        "14": "F8F8A5",
        "15": "B03800",
    },
    5: {
        "1": "9F4410",
        "2": "88F27B",
        "3": "57A044",
        "4": "227029",
        "5": "C75418",
        "6": "57BA23",
        "7": "1C6B00",
        "8": "2D6823",
        "9": "3FD744",
        "10": "E06C16",
        "11": "54C053",
        "12": "1A541E",
        "13": "F06B10",
        "14": "98F89A",
        "15": "B05830",
    },
    6: {
        "1": "7C1060",
        "2": "CA8AE8",
        "3": "8250A5",
        "4": "604B7B",
        "5": "A52068",
        "6": "8D64B8",
        "7": "B73B80",
        "8": "672D9A",
        "9": "BA82D5",
        "10": "B55098",
        "11": "9F5CCF",
        "12": "632B74",
        "13": "CF78B5",
        "14": "DA98F8",
        "15": "8D3863",
    },
    7: {
        "1": "6F1410",
        "2": "C2735C",
        "3": "5C351C",
        "4": "875440",
        "5": "9F2F0C",
        "6": "874C3B",
        "7": "88534C",
        "8": "4C1E00",
        "9": "B06458",
        "10": "921C16",
        "11": "9F5C54",
        "12": "5B3125",
        "13": "C01A14",
        "14": "CF785B",
        "15": "6B3125",
    },
    8: {
        "1": "a6a6a6",
        "2": "e6e6e6",
        "3": "bcbcbc",
        "4": "848484",
        "5": "909090",
        "6": "b5b5b5",
        "7": "848484",
        "8": "646464",
        "9": "d6d6d6",
        "10": "525252",
        "11": "c6c6c6",
        "12": "737373",
        "13": "949494",
        "14": "f6f6f6",
        "15": "545454",
    },
    9: {
        "1": "400000",
        "2": "6B6B6B",
        "3": "2B2B2B",
        "4": "181818",
        "5": "640000",
        "6": "3D3D3D",
        "7": "878787",
        "8": "020202",
        "9": "606060",
        "10": "980000",
        "11": "505050",
        "12": "474747",
        "13": "C80000",
        "14": "808080",
        "15": "AF0000",
    },
    10: {
        "1": "2B4B10",
        "2": "EF8A9D",
        "3": "C84F6B",
        "4": "B74F54",
        "5": "126018",
        "6": "D85F6F",
        "7": "D06870",
        "8": "A24858",
        "9": "E77B8D",
        "10": "168025",
        "11": "DF5C68",
        "12": "9D4353",
        "13": "48953F",
        "14": "F897AD",
        "15": "B03830",
    },
    11: {
        "1": "7B290C",
        "2": "FF9A00",
        "3": "B05C1C",
        "4": "8F3F0E",
        "5": "D23B0C",
        "6": "E08200",
        "7": "D05800",
        "8": "8A2B16",
        "9": "EF970A",
        "10": "E24800",
        "11": "E58F00",
        "12": "A03700",
        "13": "ED3B00",
        "14": "FFAF27",
        "15": "A84700",
    },
    12: {
        "1": "AFA810",
        "2": "4FF29D",
        "3": "2BA04C",
        "4": "007043",
        "5": "C7C218",
        "6": "33BA5F",
        "7": "006B40",
        "8": "2D6823",
        "9": "1CD773",
        "10": "E0CF16",
        "11": "2DC06C",
        "12": "00543F",
        "13": "F0F010",
        "14": "43F8B2",
        "15": "B0A230",
    },
    13: {
        "1": "7C73B0",
        "2": "CACAE7",
        "3": "7B7BA8",
        "4": "5F5FA7",
        "5": "B57EDC",
        "6": "8585C5",
        "7": "5B5B82",
        "8": "474796",
        "9": "B2B2D8",
        "10": "B790EF",
        "11": "9898C2",
        "12": "6B6BB7",
        "13": "CDADFA",
        "14": "E6E6FA",
        "15": "976FBD",
    },
}

gooey_flavor_presets = {
    1: {
        "1": "CD539D",
        "2": "D270AD",
        "3": "F27CBF",
        "4": "FF91C6",
        "5": "FFA1DE",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    2: {
        "1": "161600",
        "2": "592910",
        "3": "5A3118",
        "4": "AB3918",
        "5": "EB3918",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    3: {
        "1": "001616",
        "2": "102959",
        "3": "18315A",
        "4": "1839AB",
        "5": "1839EB",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    4: {
        "1": "C8A031",
        "2": "C5BD38",
        "3": "D2CD48",
        "4": "E2E040",
        "5": "EAE2A0",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    5: {
        "1": "54A208",
        "2": "5CB021",
        "3": "6CB206",
        "4": "8AC54C",
        "5": "8DD554",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    6: {
        "1": "3D083D",
        "2": "4B024B",
        "3": "4C104C",
        "4": "5F0A5F",
        "5": "9F1D9F",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    7: {
        "1": "270C08",
        "2": "481C10",
        "3": "581E10",
        "4": "5B2712",
        "5": "743316",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    8: {
        "1": "7F7F7F",
        "2": "909090",
        "3": "9D9D9D",
        "4": "BFBFBF",
        "5": "D2D2D2",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    9: {
        "1": "141414",
        "2": "2D2D2D",
        "3": "404040",
        "4": "585858",
        "5": "7F7F7F",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    10: {
        "1": "954353",
        "2": "AF4F68",
        "3": "CD6073",
        "4": "E06774",
        "5": "E587A2",
        "6": "17AF10",
        "7": "4FE748",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    11: {
        "1": "CF4700",
        "2": "D85C08",
        "3": "E26C04",
        "4": "EA7B16",
        "5": "EF8506",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    12: {
        "1": "1C4708",
        "2": "105B1C",
        "3": "186827",
        "4": "187C3B",
        "5": "188831",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
    13: {
        "1": "501E70",
        "2": "673B87",
        "3": "7848A7",
        "4": "9067C7",
        "5": "B57EDC",
        "6": "B51810",
        "7": "EF524A",
        "8": "D6C6C6",
        "9": "FFFFFF",
    },
}

kirby_target_palettes = {
    0x64646: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 1),
    0x64846: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 1),
    0x1E007E: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 1),
    0x1E009C: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 0.5),
    0x1E00F6: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 1),
    0x1E0114: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 0.5),
    0x1E0216: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 1),
    0x1E0234: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 0.5),
    0x1E0486: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 1),
    0x1E04A4: (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], 0, 0.5),
}

gooey_target_palettes = {
    0x604C2: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x64592: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x64692: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x64892: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x1E02CA: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x1E0342: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x1E05A6: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x1E05B8: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 0.5),
    0x1E0636: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1),
    0x1E065A: (["1", "2", "3", "4", "5", "6", "7", "8", "9"], 0, 1.5),
}


def get_kirby_palette(world):
    palette = world.options.kirby_flavor_preset.value
    if palette == KirbyFlavorPreset.option_custom:
        return world.options.kirby_flavor.value
    return kirby_flavor_presets.get(palette, None)


def get_gooey_palette(world):
    palette = world.options.gooey_flavor_preset.value
    if palette == GooeyFlavorPreset.option_custom:
        return world.options.gooey_flavor.value
    return gooey_flavor_presets.get(palette, None)


def rgb888_to_bgr555(red, green, blue) -> bytes:
    red = red >> 3
    green = green >> 3
    blue = blue >> 3
    outcol = (blue << 10) + (green << 5) + red
    return struct.pack("H", outcol)


def get_palette_bytes(palette, target, offset, factor):
    output_data = bytearray()
    for color in target:
        hexcol = palette[color]
        if hexcol.startswith("#"):
            hexcol = hexcol.replace("#", "")
        colint = int(hexcol, 16)
        col = ((colint & 0xFF0000) >> 16, (colint & 0xFF00) >> 8, colint & 0xFF)
        col = tuple(int(int(factor*x) + offset) for x in col)
        byte_data = rgb888_to_bgr555(col[0], col[1], col[2])
        output_data.extend(bytearray(byte_data))
    return output_data
