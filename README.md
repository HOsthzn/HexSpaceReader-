# HexSpaceReader

A lightweight Python CLI tool that converts log files containing space-separated hex bytes into human-readable ASCII text.

## What it does

If you have log files where data is stored as hex bytes like this:

```
48 65 6C 6C 6F 2C 20 57 6F 72 6C 64 21
45 72 72 6F 72 3A 20 63 6F 6E 6E 65 63 74 69 6F 6E 20 74 69 6D 65 64 20 6F 75 74
53 74 61 74 75 73 3A 20 4F 4B
```

HexSpaceReader converts it to this:

```
Hello, World!
Error: connection timed out
Status: OK
```

## Requirements

- Python 3.10+
- No external dependencies

## Usage

```bash
python3 hex_reader.py <FILE> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `FILE` | Path to the hex log file. Use `-` to read from stdin. |
| `-o FILE`, `--output FILE` | Write decoded output to a file instead of stdout. |
| `-n`, `--line-numbers` | Prefix each output line with its source line number. |
| `-h`, `--help` | Show help and exit. |

### Examples

**Decode to stdout:**
```bash
python3 hex_reader.py input.log
```

**Decode with line numbers:**
```bash
python3 hex_reader.py input.log -n
```

Output:
```
     1: Hello, World!
     2: Error: connection timed out
     3: Status: OK
```

**Write to an output file:**
```bash
python3 hex_reader.py input.log -o decoded.txt
```

**Pipe from stdin:**
```bash
cat input.log | python3 hex_reader.py -
```

**Chain with other tools:**
```bash
grep "ERROR" input.log | python3 hex_reader.py -
```

## Input Format

Each line of the log file should contain one or more space-separated hex byte tokens:

```
48 65 6C 6C 6F   ← decoded as: Hello
```

- Tokens are case-insensitive (`4F` and `4f` both work)
- Blank lines are preserved in output
- Non-printable bytes (control characters, etc.) are rendered as `\xNN` escape sequences rather than silently dropped
- Invalid (non-hex) tokens emit a warning to stderr and are skipped

## Running the Tests

```bash
python3 -m unittest test_hex_reader -v
```

14 tests cover byte conversion, stream processing, line numbering, invalid input handling, and the CLI.

## Project Structure

```
HexSpaceReader/
├── hex_reader.py       # Main CLI tool
├── test_hex_reader.py  # Unit tests
├── sample.log          # Example input file
└── README.md
```

## License

MIT
