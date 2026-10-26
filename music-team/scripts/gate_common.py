#!/usr/bin/env python3
"""gate_common.py - shared CLI, config, threshold, parsing, and result contract
for every music-team gate script (plan section 12; stage-gates.md section 2).

Contract every gate script honours:

    usage: <script>.py [--config .song/config.yml] [--json] [--genre <g>] <artifact paths...>
    exit codes: 0 PASS | 1 FAIL | 2 SKIPPED | 3 ERROR
    --json stdout schema:
    { "script", "status", "thresholds": {}, "metrics": {}, "violations": [ {location, reason, observed, limit} ] }

Threshold precedence: explicit flag > quality.genre_overrides.<genre>.<key> > quality.<key> > built-in default.

Stdlib only; safe under ``python -I``. Paths are normalised with
``pathlib.PurePath(p).as_posix()`` before any matching.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePath
from typing import Any, Callable

PASS, FAIL, SKIPPED, ERROR = "PASS", "FAIL", "SKIPPED", "ERROR"
EXIT = {PASS: 0, FAIL: 1, SKIPPED: 2, ERROR: 3}

# Built-in defaults: the values in references/shared/config-schema.md.
DEFAULT_QUALITY: dict[str, Any] = {
    "cliche_max_per_100_words": 2,
    "hook_max_syllables": 12,
    "prosody_tolerance": 0.15,
    "slant_rhyme_allowed": True,
    "diatonic_min_ratio": 0.6,
    "max_melodic_leap": 12,
    "vocal_range": [55, 79],
    "energy_curve": "chorus_rising",
    "adversarial_lyrics": False,
    "listener_panel_size": 3,
}
DEFAULT_ORIGINALITY: dict[str, Any] = {
    "resemblance_corpus": [],
    "ngram_max_overlap": 0.05,
    "block_artist_references": True,
}

SCRIPTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS_DIR.parent
SHARED_DIR = PLUGIN_ROOT / "references" / "shared"
DATA_DIR = SCRIPTS_DIR / "data"


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
def norm(path: str | Path) -> str:
    """Normalise a path to POSIX form so Windows backslashes match.

    ``PurePath.as_posix()`` only converts separators on Windows; backslashes are
    translated first so a Windows-style argument is handled on every platform."""
    return PurePath(str(path).replace("\\", "/")).as_posix()


def read_text(path: str | Path) -> str:
    return Path(norm(path)).read_text(encoding="utf-8-sig", errors="replace")


def file_named(paths: list[str], name: str) -> str | None:
    """Return the first path whose basename equals ``name`` (case-insensitive)."""
    for p in paths:
        if PurePath(norm(p)).name.lower() == name.lower():
            return p
    return None


# ---------------------------------------------------------------------------
# Minimal YAML subset loader (maps, scalars, inline lists/maps, block lists)
# ---------------------------------------------------------------------------
_INLINE_LIST = re.compile(r"^\[(.*)\]$")
_INLINE_MAP = re.compile(r"^\{(.*)\}$")
_INT = re.compile(r"^-?\d+$")
_FLOAT = re.compile(r"^-?\d+\.\d+$")


def _split_top_level(inner: str) -> list[str]:
    """Split on commas that are not nested inside [] or {}."""
    parts, depth, cur = [], 0, []
    for ch in inner:
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur))
    return parts


def _scalar(raw: str) -> Any:
    s = raw.strip()
    if s == "" or s in ("null", "~", "None"):
        return None
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    m = _INLINE_LIST.match(s)
    if m:
        inner = m.group(1).strip()
        return [] if not inner else [_scalar(x) for x in _split_top_level(inner)]
    m = _INLINE_MAP.match(s)
    if m:
        inner = m.group(1).strip()
        out: dict[str, Any] = {}
        for kv in _split_top_level(inner):
            k, _, v = kv.partition(":")
            if k.strip():
                out[k.strip()] = _scalar(v)
        return out
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if _INT.match(s):
        return int(s)
    if _FLOAT.match(s):
        return float(s)
    return s


def _strip_comment(line: str) -> str:
    # drop ' # comment' outside quotes (good enough for our config files)
    out, quote = [], None
    for i, ch in enumerate(line):
        if ch in "\"'" and quote is None:
            quote = ch
        elif ch == quote:
            quote = None
        elif ch == "#" and quote is None and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def load_yaml(text: str) -> dict[str, Any]:
    """Parse the YAML subset used by .song/config.yml and artifact front-matter."""
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    lines = text.splitlines()
    for idx, raw in enumerate(lines):
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if line.lstrip(" ").startswith("\t"):
            raise ValueError(f"tabs are not allowed in YAML indentation (line {idx + 1})")
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if content.startswith("- "):
            item = _scalar(content[2:])
            if isinstance(parent, list):
                parent.append(item)
            continue
        key, _, val = content.partition(":")
        key = key.strip()
        val = val.strip()
        if not isinstance(parent, dict):
            continue
        if val == "":
            # container or null: peek at the next non-blank, non-comment line
            nxt = next((l for l in lines[idx + 1:] if l.strip() and not l.strip().startswith("#")), "")
            nxt_indent = len(nxt) - len(nxt.lstrip(" "))
            if not nxt.strip() or nxt_indent <= indent:
                parent[key] = None
                continue
            child: Any = [] if nxt.strip().startswith("- ") else {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _scalar(val)
    return root


def load_config(path: str | None) -> dict[str, Any]:
    """Load .song/config.yml. No path yields {}; an explicit path that cannot be
    read raises FileNotFoundError so the gate reports ERROR instead of silently
    running with built-in thresholds. Tabs or malformed lines raise ValueError."""
    if not path:
        return {}
    data = load_yaml(read_text(path))
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
_NO_DEFAULT = object()


def resolve_threshold(
    key: str,
    config: dict[str, Any],
    genre: str | None,
    flag_value: Any = None,
    section: str = "quality",
    default: Any = _NO_DEFAULT,
    kind: type | None = None,
) -> Any:
    """Resolve a threshold by precedence. ``kind`` (int, float, bool) validates
    and coerces the value, raising ValueError (-> ERROR) on a bad config value."""
    value: Any = _NO_DEFAULT
    if flag_value is not None:
        value = flag_value
    else:
        sect = config.get(section, {}) if isinstance(config, dict) else {}
        if not isinstance(sect, dict):
            sect = {}
        if genre and section == "quality":
            overrides = sect.get("genre_overrides", {}) or {}
            g = overrides.get(genre) if isinstance(overrides, dict) else None
            if isinstance(g, dict) and key in g:
                value = g[key]
        if value is _NO_DEFAULT and key in sect:
            value = sect[key]
        if value is _NO_DEFAULT:
            if default is not _NO_DEFAULT:
                value = default
            else:
                table = DEFAULT_QUALITY if section == "quality" else DEFAULT_ORIGINALITY
                value = table.get(key)
    if kind is not None and value is not None:
        if kind is bool:
            if isinstance(value, bool):
                return value
            if isinstance(value, str) and value.lower() in ("true", "false"):
                return value.lower() == "true"
            raise ValueError(f"threshold {key} must be a boolean, got {value!r}")
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValueError(f"threshold {key} must be a {kind.__name__}, got {value!r}")
        try:
            return kind(value)
        except (TypeError, ValueError):
            raise ValueError(f"threshold {key} must be a {kind.__name__}, got {value!r}") from None
    return value


# ---------------------------------------------------------------------------
# Artifact parsing
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split a Markdown artifact into (front-matter dict, body)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return load_yaml("\n".join(lines[1:i])), "\n".join(lines[i + 1:])
    return {}, text


def parse_header_keys(text: str) -> dict[str, Any]:
    """Parse leading ``key: value`` lines (structure.md, arrangement.md, chords.md)."""
    out: dict[str, Any] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s:
            if out:
                break
            continue
        if s.startswith("|") or s.startswith("[") or s.startswith("#"):
            break
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", s)
        if not m:
            break
        out[m.group(1)] = _scalar(m.group(2))
    return out


def is_separator_row(cells: list[str]) -> bool:
    """True for a Markdown table alignment row such as ``|---|:--:|``."""
    return all(set(c) <= set("-: ") for c in cells)


def parse_table(text: str) -> list[dict[str, str]]:
    """Parse the first Markdown pipe table into a list of row dicts keyed by header."""
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if header is not None and rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if is_separator_row(cells):
            continue
        rows.append({header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))})
    return rows


SECTION_TAG = re.compile(r"^\[([^\]]+)\]\s*$")


def parse_sections(text: str) -> list[tuple[str, list[str]]]:
    """Split a ``[Label]``-tagged artifact into (label, non-comment lines) in order."""
    sections: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        s = line.rstrip()
        m = SECTION_TAG.match(s.strip())
        if m:
            current = []
            sections.append((m.group(1).strip(), current))
            continue
        if current is None or not s.strip() or s.lstrip().startswith("#"):
            continue
        current.append(s.strip())
    return sections


def parse_meter_spec(spec: str) -> list[tuple[int, str]]:
    """``8/uSuSuSuS; 7/SuSuSuS`` -> [(8, 'uSuSuSuS'), (7, 'SuSuSuS')]."""
    out: list[tuple[int, str]] = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        count, _, stress = part.partition("/")
        out.append((int(count.strip()), stress.strip()))
    return out


def parse_structure(text: str) -> dict[str, Any]:
    """Return {'header': {...}, 'sections': [{'label', 'bars', 'meter': [(n, stress)], 'rhyme_scheme'}]}."""
    header = parse_header_keys(text)
    sections = []
    for row in parse_table(text):
        label = row.get("label", "")
        if not label:
            continue
        try:
            bars = int(row.get("bars", "0") or 0)
        except ValueError:
            bars = 0
        sections.append({
            "label": label,
            "bars": bars,
            "meter": parse_meter_spec(row.get("meter_spec", "")),
            "rhyme_scheme": row.get("rhyme_scheme", ""),
        })
    return {"header": header, "sections": sections}


def resolve_language(args_language: str | None, paths: list[str]) -> str:
    """``--language`` flag, else brief.md ``language``, else ``en``."""
    if args_language:
        return args_language.lower()
    brief = file_named(paths, "brief.md")
    if brief:
        try:
            fm, _ = parse_frontmatter(read_text(brief))
            lang = fm.get("language")
            if isinstance(lang, str) and lang:
                return lang.lower()
        except OSError:
            pass
    return "en"


def resolve_genre(args_genre: str | None, paths: list[str]) -> str | None:
    if args_genre:
        return args_genre.lower()
    brief = file_named(paths, "brief.md")
    if brief:
        try:
            fm, _ = parse_frontmatter(read_text(brief))
            g = fm.get("genre")
            if isinstance(g, str) and g:
                return g.lower()
        except OSError:
            pass
    return None


def load_list_file(path: Path) -> list[str]:
    """Non-comment, non-blank lines of a .txt data list."""
    try:
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except OSError:
        return []
    return [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
class GateResult:
    def __init__(self, script: str):
        self.script = script.removesuffix(".py")
        self.status = PASS
        self.thresholds: dict[str, Any] = {}
        self.metrics: dict[str, Any] = {}
        self.violations: list[dict[str, Any]] = []
        self.warnings: list[dict[str, Any]] = []

    def violate(self, location: str, reason: str, observed: Any = None, limit: Any = None) -> None:
        self.violations.append({"location": location, "reason": reason, "observed": observed, "limit": limit})
        if self.status not in (ERROR,):
            self.status = FAIL

    def warn(self, location: str, reason: str, observed: Any = None, limit: Any = None) -> None:
        self.warnings.append({"location": location, "reason": reason, "observed": observed, "limit": limit})
        self.metrics["warnings"] = len(self.warnings)

    def error(self, reason: str, location: str = "") -> "GateResult":
        self.status = ERROR
        self.violations.insert(0, {"location": location, "reason": reason, "observed": None, "limit": None})
        return self

    def skip(self, reason: str) -> "GateResult":
        self.status = SKIPPED
        self.metrics["skipped_reason"] = reason
        self.violations = []
        return self

    def to_dict(self) -> dict[str, Any]:
        d = {
            "script": self.script,
            "status": self.status,
            "thresholds": self.thresholds,
            "metrics": self.metrics,
            "violations": self.violations if self.status in (FAIL, ERROR) else [],
        }
        if self.warnings:
            d["warnings"] = self.warnings
        return d

    def emit(self, as_json: bool) -> int:
        d = self.to_dict()
        if as_json:
            sys.stdout.write(json.dumps(d, indent=2) + "\n")
        else:
            sys.stdout.write(f"{self.script}: {self.status}\n")
            for k, v in self.metrics.items():
                sys.stdout.write(f"  {k}: {v}\n")
            for v in d["violations"]:
                sys.stdout.write(f"  {v['location']}: {v['reason']} (observed={v['observed']}, limit={v['limit']})\n")
            for w in self.warnings:
                sys.stdout.write(f"  WARN {w['location']}: {w['reason']}\n")
        sys.stdout.flush()
        return EXIT[self.status]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser(script: str, description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=script, description=description)
    p.add_argument("--config", metavar="PATH", help=".song/config.yml (optional)")
    p.add_argument("--json", action="store_true", help="emit the JSON result on stdout")
    p.add_argument("--genre", metavar="GENRE", help="genre for quality.genre_overrides (else brief.md)")
    p.add_argument("--language", metavar="CODE", help="lyric language (else brief.md language, else en)")
    p.add_argument("paths", nargs="*", metavar="ARTIFACT", help="artifact paths")
    return p


def run(script: str, description: str, add_args: Callable[[argparse.ArgumentParser], None] | None,
        main_fn: Callable[[argparse.Namespace, dict[str, Any], GateResult], GateResult],
        argv: list[str] | None = None) -> int:
    """Standard entry point: parse args, load config, call main_fn, emit, return exit code."""
    parser = build_parser(script, description)
    if add_args:
        add_args(parser)
    args = parser.parse_args(argv)
    args.paths = [norm(p) for p in args.paths]
    result = GateResult(script)
    try:
        config = load_config(args.config)
        result = main_fn(args, config, result)
    except FileNotFoundError as exc:
        result.error(f"file not found: {exc.filename or args.config}")
    except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError) as exc:
        if result.status != ERROR:
            result.error(f"{type(exc).__name__}: {exc}")
    return result.emit(args.json)


__all__ = [
    "PASS", "FAIL", "SKIPPED", "ERROR", "EXIT", "DEFAULT_QUALITY", "DEFAULT_ORIGINALITY",
    "SCRIPTS_DIR", "PLUGIN_ROOT", "SHARED_DIR", "DATA_DIR",
    "norm", "read_text", "file_named", "load_yaml", "load_config", "resolve_threshold",
    "parse_frontmatter", "parse_header_keys", "parse_table", "parse_sections", "parse_meter_spec",
    "parse_structure", "resolve_language", "resolve_genre", "load_list_file", "is_separator_row",
    "GateResult", "build_parser", "run",
]
