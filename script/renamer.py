#!/user/bin/env python3

from pathlib import Path

def main(root: Path) -> None:
    for p in root.rglob("*"):
        print(p.name)


if __name__ == "__main__":
    root = Path("~/tools_for_kr/test_directory")
    main(root)
