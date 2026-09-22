"""Count lines, words, and characters in a UTF-8 text file."""

import argparse
import json
import re
from pathlib import Path
from typing import Dict


def text_stats(text: str) -> Dict[str, int]:
    """Return line, word, and character counts for text."""
    return {
        "lines": len(text.splitlines()),
        "words": len(re.findall(r"\S+", text)),
        "characters": len(text),
    }


def file_stats(path: Path) -> Dict[str, int]:
    """Read a UTF-8 file and return its text statistics."""
    with path.open("r", encoding="utf-8", newline="") as file:
        return text_stats(file.read())


def main() -> None:
    """Parse the command line and print statistics as JSON."""
    parser = argparse.ArgumentParser(
        description="Count lines, words, and characters in a UTF-8 text file."
    )
    parser.add_argument("file", type=Path, help="path to the UTF-8 text file")
    args = parser.parse_args()
    print(json.dumps(file_stats(args.file), ensure_ascii=False))


if __name__ == "__main__":
    main()
