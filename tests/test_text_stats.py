import json
import subprocess
import sys
import unittest
from pathlib import Path

from src.text_stats import file_stats, text_stats


ROOT = Path(__file__).resolve().parents[1]


class TextStatsTests(unittest.TestCase):
    def test_sample_file(self) -> None:
        self.assertEqual(
            file_stats(ROOT / "sample.txt"),
            {"lines": 5, "words": 14, "characters": 88},
        )

    def test_utf8_text(self) -> None:
        self.assertEqual(
            text_stats("Café 世界\n"),
            {"lines": 1, "words": 2, "characters": 8},
        )

    def test_empty_text(self) -> None:
        self.assertEqual(
            text_stats(""),
            {"lines": 0, "words": 0, "characters": 0},
        )

    def test_top_words_are_case_insensitive_and_deterministic(self) -> None:
        self.assertEqual(
            text_stats("Beta alpha ALPHA beta gamma", top=3),
            {
                "lines": 1,
                "words": 5,
                "characters": 27,
                "top_words": [
                    {"word": "alpha", "count": 2},
                    {"word": "beta", "count": 2},
                    {"word": "gamma", "count": 1},
                ],
            },
        )

    def test_top_zero_returns_no_words(self) -> None:
        self.assertEqual(
            text_stats("one two", top=0)["top_words"],
            [],
        )

    def test_command_line_output_is_json(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "src" / "text_stats.py"), str(ROOT / "sample.txt")],
            capture_output=True,
            check=True,
            text=True,
        )
        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 5, "words": 14, "characters": 88},
        )

    def test_command_line_top_words(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "src" / "text_stats.py"),
                str(ROOT / "sample.txt"),
                "--top",
                "2",
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        self.assertEqual(
            json.loads(result.stdout)["top_words"],
            [
                {"word": "fourth?", "count": 2},
                {"word": "is", "count": 2},
            ],
        )

    def test_command_line_rejects_negative_top(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "src" / "text_stats.py"),
                str(ROOT / "sample.txt"),
                "--top",
                "-1",
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
