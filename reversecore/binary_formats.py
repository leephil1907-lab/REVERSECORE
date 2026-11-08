"""Bounds-checked metadata parsers for common executable formats."""
from __future__ import annotations

import struct
from pathlib import Path
from typing import Any

class FormatError(ValueError):
    """The input is truncated or structurally inconsistent."""

def _need(data: bytes, offset: int, size: int, label: str) -> None:
    if offset < 0 or size < 0 or offset + size > len(data):
        raise FormatError(f"truncated {label}: need bytes {offset}..{offset + size}, file has {len(data)}")

def _unpack(data: bytes, fmt: str, offset: int, label: str) -> tuple[Any, ...]:
    size = struct.calcsize(fmt)
    _need(data, offset, size, label)
    return struct.unpack_from(fmt, data, offset)

def parse_pe(path: str | Path) -> dict[str, Any]:
    data = Path(path).read_bytes()
    if len(data) < 64 or data[:2] != b"MZ":
        raise FormatError("not a valid DOS/PE candidate")
    pe_offset = _unpack(data, "<I", 0x3C, "DOS header")[0]
    _need(data, pe_offset, 24, "PE signature and COFF header")
    if data[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise FormatError("PE signature not found at e_lfanew")
    coff = pe_offset + 4
    machine, sections, timestamp, sym_ptr, sym_count, optional_size, characteristics = _unpack(data, "<HHIIIHH", coff, "COFF header")
    optional = coff + 20
    _need(data, optional, optional_size, "PE optional header")
    magic = _unpack(data, "<H", optional, "optional header magic")[0]
    if magic == 0x10B:
        image_base = _unpack(data, "<I", optional + 28, "PE32 image base")[0]
        entry_rva = _unpack(data, "<I", optional + 16, "entry point")[0]
        format_name = "PE32"
    elif magic == 0x20B:
        image_base = _unpack(data, "<Q", optional + 24, "PE32+ image base")[0]
        entry_rva = _unpack(data, "<I", optional + 16, "entry point")[0]
        format_name = "PE32+"
    else:
        raise FormatError(f"unknown PE optional-header magic: 0x{magic:04x}")
    section_offset = optional + optional_size
    rows = []
    for index in range(sections):
        off = section_offset + index * 40
        _need(data, off, 40, f"section header {index}")
        name = data[off:off + 8].split(b"\0", 1)[0].decode("ascii", "replace")
        virtual_size, virtual_address, raw_size, raw_pointer = _unpack(data, "<IIII", off + 8, "section sizes")
        rows.append({"name": name, "virtual_address": virtual_address, "virtual_size": virtual_size,
                     "raw_size": raw_size, "raw_offset": raw_pointer})
    return {"format": format_name, "machine": f"0x{machine:04x}", "section_count": sections,
            "timestamp_unix": timestamp, "image_base": image_base, "entry_point_rva": entry_rva,
            "characteristics": f"0x{characteristics:04x}", "sections": rows}

def parse_elf(path: str | Path) -> dict[str, Any]:
    data = Path(path).read_bytes()
    if len(data) < 16 or data[:4] != b"\x7fELF":
        raise FormatError("not an ELF file")
    elf_class, encoding = data[4], data[5]
    if elf_class not in (1, 2) or encoding not in (1, 2):
        raise FormatError("unsupported ELF class or byte order")
    endian = "<" if encoding == 1 else ">"
    if elf_class == 1:
        fields = _unpack(data, endian + "HHIIIIIHHHHHH", 16, "ELF32 header")
        elf_type, machine, version, entry, phoff, shoff, flags, ehsize, phentsize, phnum, shentsize, shnum, shstrndx = fields
        word = 4
    else:
        fields = _unpack(data, endian + "HHIQQQIHHHHHH", 16, "ELF64 header")
        elf_type, machine, version, entry, phoff, shoff, flags, ehsize, phentsize, phnum, shentsize, shnum, shstrndx = fields
        word = 8
    sections = []
    if shnum and shentsize:
        _need(data, shoff, shentsize * shnum, "ELF section table")
        for index in range(shnum):
            off = shoff + index * shentsize
            if word == 4:
                name_off, stype, sflags, addr, file_off, size, link, info, align, entsize = _unpack(data, endian + "IIIIIIIIII", off, "ELF32 section")
            else:
                name_off, stype, sflags, addr, file_off, size, link, info, align, entsize = _unpack(data, endian + "IIQQQQIIQQ", off, "ELF64 section")
            sections.append({"name_offset": name_off, "type": stype, "address": addr, "offset": file_off, "size": size})
    return {"format": f"ELF{32 if word == 4 else 64}", "endianness": "little" if endian == "<" else "big",
            "type": elf_type, "machine": machine, "entry_point": entry, "program_header_offset": phoff,
            "program_header_count": phnum, "section_header_offset": shoff, "section_header_count": shnum,
            "sections": sections}

def parse_macho(path: str | Path) -> dict[str, Any]:
    data = Path(path).read_bytes()
    if len(data) < 4:
        raise FormatError("file too small for Mach-O magic")
    magic = data[:4]
    formats = {
        b"\xce\xfa\xed\xfe": ("<", False, "Mach-O 32-bit"),
        b"\xcf\xfa\xed\xfe": ("<", True, "Mach-O 64-bit"),
        b"\xfe\xed\xfa\xce": (">", False, "Mach-O 32-bit"),
        b"\xfe\xed\xfa\xcf": (">", True, "Mach-O 64-bit"),
    }
    if magic in formats:
        endian, is64, name = formats[magic]
        cpu, subtype, filetype, ncmds, sizeofcmds, flags = _unpack(data, endian + "IIIIII", 4, "Mach-O header")
        return {"format": name, "cpu_type": cpu, "cpu_subtype": subtype, "file_type": filetype,
                "load_command_count": ncmds, "load_commands_bytes": sizeofcmds, "flags": flags}
    fat_formats = {b"\xca\xfe\xba\xbe": ">", b"\xbe\xba\xfe\xca": "<"}
    if magic in fat_formats:
        endian = fat_formats[magic]
        count = _unpack(data, endian + "I", 4, "fat header")[0]
        if count > 4096:
            raise FormatError("unreasonable fat Mach-O architecture count")
        rows = []
        for i in range(count):
            cpu, subtype, offset, size, align = _unpack(data, endian + "IIIII", 8 + i * 20, "fat architecture")
            _need(data, offset, size, f"fat architecture slice {i}")
            rows.append({"cpu_type": cpu, "cpu_subtype": subtype, "offset": offset, "size": size, "alignment": align})
        return {"format": "Mach-O universal/fat", "architecture_count": count, "architectures": rows}
    raise FormatError("unrecognized Mach-O magic")

def _uleb128(data: bytes, offset: int) -> tuple[int, int]:
    result = shift = 0
    while True:
        _need(data, offset, 1, "DEX ULEB128")
        byte = data[offset]
        offset += 1
        result |= (byte & 0x7f) << shift
        if not byte & 0x80:
            return result, offset
        shift += 7
        if shift > 35:
            raise FormatError("invalid DEX ULEB128 value")

def parse_dex(path: str | Path, max_strings: int = 2000) -> dict[str, Any]:
    data = Path(path).read_bytes()
    if len(data) < 0x70 or not data.startswith(b"dex\n") or data[7] != 0:
        raise FormatError("not a standard DEX file")
    file_size, header_size, endian_tag = _unpack(data, "<III", 0x20, "DEX header")
    if header_size != 0x70 or file_size > len(data) or file_size < header_size:
        raise FormatError("invalid DEX header or declared file size")
    if endian_tag != 0x12345678:
        raise FormatError("unsupported DEX byte order")
    string_count, string_offset = _unpack(data, "<II", 0x38, "DEX string table header")
    if string_count > 10_000_000:
        raise FormatError("unreasonable DEX string count")
    _need(data, string_offset, string_count * 4, "DEX string ID table")
    strings = []
    for index in range(min(string_count, max_strings)):
        item_off = _unpack(data, "<I", string_offset + index * 4, "DEX string ID")[0]
        _, cursor = _uleb128(data, item_off)  # UTF-16 length; decoding is best-effort below.
        end = data.find(b"\0", cursor, min(len(data), cursor + 1_000_000))
        if end < 0:
            continue
        strings.append(data[cursor:end].decode("utf-8", "replace"))
    return {"format": "DEX", "version": data[4:7].decode("ascii", "replace"),
            "file_size": file_size, "header_size": header_size, "checksum_adler32": f"0x{_unpack(data, '<I', 8, 'DEX checksum')[0]:08x}",
            "string_id_count": string_count, "strings_sample": strings, "strings_sample_count": len(strings)}
