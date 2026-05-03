from __future__ import annotations

from typing import Collection

from Utils import snes_to_pc


MAX_GRAPHICS_COMMAND_LENGTH = 1024
SHORT_GRAPHICS_COMMAND_LENGTH = 32
GRAPHICS_TERMINATOR = 0xFF

SPRITE_GRAPHICS_POINTER_BANK_TABLE = 0x4FF3
SPRITE_GRAPHICS_POINTER_HIGH_TABLE = 0x50D2
SPRITE_GRAPHICS_POINTER_LOW_TABLE = 0x51B1

BOSS_PRIZE_CRYSTAL_GRAPHICS_PACK = 0x9C
BOSS_PRIZE_CRYSTAL_ANIMATED_ITEM_OFFSET = 0x0678
ANIMATED_ITEM_HIGH_PACK_OFFSET = 0x0600
ANIMATED_ITEM_ROW_STRIDE = 0x0180
THREE_BPP_TILE_SIZE = 0x18

BOSS_PRIZE_CRYSTAL_SHEET_OFFSET = BOSS_PRIZE_CRYSTAL_ANIMATED_ITEM_OFFSET - ANIMATED_ITEM_HIGH_PACK_OFFSET
BOSS_PRIZE_CRYSTAL_TILE_OFFSETS = (
    BOSS_PRIZE_CRYSTAL_SHEET_OFFSET,
    BOSS_PRIZE_CRYSTAL_SHEET_OFFSET + THREE_BPP_TILE_SIZE,
    BOSS_PRIZE_CRYSTAL_SHEET_OFFSET + ANIMATED_ITEM_ROW_STRIDE,
    BOSS_PRIZE_CRYSTAL_SHEET_OFFSET + ANIMATED_ITEM_ROW_STRIDE + THREE_BPP_TILE_SIZE,
)

# The shuffled-prize crystal is the 16x16 graphic in sprite pack $9C.
# It is converted through Do3To4HighAnimated, so nonzero 3bpp pixels use the
# normally loaded upper-half sprite palette colors.
BOSS_PRIZE_CRYSTAL_COLOR_REMAP = {
    # 1: 1,  # white -> white
    # 3: 3,  # dark blue -> SP2 dark blue
    # 4: 4,  # blue -> SP2 light blue
    # 5: 6,  # light blue -> SP2 pale blue
    6: 1,
    7: 4
}


def _emit_graphics_command(out: bytearray, command: int, length: int, payload: bytes) -> None:
    if not 1 <= length <= MAX_GRAPHICS_COMMAND_LENGTH:
        raise ValueError(f"invalid graphics command length {length}")

    if length <= SHORT_GRAPHICS_COMMAND_LENGTH:
        out.append((command << 5) | (length - 1))
    else:
        out.append(0xE0 | (command << 2) | ((length - 1) >> 8))
        out.append((length - 1) & 0xFF)

    out.extend(payload)


def decompress_graphics(data: bytes) -> bytes:
    decompressed, _ = decompress_graphics_with_size(data)
    return decompressed


def decompress_graphics_with_size(data: bytes) -> tuple[bytes, int]:
    out = bytearray()
    index = 0

    while True:
        command_byte = data[index]
        index += 1

        if command_byte == GRAPHICS_TERMINATOR:
            return bytes(out), index

        if (command_byte & 0xE0) == 0xE0:
            command = (command_byte >> 2) & 0x07
            length = (((command_byte & 0x03) << 8) | data[index]) + 1
            index += 1
        else:
            command = (command_byte >> 5) & 0x07
            length = (command_byte & 0x1F) + 1

        if command == 0:
            out.extend(data[index:index + length])
            index += length
        elif command == 1:
            out.extend([data[index]] * length)
            index += 1
        elif command == 2:
            first = data[index]
            second = data[index + 1]
            index += 2
            for offset in range(length):
                out.append(first if offset % 2 == 0 else second)
        elif command == 3:
            value = data[index]
            index += 1
            for _ in range(length):
                out.append(value)
                value = (value + 1) & 0xFF
        else:
            offset = data[index] | (data[index + 1] << 8)
            index += 2
            for _ in range(length):
                out.append(out[offset])
                offset += 1


