#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from typing import Iterator

IS_DRY_RUN=False # This is bad, but I don't care.

def cli() -> ArgumentParser:
    parser = ArgumentParser(
        description="Program to clean up KR's iphone live images.")

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Print out what the tool would do."
    )

    parser.add_argument(
        "root",
        type=Path,
    )

    return parser


def all_not_dirs(root: Path) -> Iterator[Path]:
    for p in filter(lambda p: not p.is_dir(), root.rglob("*")):
        yield p.resolve()


def rm(p: Path) -> None:
    if IS_DRY_RUN:
        print(f"Removing {p}")
    else:
        p.unlink()


def rename(old: Path, new: Path) -> None:
    if IS_DRY_RUN:
        print(f"Renaming {old}\n  to {new}")
    else:
        old.rename(new)


def remove_apple_hidden_file(p: Path) -> None:
    if len(p.name) < 2: return

    should_remove = p.name[:2] == "._"

    if should_remove:
        rm(p)


def make_extension_lowercase(p: Path) -> None:
    if len(p.suffixes) != 1:
        return

    lower_case_version = p.with_suffix(p.suffix.lower())

    if p == lower_case_version:
        return

    rename(p, lower_case_version)


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
        rm(mov)
    elif exists[m4v] and exists[mov]:
        rm(m4v)


def main(root: Path) -> None:
    if IS_DRY_RUN:
        print("Running in test mode.  All actions are simulated")

    on_all_not_dirs = lambda op: list(map(op, all_not_dirs(root)))

    on_all_not_dirs(remove_apple_hidden_file)
    on_all_not_dirs(make_extension_lowercase)
    on_all_not_dirs(remove_unwanted_files)


if __name__ == "__main__":
    args = cli().parse_args()
    IS_DRY_RUN = args.dry_run
    main(args.root)
