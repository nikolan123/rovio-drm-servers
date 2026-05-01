import platform
import struct
import subprocess
import sys


def current_arch_label() -> str:
    is_32_bit = struct.calcsize("P") * 8 == 32
    machine = platform.machine().lower()

    if is_32_bit:
        return "win-x86"

    if machine in {"amd64", "x86_64"}:
        return "win-x64"

    return f"win-{machine or 'unknown'}"


arch_label = current_arch_label()

cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "main.py",
    "--name",
    f"Rovio CAS-{arch_label}",
    "--onefile",
    # "--windowed", # prevent console appearing
]
subprocess.call(cmd)
