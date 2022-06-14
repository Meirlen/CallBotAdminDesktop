from pathlib import Path

import sys
import os

CWD = Path(
    getattr(
        sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__))
    )
)
