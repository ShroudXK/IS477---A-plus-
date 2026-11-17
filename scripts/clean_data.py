import pandas as pd
from pathlib import Path

raw_folder = Path("data/raw")
clean_folder = Path("data/clean")
clean_folder.mkdir(parents=True, exist_ok=True)
