"""Build simplified county boundaries GeoJSON from SCB open data (CC0)."""
from __future__ import annotations

import json
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import fiona
from pyproj import Transformer
from shapely.geometry import mapping, shape
from shapely.ops import transform as shp_transform

SCB_ZIP = (
    "https://www.scb.se/contentassets/3443fea3fa6640f7a57ea15d9a372d33/"
    "shape_svenska_260225.zip"
)
OUT = Path(__file__).resolve().parents[1] / "public" / "data" / "lansgranser.geojson"

CODE_MAP = {
    "01": "sthlm", "03": "upp", "04": "sod", "05": "ost", "06": "jon", "07": "kro",
    "08": "kal", "09": "got", "10": "ble", "12": "skane", "13": "hal", "14": "vg",
    "17": "vrm", "18": "ore", "19": "vml", "20": "dal", "21": "gav", "22": "vnr",
    "23": "jam", "24": "vbo", "25": "nrb",
}
LAN_NAMES = {
    "sthlm": "Stockholms län", "upp": "Uppsala län", "sod": "Södermanlands län",
    "ost": "Östergötlands län", "jon": "Jönköpings län", "kro": "Kronobergs län",
    "kal": "Kalmar län", "got": "Gotlands län", "ble": "Blekinge län",
    "skane": "Skåne län", "hal": "Hallands län", "vg": "Västra Götalands län",
    "vrm": "Värmlands län", "ore": "Örebro län", "vml": "Västmanlands län",
    "dal": "Dalarnas län", "gav": "Gävleborgs län", "vnr": "Västernorrlands län",
    "jam": "Jämtlands län", "vbo": "Västerbottens län", "nrb": "Norrbottens län",
}


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        zip_path = root / "scb.zip"
        urllib.request.urlretrieve(SCB_ZIP, zip_path)
        with zipfile.ZipFile(zip_path) as outer:
            outer.extractall(root)
        lan_dir = root / "lan"
        lan_dir.mkdir()
        with zipfile.ZipFile(root / "LanSweref99TM.zip") as inner:
            inner.extractall(lan_dir)
        shp = lan_dir / "Lan_Sweref99TM_region.shp"

        tr = Transformer.from_crs("EPSG:3006", "EPSG:4326", always_xy=True)
        features = []
        with fiona.open(shp) as src:
            for feat in src:
                code = CODE_MAP.get(feat["properties"]["LnKod"])
                if not code:
                    continue
                geom = shp_transform(tr.transform, shape(feat["geometry"]))
                geom = geom.simplify(0.002, preserve_topology=True)
                features.append(
                    {
                        "type": "Feature",
                        "id": code,
                        "properties": {
                            "county": code,
                            "LAN": LAN_NAMES[code],
                            "LnKod": feat["properties"]["LnKod"],
                        },
                        "geometry": mapping(geom),
                    }
                )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh, ensure_ascii=False)
    print(f"Wrote {len(features)} counties to {OUT}")


if __name__ == "__main__":
    main()
