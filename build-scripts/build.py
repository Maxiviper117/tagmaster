# /// script
# dependencies = ["pyinstaller"]
# ///

import subprocess
import sys

def main():
    try:
        subprocess.run(
            ["pyinstaller", "./tagger.py", "--onefile"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
