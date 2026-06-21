# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "capstone>=5.0.0,<6",
#   "pefile>=2024.8.26",
#   "pycryptodome>=3.20.0",
#   "py7zr>=0.22.0",
# ]
# ///

"""Discover Rovio Lua AES keys in a PE executable and decrypt its scripts."""

from __future__ import annotations

import argparse
import io
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import pefile
import py7zr
from capstone import CS_ARCH_X86, CS_MODE_32, CS_MODE_64, Cs
from capstone.x86 import (
    X86_OP_IMM,
    X86_OP_MEM,
    X86_OP_REG,
    X86_REG_AH,
    X86_REG_AL,
    X86_REG_AX,
    X86_REG_BL,
    X86_REG_BX,
    X86_REG_CL,
    X86_REG_CX,
    X86_REG_DL,
    X86_REG_DX,
    X86_REG_EAX,
    X86_REG_EBX,
    X86_REG_ECX,
    X86_REG_EDX,
    X86_REG_RAX,
    X86_REG_RBX,
    X86_REG_RCX,
    X86_REG_RDX,
)
from Crypto.Cipher import AES


SEVEN_Z_SIGNATURE = b"7z\xbc\xaf\x27\x1c"
KEY_LENGTHS = {16, 24, 32}
MAX_KEY_FUNCTION_BYTES = 2048


LOW_BYTE_REGISTER = {
    X86_REG_AL: X86_REG_AL,
    X86_REG_AX: X86_REG_AL,
    X86_REG_EAX: X86_REG_AL,
    X86_REG_RAX: X86_REG_AL,
    X86_REG_BL: X86_REG_BL,
    X86_REG_BX: X86_REG_BL,
    X86_REG_EBX: X86_REG_BL,
    X86_REG_RBX: X86_REG_BL,
    X86_REG_CL: X86_REG_CL,
    X86_REG_CX: X86_REG_CL,
    X86_REG_ECX: X86_REG_CL,
    X86_REG_RCX: X86_REG_CL,
    X86_REG_DL: X86_REG_DL,
    X86_REG_DX: X86_REG_DL,
    X86_REG_EDX: X86_REG_DL,
    X86_REG_RDX: X86_REG_DL,
}


@dataclass(frozen=True)
class DecryptionMethod:
    key: bytes
    mode: str
    executable: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Find byte-wise AES keys in Rovio Windows executables, validate them "
            "against encrypted .lua files, and extract the embedded Lua bytecode."
        )
    )
    parser.add_argument("game_dir", type=Path, help="Game installation directory")
    parser.add_argument(
        "--exe",
        action="append",
        type=Path,
        default=[],
        help="Executable to inspect; may be repeated (default: EXEs in game_dir)",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Directory for decrypted Lua bytecode",
    )
    parser.add_argument(
        "--include-plain",
        action="store_true",
        help="Also copy Lua files that are already plaintext",
    )
    return parser.parse_args()


def _is_printable_key(candidate: bytes) -> bool:
    return len(candidate) in KEY_LENGTHS and all(0x21 <= byte <= 0x7E for byte in candidate)


def _record_candidate(values: dict[int, int], candidates: set[bytes]) -> None:
    for length in sorted(KEY_LENGTHS, reverse=True):
        if all(offset in values for offset in range(length)):
            candidate = bytes(values[offset] for offset in range(length))
            if _is_printable_key(candidate):
                candidates.add(candidate)
            return


def discover_instruction_built_keys(executable: Path) -> set[bytes]:
    """Recover keys constructed as byte assignments such as [ptr+3] = 0x6d."""

    pe = pefile.PE(str(executable), fast_load=True)
    mode = CS_MODE_64 if pe.OPTIONAL_HEADER.Magic == 0x20B else CS_MODE_32
    disassembler = Cs(CS_ARCH_X86, mode)
    disassembler.detail = True
    disassembler.skipdata = True
    candidates: set[bytes] = set()

    for section in pe.sections:
        if not section.Characteristics & 0x20000000:  # IMAGE_SCN_MEM_EXECUTE
            continue

        code = section.get_data()
        address = pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress
        register_values = {
            X86_REG_AL: None,
            X86_REG_BL: None,
            X86_REG_CL: None,
            X86_REG_DL: None,
        }
        byte_assignments: dict[int, int] = {}
        region_start = address

        for instruction in disassembler.disasm(code, address):
            if instruction.address - region_start > MAX_KEY_FUNCTION_BYTES:
                register_values = dict.fromkeys(register_values)
                byte_assignments.clear()
                region_start = instruction.address

            if instruction.mnemonic == "mov" and len(instruction.operands) == 2:
                destination, source = instruction.operands

                if destination.type == X86_OP_MEM and destination.size == 1:
                    offset = destination.mem.disp
                    value: int | None = None
                    if source.type == X86_OP_IMM:
                        value = source.imm & 0xFF
                    elif source.type == X86_OP_REG:
                        source_low = LOW_BYTE_REGISTER.get(source.reg)
                        if source_low is not None:
                            value = register_values[source_low]
                    if 0 <= offset < max(KEY_LENGTHS) and value is not None:
                        byte_assignments[offset] = value
                        _record_candidate(byte_assignments, candidates)

                if destination.type == X86_OP_REG:
                    destination_low = LOW_BYTE_REGISTER.get(destination.reg)
                    if destination_low is not None:
                        if source.type == X86_OP_IMM:
                            register_values[destination_low] = source.imm & 0xFF
                        else:
                            register_values[destination_low] = None

            if instruction.mnemonic.startswith("ret"):
                register_values = dict.fromkeys(register_values)
                byte_assignments.clear()
                region_start = instruction.address + instruction.size

    return candidates


