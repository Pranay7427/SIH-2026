import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Ensure output directory works in serverless read-only environments (e.g. Vercel)
if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    OUTPUTS_DIR = Path("/tmp/sim_outputs")
else:
    OUTPUTS_DIR = BASE_DIR / "sim_outputs"

try:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    OUTPUTS_DIR = Path("/tmp/sim_outputs")
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Delft3D FM configuration
DELFT3D_BIN_PATH = os.getenv("DELFT3D_BIN_PATH", "dflowfm.exe")
# DualSPHysics configuration
DUALSPHYSICS_BIN_PATH = os.getenv("DUALSPHYSICS_BIN_PATH", "DualSPHysics5.2_win64.exe")

# Operating mode: "MOCK" or "REAL"
# Defaults to MOCK if Delft3D executable is not discovered on the machine
def detect_mode() -> str:
    env_mode = os.getenv("MODE", "").upper()
    if env_mode in ["MOCK", "REAL"]:
        return env_mode
    # Auto-detect if binary exists
    if Path(DELFT3D_BIN_PATH).is_file():
        return "REAL"
    return "MOCK"

MODE = detect_mode()

# Server configs
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
