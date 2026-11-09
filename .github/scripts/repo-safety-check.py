#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

CAMPAIGN_GITIGNORE = {
    "config.bat",
    "temp_auto_push.bat",
    "temp_interactive_push.bat",
    "branch_structure.json",
}

FONT_MAGIC = {
    ".woff": b"wOFF",
    ".woff2": b"wOF2",
}

DISGUISED_EXTENSIONS = {".orc"}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


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
        if not path.is_file() or ".git" in path.parts:
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


def main() -> int:
    check_settings()
    check_tasks()
    check_fonts()
    check_gitignore()
    for error in errors:
        print(f"::error::{error}")
    if errors:
        print(f"{len(errors)} repository safety problem(s) found.")
        return 1
    print("Repository safety check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
