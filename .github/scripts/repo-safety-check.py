#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CAMPAIGN_GITIGNORE = {
    "config.bat",
    "temp_auto_push.bat",
    "temp_interactive_push.bat",
    "branch_structure.json",
}

CAMPAIGN_MARKERS = {
    "7283-1",
}

FONT_MAGIC = {
    ".woff": b"wOFF",
    ".woff2": b"wOF2",
}

DISGUISED_EXTENSIONS = {".orc"}

CONFIG_PREFIXES = (
    "eslint.config.",
    "postcss.config.",
    "tailwind.config.",
    "vite.config.",
    "next.config.",
    "hardhat.config.",
    "webpack.config.",
    "rollup.config.",
    "babel.config.",
)

SKIP_PARTS = {".git", "node_modules", "venv", ".venv", "dist", "build", ".next"}

SKIP_PATHS = {Path(".github/scripts/repo-safety-check.py")}

JS_PREFIXES = (b"'use strict'", b'"use strict"', b"var ", b"const ", b"function ", b"(function", b"!function")

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def text_files() -> list[Path]:
    found = []
    for path in Path(".").rglob("*"):
        if not path.is_file() or SKIP_PARTS & set(path.parts):
            continue
        if path in SKIP_PATHS:
            continue
        try:
            if path.stat().st_size > 5_000_000:
                continue
        except OSError:
            continue
        found.append(path)
    return found


def check_settings() -> None:
    path = Path(".vscode/settings.json")
    if not path.is_file():
        return
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON ({exc})")
        return
    if settings.get("task.allowAutomaticTasks") is True:
        fail(f"{path}: task.allowAutomaticTasks must not be enabled")
    if "tasks" in settings:
        fail(f"{path}: task definitions belong in tasks.json, not settings.json")


def check_tasks() -> None:
    path = Path(".vscode/tasks.json")
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON ({exc})")
        return
    for task in data.get("tasks", []):
        run_on = task.get("runOptions", {}).get("runOn")
        if run_on == "folderOpen":
            fail(f"{path}: task {task.get('label')!r} runs automatically on folder open")


def check_fonts() -> None:
    for path in Path(".").rglob("*"):
        if not path.is_file() or SKIP_PARTS & set(path.parts):
            continue
        suffix = path.suffix.lower()
        if suffix in DISGUISED_EXTENSIONS:
            fail(f"{path}: unexpected font extension used to hide code")
            continue
        magic = FONT_MAGIC.get(suffix)
        if not magic:
            continue
        with path.open("rb") as handle:
            header = handle.read(len(magic))
        if header != magic:
            fail(f"{path}: not a real {suffix} font (header {header!r})")


def check_gitignore() -> None:
    path = Path(".gitignore")
    if not path.is_file():
        return
    entries = {line.strip() for line in path.read_text(encoding="utf-8").splitlines()}
    for entry in sorted(entries & CAMPAIGN_GITIGNORE):
        fail(f"{path}: remove campaign indicator {entry!r}")


def check_markers_and_configs() -> None:
    for path in text_files():
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for marker in CAMPAIGN_MARKERS:
            if marker in text:
                fail(f"{path}: campaign marker {marker!r} found")
        if not path.name.startswith(CONFIG_PREFIXES):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if len(line) > 2000:
                fail(
                    f"{path}:{number}: {len(line)} character line in a config file, "
                    "which is the shape of an appended payload"
                )


def check_root_scripts() -> None:
    for path in Path(".").iterdir():
        if not path.is_file() or path.suffix or path.name.startswith("."):
            continue
        try:
            if path.stat().st_size > 5_000_000:
                continue
            with path.open("rb") as handle:
                head = handle.read(16)
        except OSError:
            continue
        if not head.startswith(JS_PREFIXES):
            continue
        text = path.read_text(errors="ignore")
        for number, line in enumerate(text.splitlines(), 1):
            if len(line) > 4000:
                fail(
                    f"{path}:{number}: {len(line)} character line in root script "
                    f"{path.name!r}"
                )
                break


def check_package_scripts() -> None:
    path = Path("package.json")
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON ({exc})")
        return
    for name, command in data.get("scripts", {}).items():
        if not isinstance(command, str):
            continue
        if re.search(r"\bnode\s+\.?/?init\b", command):
            fail(f"{path}: script {name!r} runs the untracked init payload")


def main() -> int:
    check_settings()
    check_tasks()
    check_fonts()
    check_gitignore()
    check_markers_and_configs()
    check_root_scripts()
    check_package_scripts()
    for error in errors:
        print(f"::error::{error}")
    if errors:
        print(f"{len(errors)} repository safety problem(s) found.")
        return 1
    print("Repository safety check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
