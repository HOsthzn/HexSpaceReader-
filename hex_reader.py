#!/usr/bin/env python3
"""HexSpaceReader - Convert space-separated hex log files to human-readable ASCII text."""

import argparse
import sys


def hex_bytes_to_ascii(tokens: list[str]) -> str:
    """Convert a list of hex byte tokens to an ASCII string.

    Non-printable bytes (except tab/newline/carriage-return) are shown as \\xNN.
    Invalid tokens are skipped with a warning written to stderr.
    """
    parts = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        try:
            byte_val = int(token, 16)
        except ValueError:
            print(f"[warn] skipping invalid hex token: {token!r}", file=sys.stderr)
            continue

        char = chr(byte_val)
        if char.isprintable() or char in ("\t", "\n", "\r"):
            parts.append(char)
        else:
            parts.append(f"\\x{byte_val:02x}")

    return "".join(parts)


def process_stream(in_stream, out_stream, line_numbers: bool) -> int:
    """Read hex lines from in_stream, write decoded ASCII to out_stream.

    Returns the number of lines processed.
    """
    count = 0
    for lineno, raw_line in enumerate(in_stream, start=1):
        line = raw_line.rstrip("\n\r")
        if not line.strip():
            out_stream.write("\n")
            continue

        tokens = line.split()
        decoded = hex_bytes_to_ascii(tokens)

        if line_numbers:
            out_stream.write(f"{lineno:>6}: {decoded}\n")
        else:
            out_stream.write(decoded + "\n")

        count += 1

    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hex_reader",
        description="Convert a log file of space-separated hex bytes to human-readable ASCII.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hex_reader.py input.log
  hex_reader.py input.log -o output.txt
  hex_reader.py input.log --line-numbers
  cat input.log | hex_reader.py -
        """,
    )
    parser.add_argument(
        "input",
        metavar="FILE",
        help="Path to the hex log file, or '-' to read from stdin.",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        default=None,
        help="Write decoded output to FILE instead of stdout.",
    )
    parser.add_argument(
        "-n", "--line-numbers",
        action="store_true",
        help="Prefix each output line with its source line number.",
    )

    args = parser.parse_args(argv)

    # --- open input ---
    try:
        if args.input == "-":
            in_stream = sys.stdin
        else:
            in_stream = open(args.input, "r", encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"error: cannot open input file: {exc}", file=sys.stderr)
        return 1

    # --- open output ---
    try:
        if args.output:
            out_stream = open(args.output, "w", encoding="utf-8")
        else:
            out_stream = sys.stdout
    except OSError as exc:
        print(f"error: cannot open output file: {exc}", file=sys.stderr)
        if in_stream is not sys.stdin:
            in_stream.close()
        return 1

    # --- process ---
    try:
        count = process_stream(in_stream, out_stream, line_numbers=args.line_numbers)
        if args.output:
            print(f"Decoded {count} line(s) → {args.output}", file=sys.stderr)
    finally:
        if in_stream is not sys.stdin:
            in_stream.close()
        if out_stream is not sys.stdout:
            out_stream.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
