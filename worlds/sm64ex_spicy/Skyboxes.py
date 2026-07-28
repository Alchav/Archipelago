import random
import typing


SM64_SKYBOX_AREAS = (
    41, 51, 81, 91, 101, 111, 121, 131, 132, 151, 161, 171,
    191, 201, 211, 221, 231, 241, 261, 281, 291, 311, 331, 341, 361,
)

SM64_SKYBOX_IDS = tuple(range(10))


def generate_skybox_map(random_source: random.Random) -> typing.Dict[str, int]:
    return {
        str(area_key): random_source.choice(SM64_SKYBOX_IDS)
        for area_key in SM64_SKYBOX_AREAS
    }


def build_skybox_slot_data(mode: int, random_source: random.Random) -> typing.Dict[str, typing.Any]:
    slot_data: typing.Dict[str, typing.Any] = {"SkyboxShuffleMode": mode}
    if mode == 1:
        slot_data["SkyboxMap"] = generate_skybox_map(random_source)
    return slot_data
