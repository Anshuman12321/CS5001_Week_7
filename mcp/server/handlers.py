"""
Tool handlers — pure Python functions, one per tool.

Function names must match the tool names in schemas.py exactly;
app.py dispatches by name using getattr(handlers, name).

No MCP imports here — these are plain functions that can be
tested independently of the MCP server.
"""
from pathlib import Path

MAX_FILE_CHARS = 8_000


def read_file(path: str) -> str:
    return Path(path).read_text(errors="replace")[:MAX_FILE_CHARS]


def list_directory(path: str) -> str:
    entries = sorted(Path(path).iterdir(), key=lambda e: (e.is_file(), e.name))
    lines   = [f"{'DIR ' if e.is_dir() else 'FILE'} {e.name}" for e in entries]
    return "\n".join(lines) or "(empty)"


def grep_code(pattern: str, path: str) -> str:
    """Search *.py files for a literal substring (cross-platform, no shell grep)."""
    root = Path(path).resolve()
    files = [root] if root.is_file() and root.suffix == ".py" else sorted(root.rglob("*.py"))
    lines_out: list[str] = []
    for fp in files:
        if not fp.is_file():
            continue
        try:
            text = fp.read_text(errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if pattern in line:
                lines_out.append(f"{fp}:{i}:{line}")
    return "\n".join(lines_out) if lines_out else "No matches found."
