import os
from pathlib import Path

# Paths
SDK_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_ROOT / "data"

# Build configs
DEBUG = os.environ.get("OPENGITA_DEBUG", "0") == "1"
