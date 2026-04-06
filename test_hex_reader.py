"""Unit tests for hex_reader.py"""

import io
import sys
import unittest

sys.path.insert(0, ".")
from hex_reader import hex_bytes_to_ascii, process_stream, main


class TestHexBytesToAscii(unittest.TestCase):
    def test_hello_world(self):
        tokens = "48 65 6C 6C 6F 2C 20 57 6F 72 6C 64 21".split()
        self.assertEqual(hex_bytes_to_ascii(tokens), "Hello, World!")

    def test_uppercase_hex(self):
        tokens = "48 45 4C 4C 4F".split()
        self.assertEqual(hex_bytes_to_ascii(tokens), "HELLO")

    def test_lowercase_hex(self):
        tokens = "68 65 6c 6c 6f".split()
        self.assertEqual(hex_bytes_to_ascii(tokens), "hello")

    def test_non_printable_shown_as_escape(self):
        tokens = ["01", "02", "41"]  # SOH, STX, 'A'
        result = hex_bytes_to_ascii(tokens)
        self.assertIn("\\x01", result)
        self.assertIn("\\x02", result)
        self.assertIn("A", result)

    def test_tab_preserved(self):
        tokens = ["41", "09", "42"]  # A, TAB, B
        self.assertEqual(hex_bytes_to_ascii(tokens), "A\tB")

    def test_empty_tokens(self):
        self.assertEqual(hex_bytes_to_ascii([]), "")

    def test_invalid_token_skipped(self):
        tokens = ["48", "ZZ", "69"]
        result = hex_bytes_to_ascii(tokens)
        self.assertEqual(result, "Hi")

    def test_numbers_and_symbols(self):
        tokens = "31 32 33 20 21 40 23".split()  # "123 !@#"
        self.assertEqual(hex_bytes_to_ascii(tokens), "123 !@#")


class TestProcessStream(unittest.TestCase):
    def _run(self, text: str, line_numbers: bool = False) -> str:
        in_stream = io.StringIO(text)
        out_stream = io.StringIO()
        process_stream(in_stream, out_stream, line_numbers=line_numbers)
        return out_stream.getvalue()

    def test_single_line(self):
        out = self._run("48 65 6C 6C 6F\n")
        self.assertEqual(out, "Hello\n")

    def test_multiple_lines(self):
        out = self._run("48 69\n42 79 65\n")
        self.assertEqual(out, "Hi\nBye\n")

    def test_blank_line_preserved(self):
        out = self._run("48 69\n\n42 79 65\n")
        self.assertEqual(out, "Hi\n\nBye\n")

    def test_line_numbers(self):
        out = self._run("48 69\n42 79 65\n", line_numbers=True)
        lines = out.splitlines()
        self.assertIn("Hi", lines[0])
        self.assertIn("Bye", lines[1])
        self.assertTrue(lines[0].strip().startswith("1"))
        self.assertTrue(lines[1].strip().startswith("2"))


class TestCLI(unittest.TestCase):
    def test_missing_file_returns_error(self):
        ret = main(["nonexistent_file_xyz.log"])
        self.assertEqual(ret, 1)

    def test_reads_sample_log(self):
        ret = main(["sample.log"])
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
