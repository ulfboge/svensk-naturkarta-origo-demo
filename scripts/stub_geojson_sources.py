#!/usr/bin/env python3
"""Point GEOJSON county layers at empty.geojson for lazy loading (GEOJSON type only)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGO_JSON = ROOT / "public" / "config" / "origo.json"
EMPTY = "data/empty.geojson"


def main() -> None:
    data = json.loads(ORIGO_JSON.read_text(encoding="utf-8"))
    count = 0
    for layer in data["layers"]:
        name = layer.get("name", "")
        if layer.get("type") != "GEOJSON":
            continue
        if name.startswith("nv_naturreservat_") or name == "nv_nationalparker":
            layer["source"] = EMPTY
            count += 1
    ORIGO_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Stubbed {count} GEOJSON layers to {EMPTY}")


if __name__ == "__main__":
    main()
