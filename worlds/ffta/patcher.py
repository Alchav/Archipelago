# Patcher created by Silvris for APPP
from __future__ import annotations

import json
import struct
import zipfile
from enum import IntEnum
import os
import threading
import bsdiff4

from typing import ClassVar, Dict, Tuple, Any, Optional, Union, BinaryIO, List

from worlds.Files import AutoPatchRegister, APContainer, APDeltaPatch

semaphore = threading.Semaphore(os.cpu_count() or 4)

del threading
del os

current_patch_version: int = 6


class AutoPatchExtensionRegister(type):
    extension_types: ClassVar[Dict[str, AutoPatchExtensionRegister]] = {}
    required_extensions: List[str] = []

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoPatchExtensionRegister:
        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoPatchExtensionRegister.extension_types[dct["game"]] = new_class
        return new_class

    @staticmethod
    def get_handler(game: str) -> Union[AutoPatchExtensionRegister, List[AutoPatchExtensionRegister]]:
        for extension_type, handler in AutoPatchExtensionRegister.extension_types.items():
            if extension_type == game:
                if handler.required_extensions:
                    handlers = [handler]
                    for required in handler.required_extensions:
                        if required in AutoPatchExtensionRegister.extension_types:
                            handlers.append(AutoPatchExtensionRegister.extension_types[required])
                        else:
                            raise NotImplementedError(f"No handler for {required}.")
                    return handlers
                else:
                    return handler
        return APPatchExtension


class APProcedurePatch(APContainer, metaclass=AutoPatchRegister):
    """
    An APContainer that defines a procedure to produce the desired file.
    """
    procedure: List[Tuple[str, List[Any]]]
    hash: Optional[str]  # base checksum of source file
    source_data: bytes
    patch_file_ending: str = ""
    result_file_ending: str = ".sfc"
    files: Dict[str, bytes] = {}

    @classmethod
    def get_source_data(cls) -> bytes:
        """Get Base data"""
        raise NotImplementedError()

    @classmethod
    def get_source_data_with_cache(cls) -> bytes:
        if not hasattr(cls, "source_data"):
            cls.source_data = cls.get_source_data()
        return cls.source_data

    def __init__(self, *args: Any, **kwargs: Any):
        super(APProcedurePatch, self).__init__(*args, **kwargs)

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super(APProcedurePatch, self).get_manifest()
        manifest["base_checksum"] = self.hash
        manifest["result_file_ending"] = self.result_file_ending
        manifest["patch_file_ending"] = self.patch_file_ending
        manifest["procedure"] = self.procedure
        return manifest

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).read_contents(opened_zipfile)
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        #if manifest["version"] < 6:
            # support patching files made before moving to procedures
            #self.procedure = [("apply_bsdiff4", ["delta.bsdiff4"])]
        #else:
        self.procedure = manifest["procedure"] # need to remove those lines in order for it to patch properly, otherwise it always assumes this is a delta patch
        for file in opened_zipfile.namelist():
            if file not in ["archipelago.json"]:
                self.files[file] = opened_zipfile.read(file)



    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).write_contents(opened_zipfile)
        for file in self.files:
            opened_zipfile.writestr(file, self.files[file],
                                    compress_type=zipfile.ZIP_STORED if file.endswith(".bsdiff4") else None)

    def get_file(self, file: str) -> bytes:
        """ Retrieves a file from the patch container."""
        if file not in self.files:
            self.read()
        return self.files[file]

    def write_file(self, file_name: str, file: bytes) -> None:
        """ Writes a file to the patch container, to be retrieved upon patching. """
        self.files[file_name] = file

    def patch(self, target: str) -> None:
        self.read()
        base_data = self.get_source_data_with_cache()
        patch_extender = AutoPatchExtensionRegister.get_handler(self.game)
        for step, args in self.procedure:
            if isinstance(patch_extender, list):
                extension = next((item for item in [getattr(extender, step, None) for extender in patch_extender]
                                  if item is not None), None)
            else:
                extension = getattr(patch_extender, step, None)
            if extension is not None:
                base_data = extension(self, base_data, *args)
            else:
                raise NotImplementedError(f"Unknown procedure {step} for {self.game}.")
        with open(target, 'wb') as f:
            f.write(base_data)


class APTokenTypes(IntEnum):
    WRITE = 0
    COPY = 1
    RLE = 2
    AND_8 = 3
    OR_8 = 4
    XOR_8 = 5


class APTokenMixin:
    """
    A class that defines functions for generating a token binary, for use in patches.
    """
    tokens: List[
        Tuple[int, int,
              Union[
                    bytes,  # WRITE
                    Tuple[int, int],  # COPY, RLE
                    int  # AND_8, OR_8, XOR_8
              ]]] = []

    def get_token_binary(self) -> bytes:
        """
        Returns the token binary created from stored tokens.
        :return: A bytes object representing the token data.
        """
        data = bytearray()
        data.extend(struct.pack("I", len(self.tokens)))
        for token_type, offset, args in self.tokens:
            data.append(token_type)
            data.extend(struct.pack("I", offset))
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                data.extend(struct.pack("I", 1))
                data.append(args)
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                data.extend(struct.pack("I", 8))
                data.extend(struct.pack("I", args[0]))
                data.extend(struct.pack("I", args[1]))
            else:
                data.extend(struct.pack("I", len(args)))
                data.extend(args)
        return data

    def write_token(self, token_type: APTokenTypes, offset: int, data: Union[bytes, Tuple[int, int], int]):
        """
        Stores a token to be used by patching.
        """
        self.tokens.append((token_type, offset, data))


class APPatchExtension(metaclass=AutoPatchExtensionRegister):
    """Class that defines patch extension functions for a given game.
    Patch extension functions must have the following two arguments in the following order:

    caller: APProcedurePatch (used to retrieve files from the patch container)

    rom: bytes (the data to patch)

    Further arguments are passed in from the procedure as defined.

    Patch extension functions must return the changed bytes.
    """
    game: str
    required_extensions: List[str] = []

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str):
        """Applies the given bsdiff4 from the patch onto the current file."""
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_tokens(caller: APProcedurePatch, rom: bytes, token_file: str) -> bytes:
        """Applies the given token file from the patch onto the current file."""
        token_data = caller.get_file(token_file)
        rom_data = bytearray(rom)
        token_count = struct.unpack("I", token_data[0:4])[0]
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = struct.unpack("I", token_data[bpr + 1:bpr + 5])[0]
            size = struct.unpack("I", token_data[bpr + 5:bpr + 9])[0]
            data = token_data[bpr + 9:bpr + 9 + size]
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                arg = data[0]
                if token_type == APTokenTypes.AND_8:
                    rom_data[offset] = rom_data[offset] & arg
                elif token_type == APTokenTypes.OR_8:
                    rom_data[offset] = rom_data[offset] | arg
                else:
                    rom_data[offset] = rom_data[offset] ^ arg
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                args = struct.unpack("II", data)
                length = args[0]
                value = args[1]
                if token_type == APTokenTypes.COPY:
                    rom_data[offset: offset + length] = rom_data[value: value + length]
                else:
                    rom_data[offset: offset + length] = bytes([value] * length)
            else:
                rom_data[offset:offset + len(data)] = data
            bpr += 9 + size
        return rom_data

