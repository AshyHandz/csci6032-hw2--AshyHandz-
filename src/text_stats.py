"""Count lines, words, and characters in a UTF-8 text file."""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Union


def text_stats(text: str, top: Optional[int] = None) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]:
    """Return line, word, and character counts for text."""
    stats: Dict[str, Union[int, List[Dict[str, Union[str, int]]]]] = {
        "lines": len(text.splitlines()),
        "words": len(re.findall(r"\S+", text)),
        "characters": len(text),
    }
    if top is not None:
        word_counts: Dict[str, int] = {}
        for word in re.findall(r"\S+", text):
            normalized_word = word.casefold()
            word_counts[normalized_word] = word_counts.get(normalized_word, 0) + 1
        ranked_words = sorted(
            word_counts.items(), key=lambda item: (-item[1], item[0])
        )
        stats["top_words"] = [
            {"word": word, "count": count} for word, count in ranked_words[:top]
        ]
    return stats


def file_stats(
    path: Path, top: Optional[int] = None
) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]:
    """Read a UTF-8 file and return its text statistics."""
    with path.open("r", encoding="utf-8", newline="") as file:
        return text_stats(file.read(), top=top)


def main() -> None:
    """Parse the command line and print statistics as JSON."""
    parser = argparse.ArgumentParser(
        description="Count lines, words, and characters in a UTF-8 text file."
    )
    parser.add_argument("file", type=Path, help="path to the UTF-8 text file")
    parser.add_argument(
        "--top",
        type=int,
        metavar="N",
        help="include the N most frequent words",
    )
    args = parser.parse_args()
    if args.top is not None and args.top < 0:
        parser.error("--top must be non-negative")
    print(json.dumps(file_stats(args.file, top=args.top), ensure_ascii=False))


if __name__ == "__main__":
    main()
