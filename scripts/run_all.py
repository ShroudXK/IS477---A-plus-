"""Run the whole workflow, one step at a time, from a fresh clone.

    python scripts/run_all.py

Each step is its own script. If a step fails, the workflow stops.
"""
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Steps in order: acquisition -> quality assessment -> cleaning -> integration.
# The analysis scripts will be added here when they are ready.
STEPS = [
    ("Download raw data from Box and check SHA-256", "scripts/download_data.py"),
    ("Data quality assessment (read-only report)", "scripts/Data quality Assessment.py"),
    ("Clean the three datasets", "scripts/clean_data.py"),
    ("Integrate crashes, people, and weather", "scripts/integrate_data.py"),
]


def main():
    start_all = time.time()
    for number, (title, script) in enumerate(STEPS, start=1):
        print(f"\n=== Step {number}/{len(STEPS)}: {title} ({script}) ===", flush=True)
        start = time.time()
        # sys.executable is the same Python that runs this file.
        result = subprocess.run([sys.executable, str(PROJECT_ROOT / script)], cwd=PROJECT_ROOT)
        if result.returncode != 0:
            sys.exit(f"Step {number} failed: {script}. The workflow stopped.")
        print(f"--- Step {number} finished in {time.time() - start:.1f} s", flush=True)
    print(f"\nAll steps finished in {time.time() - start_all:.1f} s.")


if __name__ == "__main__":
    main()
