# setup.py
import os
from cx_Freeze import setup, Executable

# ---- Metadata ----
APP_NAME = "soundcloud-to-tiermaker"
APP_VERSION = input("Version (e.g., 1.0.0): ") or "1.0.0"
APP_VERSION = APP_VERSION.strip()
ENTRYPOINT = "gui.py"

# ---- Dependencies ----
build_exe_options = {
    "packages": [],
    "excludes": [],
    "include_files": [
        "README.md"
    ],
}

# ---- Executable target ----
base = "Win32GUI" if os.name == "nt" else None
executables = [
    Executable(ENTRYPOINT, base=base, target_name=APP_NAME.lower())
]

# ---- Setup ----
setup(
    name=APP_NAME,
    version=APP_VERSION,
    description=APP_NAME,
    options={"build_exe": build_exe_options},
    executables=executables,
)

os.system(f"explorer {os.path.abspath('./build/exe.win-amd64-3.11')}")
