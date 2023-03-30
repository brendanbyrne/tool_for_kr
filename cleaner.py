#!/usr/bin/env python3

from pathlib import Path
from typing import Iterator

ROOT = Path("/home/bbyrne/projects/tool_for_kr/test_directory")
TEST_MODE=True

def all_not_dirs(root: Path) -> Iterator[Path]:
    for p in root.rglob("*"):
        if p.is_dir(): continue
        yield p.resolve()


def safe_rm(p: Path) -> None:
    if TEST_MODE:
        print(f"Removing {p}")
    else:
        p.unlink()


def safe_rename(old: Path, new: Path) -> None:
    if TEST_MODE:
        print(f"Renaming {old}\n  to {new}")
    else:
        old.rename(new)


def remove_apple_hidden_file(p: Path) -> None:
    if len(p.name) < 2: return

    should_remove = p.name[:2] == "._"

    if should_remove:
        safe_rm(p)


def make_extension_lowercase(p: Path) -> None:
    if len(p.suffixes) != 1:
        return

    lower_case_version = p.parent / (p.stem + p.suffix.lower())

    if p == lower_case_version:
        print(f"Already matches")
        return

    safe_rename(p, lower_case_version)


def remove_unwanted_files(p: Path) -> None:
    jpg = p.with_suffix(".jpg")
    mov = p.with_suffix(".mov")
    m4v = p.with_suffix(".m4v")

    exists = {
        jpg: jpg.is_file(),
        mov: mov.is_file(),
        m4v: m4v.is_file(),
    }

    if sum(exists.values()) != 2:
        return

    if exists[jpg] and exists[mov]:
        safe_rm(mov)
    if exists[m4v] and exists[mov]:
        safe_rm(m4v)


def main() -> None:
    # Remove all of the apple hidden files
    print("Removing all apple hidden files")
    for p in all_not_dirs(ROOT):
        remove_apple_hidden_file(p)

    # Makes all extensions lowercase for consistency
    print("Making all extensions lowercase")
    for p in all_not_dirs(ROOT):
        make_extension_lowercase(p)

    # Remove unwanted files
    for p in all_not_dirs(ROOT):
        remove_unwanted_files(p)


if __name__ == "__main__":
    if TEST_MODE: print("Running in test mode.  All actions are simulated")

    main()