def compress_graphics(data: bytes) -> bytes:
    out = bytearray()
    literal = bytearray()
    index = 0

    def flush_literal() -> None:
        nonlocal literal
        while literal:
            length = min(len(literal), MAX_GRAPHICS_COMMAND_LENGTH)
            _emit_graphics_command(out, 0, length, bytes(literal[:length]))
            del literal[:length]

    while index < len(data):
        best_command: tuple[int, int, bytes] | None = None
        best_savings = 0
        max_length = min(MAX_GRAPHICS_COMMAND_LENGTH, len(data) - index)

        repeated_length = 1
        while repeated_length < max_length and data[index + repeated_length] == data[index]:
            repeated_length += 1
        if repeated_length >= 2:
            best_command = (1, repeated_length, bytes([data[index]]))
            best_savings = repeated_length - (2 if repeated_length <= SHORT_GRAPHICS_COMMAND_LENGTH else 3)

        if index + 1 < len(data):
            first = data[index]
            second = data[index + 1]
            alternating_length = 0
            while alternating_length < max_length:
                expected = first if alternating_length % 2 == 0 else second
                if data[index + alternating_length] != expected:
                    break
                alternating_length += 1
            if alternating_length >= 4:
                savings = alternating_length - (3 if alternating_length <= SHORT_GRAPHICS_COMMAND_LENGTH else 4)
                if savings > best_savings:
                    best_command = (2, alternating_length, bytes([first, second]))
                    best_savings = savings

        incrementing_length = 1
        start_value = data[index]
        while (
            incrementing_length < max_length
            and data[index + incrementing_length] == ((start_value + incrementing_length) & 0xFF)
        ):
            incrementing_length += 1
        if incrementing_length >= 3:
            savings = incrementing_length - (2 if incrementing_length <= SHORT_GRAPHICS_COMMAND_LENGTH else 3)
            if savings > best_savings:
                best_command = (3, incrementing_length, bytes([start_value]))
                best_savings = savings

        copy_length = 0
        copy_offset = 0
        for offset in range(index):
            if data[offset] != data[index]:
                continue
            length = 1
            while length < max_length and offset + length < index and data[offset + length] == data[index + length]:
                length += 1
            if length > copy_length:
                copy_length = length
                copy_offset = offset
                if length == max_length:
                    break
        if copy_length >= 3:
            savings = copy_length - (3 if copy_length <= SHORT_GRAPHICS_COMMAND_LENGTH else 4)
            if savings > best_savings:
                best_command = (4, copy_length, bytes([copy_offset & 0xFF, copy_offset >> 8]))
                best_savings = savings

        if best_command is None or best_savings <= 0:
            literal.append(data[index])
            index += 1
            if len(literal) == MAX_GRAPHICS_COMMAND_LENGTH:
                flush_literal()
            continue

        flush_literal()
        command, length, payload = best_command
        _emit_graphics_command(out, command, length, payload)
        index += length

    flush_literal()
    out.append(GRAPHICS_TERMINATOR)
    return bytes(out)


def _decode_3bpp_tile(sheet: bytearray, offset: int) -> list[list[int]]:
    tile = []
    for y in range(8):
        plane_0 = sheet[offset + y * 2]
        plane_1 = sheet[offset + y * 2 + 1]
        plane_2 = sheet[offset + 0x10 + y]
        tile.append([
            ((plane_0 >> (7 - x)) & 0x01)
            | (((plane_1 >> (7 - x)) & 0x01) << 1)
            | (((plane_2 >> (7 - x)) & 0x01) << 2)
            for x in range(8)
        ])
    return tile


def _encode_3bpp_tile(sheet: bytearray, offset: int, tile: list[list[int]]) -> None:
    for y, row in enumerate(tile):
        plane_0 = 0
        plane_1 = 0
        plane_2 = 0
        for x, value in enumerate(row):
            bit = 7 - x
            plane_0 |= (value & 0x01) << bit
            plane_1 |= ((value >> 1) & 0x01) << bit
            plane_2 |= ((value >> 2) & 0x01) << bit
        sheet[offset + y * 2] = plane_0
        sheet[offset + y * 2 + 1] = plane_1
        sheet[offset + 0x10 + y] = plane_2


def remap_3bpp_tile_colors(sheet: bytearray, tile_offsets: Collection[int],
                           color_map: dict[int, int]) -> None:
    for tile_offset in tile_offsets:
        tile = _decode_3bpp_tile(sheet, tile_offset)
        for y, row in enumerate(tile):
            tile[y] = [color_map.get(value, value) for value in row]
        _encode_3bpp_tile(sheet, tile_offset, tile)


def _read_sprite_graphics_pointer(rom, graphics_pack: int) -> tuple[int, int]:
    bank = rom.read_byte(SPRITE_GRAPHICS_POINTER_BANK_TABLE + graphics_pack)
    high = rom.read_byte(SPRITE_GRAPHICS_POINTER_HIGH_TABLE + graphics_pack)
    low = rom.read_byte(SPRITE_GRAPHICS_POINTER_LOW_TABLE + graphics_pack)
    snes_address = (bank << 16) | (high << 8) | low
    return snes_address, snes_to_pc(snes_address)


def patch_boss_prize_crystal_sprite(rom) -> None:
    _, pc_address = _read_sprite_graphics_pointer(rom, BOSS_PRIZE_CRYSTAL_GRAPHICS_PACK)
    sheet, compressed_size = decompress_graphics_with_size(bytes(rom.buffer[pc_address:]))
    sheet = bytearray(sheet)

    remap_3bpp_tile_colors(
        sheet,
        BOSS_PRIZE_CRYSTAL_TILE_OFFSETS,
        BOSS_PRIZE_CRYSTAL_COLOR_REMAP,
    )

    compressed = compress_graphics(bytes(sheet))

    if decompress_graphics(compressed) != bytes(sheet):
        raise RuntimeError("Recompressed ALttP crystal graphics failed round-trip verification.")

    if len(compressed) > compressed_size:
        raise RuntimeError(
            "Recompressed ALttP crystal graphics exceed the original graphics pack size "
            f"({len(compressed)} > {compressed_size})."
        )

    rom.write_bytes(pc_address, compressed)
