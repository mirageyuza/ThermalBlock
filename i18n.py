#!/usr/bin/env python3
"""
i18n.py — ThermalBlock Language Pack Generator & Builder

Reads tpe_manager_v4.py, replaces all Chinese string literals with translations
from lang/<code>.json, then optionally builds an EXE via PyInstaller.
After building, the original source file is restored.

Usage:
    python i18n.py --list              List available language packs
    python i18n.py --lang de --build   Build German version
    python i18n.py --all               Build all available languages
    python i18n.py --init-zh           Generate lang/zh.json template from source
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
SRC_FILE = SCRIPT_DIR / "tpe_manager_v4.py"
LANG_DIR = SCRIPT_DIR / "lang"
OUTPUT_DIR = SCRIPT_DIR / "output" / "dist" / "i18n"
BACKUP_FILE = SCRIPT_DIR / "tpe_manager_v4.py.bak"

# Chinese character + punctuation regex for extraction
# Matches contiguous runs of CJK Unified Ideographs, plus common CJK punctuation
CHINESE_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3000-\u303f\uff00-\uffef\u2000-\u206f]+")

# Regex to match Python string literals containing Chinese
# Captures: single-quoted, double-quoted, triple-quoted strings with Chinese content
STRING_RE = re.compile(
    r"""(?P<quote>['\"]{1,3})         # opening quote (captured)
        (?P<body>                     # string body
            (?:[^\\]|\\.)*?           # content (lazy), handles escapes
            [\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+  # at least one CJK char
            (?:[^\\]|\\.)*?           # rest of content
        )
        (?P=quote)                    # matching closing quote
    """,
    re.VERBOSE,
)

# ---------------------------------------------------------------------------
# Language metadata
# ---------------------------------------------------------------------------

LANG_META = {
    "zh": {"name": "Chinese (Simplified)", "native": "简体中文"},
    "en": {"name": "English", "native": "English"},
    "de": {"name": "German", "native": "Deutsch"},
    "fr": {"name": "French", "native": "Français"},
    "es": {"name": "Spanish", "native": "Español"},
    "pt": {"name": "Portuguese (Brazilian)", "native": "Português"},
    "ja": {"name": "Japanese", "native": "日本語"},
    "ko": {"name": "Korean", "native": "한국어"},
    "ru": {"name": "Russian", "native": "Русский"},
    "ar": {"name": "Arabic", "native": "العربية"},
}


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def extract_chinese_strings(source_path: Path) -> dict:
    """Extract all unique Chinese string literals from source, return {zh_text: zh_text}."""
    content = source_path.read_text(encoding="utf-8")
    strings = set()
    for m in STRING_RE.finditer(content):
        body = m.group("body")
        # Unescape common Python escape sequences for the key
        cleaned = body.encode("latin-1", errors="ignore").decode("unicode_escape", errors="replace")
        # Only keep if it contains CJK
        if CHINESE_RE.search(cleaned):
            strings.add(cleaned)
    # Sort for reproducibility; return as identity dict
    return {s: s for s in sorted(strings, key=len, reverse=True)}


def load_lang_pack(lang_code: str) -> dict:
    """Load a language pack JSON file."""
    path = LANG_DIR / f"{lang_code}.json"
    if not path.exists():
        raise FileNotFoundError(f"Language pack not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_lang_pack(lang_code: str, data: dict):
    """Save a language pack JSON file."""
    LANG_DIR.mkdir(parents=True, exist_ok=True)
    path = LANG_DIR / f"{lang_code}.json"
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[OK] Saved {path}")


def replace_strings_in_file(source_path: Path, mapping: dict) -> Path:
    """Replace Chinese strings in source with translations, write to temp file.
    Returns the temp file path.
    """
    content = source_path.read_text(encoding="utf-8")

    # Sort keys by length descending to avoid partial replacements
    for zh_text in sorted(mapping.keys(), key=len, reverse=True):
        translated = mapping[zh_text]
        if zh_text == translated:
            continue  # skip untranslated entries (keep original)
        # Escape for literal replacement in Python source context
        # We replace the raw string content inside quotes
        content = content.replace(zh_text, translated)

    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".py", delete=False, dir=SCRIPT_DIR
    )
    tmp.write(content)
    tmp.flush()
    return Path(tmp.name)


def build_exe(source_path: Path, lang_code: str):
    """Run PyInstaller to build the EXE."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    exe_name = f"TPE_Manager_{lang_code}"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        f"--name={exe_name}",
        f"--distpath={OUTPUT_DIR}",
        str(source_path),
    ]

    print(f"[BUILD] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(SCRIPT_DIR))

    if result.returncode != 0:
        print(f"[ERROR] PyInstaller failed:\n{result.stderr}")
        raise RuntimeError("Build failed")
    print(f"[OK] Built {OUTPUT_DIR / exe_name}.exe")


def restore_source(backup_path: Path, target_path: Path):
    """Restore original source from backup."""
    if backup_path.exists():
        shutil.copy(str(backup_path), str(target_path))
        backup_path.unlink()
        print("[OK] Source file restored.")


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_list():
    """List available language packs."""
    if not LANG_DIR.exists():
        print("No language packs found. Run --init-zh first.")
        return

    packs = sorted(LANG_DIR.glob("*.json"))
    if not packs:
        print("No language packs found. Run --init-zh first.")
        return

    print(f"{'Code':<6} {'Language':<30} {'Native Name'}")
    print("-" * 56)
    for p in packs:
        code = p.stem
        meta = LANG_META.get(code, {"name": "Unknown", "native": ""})
        print(f"{code:<6} {meta['name']:<30} {meta['native']}")


def cmd_init_zh():
    """Generate lang/zh.json template from source chinese strings."""
    if not SRC_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {SRC_FILE}")

    strings = extract_chinese_strings(SRC_FILE)
    if not strings:
        print("[WARN] No Chinese strings found in source.")
        return

    save_lang_pack("zh", strings)
    print(f"[INFO] Extracted {len(strings)} unique Chinese strings to lang/zh.json")


def cmd_build(lang_code: str):
    """Build EXE for a specific language."""
    if not SRC_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {SRC_FILE}")

    # Backup original
    shutil.copy(str(SRC_FILE), str(BACKUP_FILE))
    print(f"[INFO] Backed up original to {BACKUP_FILE}")

    try:
        # Load language pack
        pack = load_lang_pack(lang_code)
        print(f"[INFO] Loaded {len(pack)} translations for '{lang_code}'")

        if lang_code == "zh":
            print("[INFO] Source language is Chinese — skipping replacement, building directly.")
            build_exe(SRC_FILE, lang_code)
        else:
            # Create temp file with translations
            tmp_path = replace_strings_in_file(SRC_FILE, pack)
            # Overwrite source with translated version
            shutil.copy(str(tmp_path), str(SRC_FILE))
            tmp_path.unlink()

            # Build
            build_exe(SRC_FILE, lang_code)

    finally:
        restore_source(BACKUP_FILE, SRC_FILE)


def cmd_all():
    """Build EXEs for all available language packs."""
    if not LANG_DIR.exists():
        raise FileNotFoundError("No lang/ directory found. Run --init-zh first.")

    packs = [p.stem for p in sorted(LANG_DIR.glob("*.json"))]
    if not packs:
        raise FileNotFoundError("No language packs found. Run --init-zh first.")

    # Always build zh first (creates template for others if missing)
    if "zh" not in packs:
        print("[WARN] zh.json not found, generating from source first...")
        cmd_init_zh()
        packs.insert(0, "zh")

    for code in packs:
        print(f"\n{'='*60}")
        print(f"  Building: {LANG_META.get(code, {}).get('name', code)} ({code})")
        print(f"{'='*60}")
        try:
            cmd_build(code)
        except Exception as e:
            print(f"[ERROR] Failed to build '{code}': {e}")
            continue

    print(f"\n[OK] All builds complete. Output: {OUTPUT_DIR}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ThermalBlock i18n — Language pack generator & builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python i18n.py --init-zh        Generate lang/zh.json template
  python i18n.py --list           List available languages
  python i18n.py --lang de        Build German EXE
  python i18n.py --all            Build all languages
        """,
    )

    parser.add_argument("--list", action="store_true", help="List available language packs")
    parser.add_argument("--init-zh", action="store_true", help="Generate lang/zh.json from source")
    parser.add_argument("--lang", type=str, metavar="CODE", help="Language code to build (e.g. de, fr, ja)")
    parser.add_argument("--all", action="store_true", help="Build EXEs for all available languages")

    args = parser.parse_args()

    if args.list:
        cmd_list()
    elif args.init_zh:
        cmd_init_zh()
    elif args.lang:
        cmd_build(args.lang)
    elif args.all:
        cmd_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
