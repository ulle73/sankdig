#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

LOCAL_JSON = Path(r"C:/Users/ryd/repos/golf-instagram/data/golf_karuseller_100.json")
REPO_JSON = Path(r"C:/Users/ryd/repos/sankdig-upload/data/golf_karuseller_100.json")


def update_file(path: Path, carousel_id: int) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    now = datetime.now(timezone.utc).isoformat()

    for item in data.get("karuseller", []):
        if int(item.get("id", -1)) == carousel_id:
            item["used"] = True
            item["used_at"] = now
            changed = True
            break

    if not changed:
        raise SystemExit(f"Carousel id {carousel_id} not found in {path}")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mark a carousel as used in local and repo JSON copies")
    parser.add_argument("id", type=int, help="Carousel id to mark as used")
    parser.add_argument("--local-json", default=str(LOCAL_JSON), help="Local JSON path")
    parser.add_argument("--repo-json", default=str(REPO_JSON), help="Repo JSON path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    local = Path(args.local_json)
    repo = Path(args.repo_json)

    update_file(local, args.id)
    update_file(repo, args.id)

    print(json.dumps({"status": "ok", "id": args.id, "local": str(local), "repo": str(repo)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