def discover_contiguous_keys(executable: Path) -> set[bytes]:
    """Also support versions that store an AES key as a normal ASCII string."""

    data = executable.read_bytes()
    candidates: set[bytes] = set()
    for match in re.finditer(rb"(?<![!-~])[!-~]{16,32}\x00", data):
        candidate = match.group()[:-1]
        if _is_printable_key(candidate):
            candidates.add(candidate)
    return candidates


def discover_keys(executable: Path) -> set[bytes]:
    return discover_instruction_built_keys(executable) | discover_contiguous_keys(executable)


def remove_pkcs7_padding(data: bytes) -> bytes | None:
    if not data:
        return None
    padding = data[-1]
    if not 1 <= padding <= AES.block_size:
        return None
    if not data.endswith(bytes([padding]) * padding):
        return None
    return data[:-padding]


def decrypt_archive(ciphertext: bytes, key: bytes, mode: str) -> bytes | None:
    if not ciphertext or len(ciphertext) % AES.block_size:
        return None

    if mode == "cbc-zero-iv":
        cipher = AES.new(key, AES.MODE_CBC, iv=bytes(AES.block_size))
    elif mode == "ecb":
        cipher = AES.new(key, AES.MODE_ECB)
    else:
        raise ValueError(f"Unsupported AES mode: {mode}")

    plaintext = remove_pkcs7_padding(cipher.decrypt(ciphertext))
    if plaintext is None or not plaintext.startswith(SEVEN_Z_SIGNATURE):
        return None

    # CBC with a zero IV and ECB produce the same first block. Checking only the
    # magic bytes can therefore misidentify ECB when the real mode is CBC.
    try:
        with py7zr.SevenZipFile(io.BytesIO(plaintext), mode="r") as archive:
            safe_archive_names(archive)
    except (OSError, ValueError, py7zr.Bad7zFile):
        return None
    return plaintext


def find_decryption_methods(
    executables: list[Path], lua_files: list[Path]
) -> list[DecryptionMethod]:
    methods: list[DecryptionMethod] = []

    for executable in executables:
        try:
            keys = discover_keys(executable)
        except (OSError, pefile.PEFormatError) as error:
            print(f"warning: cannot inspect {executable}: {error}", file=sys.stderr)
            continue
        print(f"{executable.name}: discovered {len(keys)} candidate key(s)")
        for key in keys:
            for mode in ("cbc-zero-iv", "ecb"):
                if any(decrypt_archive(path.read_bytes(), key, mode) for path in lua_files):
                    methods.append(DecryptionMethod(key, mode, executable))

    return methods


def safe_archive_names(archive: py7zr.SevenZipFile) -> list[str]:
    names = archive.getnames()
    for name in names:
        path = PurePosixPath(name.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Unsafe path in 7-Zip archive: {name!r}")
    return names


def extract_single_file(archive_data: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        with py7zr.SevenZipFile(io.BytesIO(archive_data), mode="r") as archive:
            names = safe_archive_names(archive)
            archive.extractall(path=temporary_path)

        extracted = [path for path in temporary_path.rglob("*") if path.is_file()]
        if len(extracted) != 1:
            raise ValueError(
                f"Expected one file in archive, found {len(extracted)} ({', '.join(names)})"
            )
        return extracted[0].read_bytes()


def is_probably_plaintext_lua(data: bytes) -> bool:
    if not data or b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    readable = sum(byte in b"\t\n\r" or 0x20 <= byte <= 0x7E for byte in data)
    return readable / len(data) >= 0.95


def main() -> int:
    args = parse_args()
    game_dir = args.game_dir.expanduser().resolve()
    output_dir = args.output.expanduser().resolve()

    if not game_dir.is_dir():
        print(f"error: game directory does not exist: {game_dir}", file=sys.stderr)
        return 2

    executables = [path.expanduser().resolve() for path in args.exe]
    if not executables:
        executables = sorted(game_dir.glob("*.exe"))
    if not executables:
        print(f"error: no executables found in {game_dir}", file=sys.stderr)
        return 2

    lua_files = sorted(
        path
        for path in game_dir.rglob("*.lua")
        if not path.resolve().is_relative_to(output_dir)
    )
    if not lua_files:
        print(f"error: no Lua files found in {game_dir}", file=sys.stderr)
        return 2

    methods = find_decryption_methods(executables, lua_files)
    if not methods:
        print("error: no candidate key produced a valid encrypted 7-Zip archive", file=sys.stderr)
        return 1

    for method in methods:
        print(
            f"validated {method.mode} key from {method.executable.name}: "
            f"{method.key.decode('ascii')}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    decrypted_count = 0
    plain_count = 0
    unmatched_count = 0

    for lua_file in lua_files:
        relative_path = lua_file.relative_to(game_dir)
        ciphertext = lua_file.read_bytes()
        archive_data = None

        for method in methods:
            archive_data = decrypt_archive(ciphertext, method.key, method.mode)
            if archive_data is not None:
                break

        destination = output_dir / relative_path
        if archive_data is not None:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(extract_single_file(archive_data))
            decrypted_count += 1
        elif args.include_plain and is_probably_plaintext_lua(ciphertext):
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(lua_file, destination)
            plain_count += 1
        else:
            unmatched_count += 1

    print(
        f"decrypted {decrypted_count} file(s), copied {plain_count} plaintext file(s), "
        f"skipped {unmatched_count} unmatched file(s)"
    )
    print(f"output: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
