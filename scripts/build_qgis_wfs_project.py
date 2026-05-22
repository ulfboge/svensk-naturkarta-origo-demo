#!/usr/bin/env python3
"""Build GeoPackage + QGIS project and sync Origo WFS layers for all counties."""

from __future__ import annotations

import json
import uuid
from copy import deepcopy
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[1]
SERVER_DIR = ROOT / "qgis" / "server"
DATA_DIR = SERVER_DIR / "data"
GPKG_PATH = DATA_DIR / "naturkarta.gpkg"
QGS_PATH = SERVER_DIR / "naturkarta.qgs"
ORIGO_JSON = ROOT / "public" / "config" / "origo.json"

EPSG3857_WKT = (
    'PROJCRS["WGS 84 / Pseudo-Mercator",BASEGEOGCRS["WGS 84",ENSEMBLE["World Geodetic System 1984 ensemble",'
    'MEMBER["World Geodetic System 1984 (Transit)"],MEMBER["World Geodetic System 1984 (G730)"],'
    'MEMBER["World Geodetic System 1984 (G873)"],MEMBER["World Geodetic System 1984 (G1150)"],'
    'MEMBER["World Geodetic System 1984 (G1674)"],MEMBER["World Geodetic System 1984 (G1762)"],'
    'MEMBER["World Geodetic System 1984 (G2139)"],MEMBER["World Geodetic System 1984 (G2296)"],'
    'ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]],ENSEMBLEACCURACY[2.0]],'
    'PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4326]],'
    'CONVERSION["Popular Visualisation Pseudo-Mercator",METHOD["Popular Visualisation Pseudo Mercator",ID["EPSG",1024]],'
    'PARAMETER["Latitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8801]],'
    'PARAMETER["Longitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8802]],'
    'PARAMETER["False easting",0,LENGTHUNIT["metre",1],ID["EPSG",8806]],'
    'PARAMETER["False northing",0,LENGTHUNIT["metre",1],ID["EPSG",8807]]],'
    'CS[Cartesian,2],AXIS["easting (X)",east,ORDER[1],LENGTHUNIT["metre",1]],'
    'AXIS["northing (Y)",north,ORDER[2],LENGTHUNIT["metre",1]],'
    'USAGE[SCOPE["Web mapping and visualisation."],AREA["World between 85.06°S and 85.06°N."],'
    'BBOX[-85.06,-180,85.06,180]],ID["EPSG",3857]]'
)


def layer_id(name: str) -> str:
    return f"{name}_{uuid.uuid5(uuid.NAMESPACE_DNS, name).hex[:8]}"


def qgs_field_type(dtype) -> str:
    name = str(dtype)
    if "int" in name:
        return "Integer"
    if "float" in name:
        return "Real"
    return "String"


def discover_layers_from_origo() -> list[dict]:
    cfg = json.loads(ORIGO_JSON.read_text(encoding="utf-8"))
    layers = []
    for layer in cfg["layers"]:
        name = layer.get("name", "")
        if not name.startswith("nv_naturreservat_"):
            continue
        if layer.get("type") != "GEOJSON":
            continue
        src = layer.get("source", "")
        if not src.endswith(".geojson"):
            continue
        path = ROOT / "public" / src
        if not path.exists():
            print(f"WARNING: missing {path.name}, skipping")
            continue
        slug = Path(src).stem.replace("naturreservat-", "")
        layers.append(
            {
                "geojson": path,
                "layer_name": f"naturreservat_{slug}",
                "title": layer.get("title", slug),
                "origo_suffix": name.replace("nv_naturreservat_", ""),
                "attributes": deepcopy(layer.get("attributes", [])),
                "featureinfoTitle": layer.get("featureinfoTitle", "NAMN"),
            }
        )
    return layers


def wfs_title_from_geojson(title: str) -> str:
    cleaned = title.replace(" – ", " ").replace(" län", "").strip()
    if "(WFS live)" in cleaned:
        return cleaned
    return f"{cleaned} (WFS live)"


def make_wfs_layer(spec: dict) -> dict:
    suffix = spec["origo_suffix"]
    return {
        "name": f"nv_wfs_{suffix}",
        "id": spec["layer_name"],
        "title": wfs_title_from_geojson(spec["title"]),
        "group": "naturreservat_group",
        "type": "WFS",
        "source": "local_qgis_wfs",
        "strategy": "all",
        "visible": False,
        "queryable": True,
        "zIndex": 11,
        "style": "naturreservat_polygon",
        "attributes": spec["attributes"],
        "featureinfoTitle": spec["featureinfoTitle"],
    }


def sync_origo_wfs_layers(county_layers: list[dict]) -> None:
    cfg = json.loads(ORIGO_JSON.read_text(encoding="utf-8"))
    wfs_by_suffix = {spec["origo_suffix"]: make_wfs_layer(spec) for spec in county_layers}

    cfg["layers"] = [layer for layer in cfg["layers"] if not layer.get("name", "").startswith("nv_wfs_")]

    updated = []
    for layer in cfg["layers"]:
        updated.append(layer)
        name = layer.get("name", "")
        if name.startswith("nv_naturreservat_") and layer.get("type") == "GEOJSON":
            suffix = name.replace("nv_naturreservat_", "")
            if suffix in wfs_by_suffix:
                updated.append(wfs_by_suffix[suffix])

    cfg["layers"] = updated
    ORIGO_JSON.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Synced {len(wfs_by_suffix)} WFS layers in {ORIGO_JSON.name}")


def build_field_definitions(gdf: gpd.GeoDataFrame) -> str:
    parts = ["    <attributeTable>"]
    for col in gdf.columns:
        if col == "geometry":
            continue
        parts.append(
            f'      <field configurationFlags="NoFlag" name="{col}" type="{qgs_field_type(gdf[col].dtype)}"/>'
        )
    parts.append("    </attributeTable>")
    return "\n".join(parts)


def build_maplayer(meta: dict, gdf: gpd.GeoDataFrame) -> str:
    lid = layer_id(meta["layer_name"])
    bounds = gdf.total_bounds
    wgs = gdf.to_crs(4326).total_bounds
    geom_type = gdf.geometry.geom_type.iloc[0]
    wkb = "MultiPolygon" if "Multi" in geom_type else "Polygon"
    datasource = f"./data/naturkarta.gpkg|layername={meta['layer_name']}"

    return f"""    <maplayer autoRefreshMode="Disabled" autoRefreshTime="0" geometry="Polygon" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" maxScale="0" minScale="100000000" readOnly="0" simplifyAlgorithm="0" simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1" styleCategories="AllStyleCategories" symbologyReferenceScale="-1" type="vector" wkbType="{wkb}">
      <extent>
        <xmin>{bounds[0]}</xmin>
        <ymin>{bounds[1]}</ymin>
        <xmax>{bounds[2]}</xmax>
        <ymax>{bounds[3]}</ymax>
      </extent>
      <wgs84extent>
        <xmin>{wgs[0]}</xmin>
        <ymin>{wgs[1]}</ymin>
        <xmax>{wgs[2]}</xmax>
        <ymax>{wgs[3]}</ymax>
      </wgs84extent>
      <id>{lid}</id>
      <datasource>{datasource}</datasource>
      <layername>{meta['layer_name']}</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <wkt>{EPSG3857_WKT}</wkt>
          <proj4>+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs</proj4>
          <srsid>3857</srsid>
          <srid>3857</srid>
          <authid>EPSG:3857</authid>
          <description>WGS 84 / Pseudo-Mercator</description>
          <projectionacronym>merc</projectionacronym>
          <ellipsoidacronym>EPSG:7030</ellipsoidacronym>
          <geographicflag>false</geographicflag>
        </spatialrefsys>
      </srs>
      <provider encoding="UTF-8">ogr</provider>
      <flags>
        <Identifiable>1</Identifiable>
        <Removable>1</Removable>
        <Searchable>1</Searchable>
        <Private>0</Private>
      </flags>
{build_field_definitions(gdf)}
      <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
        <symbols>
          <symbol clip_to_extent="1" type="fill" name="0" alpha="1" force_rhr="0">
            <layer class="SimpleFill" pass="0" locked="0" enabled="1">
              <Option type="Map">
                <Option value="76,175,80,76,rgb:0.2980392,0.6862745,0.3137255,0.2980392" type="QString" name="color"/>
                <Option value="46,125,50,255,rgb:0.1803922,0.4901961,0.1960784,1" type="QString" name="outline_color"/>
                <Option value="0.4" type="QString" name="outline_width"/>
                <Option value="MM" type="QString" name="outline_width_unit"/>
                <Option value="solid" type="QString" name="style"/>
              </Option>
            </layer>
          </symbol>
        </symbols>
      </renderer-v2>
    </maplayer>"""


def build_project(layers: list[tuple[dict, gpd.GeoDataFrame]]) -> str:
    import pandas as pd

    all_gdf = gpd.GeoDataFrame(
        pd.concat([gdf for _, gdf in layers], ignore_index=True),
        crs=layers[0][1].crs,
    )
    bounds = all_gdf.total_bounds
    layer_tree = []
    maplayers = []
    wfs_ids = []

    for meta, gdf in layers:
        lid = layer_id(meta["layer_name"])
        wfs_ids.append(f"      <value>{lid}</value>")
        layer_tree.append(
            f'      <layer-tree-layer checked="Qt::Checked" expanded="1" id="{lid}" '
            f'name="{meta["title"]}" providerKey="ogr" '
            f'source="./data/naturkarta.gpkg|layername={meta["layer_name"]}"/>'
        )
        maplayers.append(build_maplayer(meta, gdf))

    return f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis saveDateTime="2026-05-22T12:00:00" version="3.34.0" projectname="Naturkarta WFS">
  <homePath path=""/>
  <title>Naturkarta WFS</title>
  <projectCrs>
    <spatialrefsys nativeFormat="Wkt">
      <wkt>{EPSG3857_WKT}</wkt>
      <proj4>+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs</proj4>
      <srsid>3857</srsid>
      <srid>3857</srid>
      <authid>EPSG:3857</authid>
      <description>WGS 84 / Pseudo-Mercator</description>
      <projectionacronym>merc</projectionacronym>
      <ellipsoidacronym>EPSG:7030</ellipsoidacronym>
      <geographicflag>false</geographicflag>
    </spatialrefsys>
  </projectCrs>
  <layer-tree-group checked="Qt::Checked" expanded="1" name="">
{chr(10).join(layer_tree)}
  </layer-tree-group>
  <mapcanvas name="theMapCanvas">
    <units>meters</units>
    <extent>
      <xmin>{bounds[0]}</xmin>
      <ymin>{bounds[1]}</ymin>
      <xmax>{bounds[2]}</xmax>
      <ymax>{bounds[3]}</ymax>
    </extent>
    <rotation>0</rotation>
  </mapcanvas>
  <projectlayers>
{chr(10).join(maplayers)}
  </projectlayers>
  <properties>
    <WFSLayers type="QStringList">
{chr(10).join(wfs_ids)}
    </WFSLayers>
    <WFSTLayers>
      <Delete type="QStringList"/>
      <Insert type="QStringList"/>
      <Update type="QStringList"/>
    </WFSTLayers>
    <WMSServiceTitle type="QString">Naturkarta WFS</WMSServiceTitle>
    <WMSServiceAbstract type="QString">WFS for svensk-naturkarta-origo-demo (all counties)</WMSServiceAbstract>
  </properties>
</qgis>
"""


def main() -> None:
    specs = discover_layers_from_origo()
    if not specs:
        raise SystemExit("No county GeoJSON layers found in origo.json")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if GPKG_PATH.exists():
        GPKG_PATH.unlink()

    built_layers: list[tuple[dict, gpd.GeoDataFrame]] = []
    total_features = 0
    for spec in specs:
        print(f"Loading {spec['geojson'].name}...")
        gdf = gpd.read_file(spec["geojson"])
        if gdf.crs is None:
            gdf = gdf.set_crs(4326)
        gdf = gdf.to_crs(3857)
        gdf.to_file(GPKG_PATH, layer=spec["layer_name"], driver="GPKG")
        built_layers.append((spec, gdf))
        total_features += len(gdf)
        print(f"  -> {len(gdf)} features as {spec['layer_name']}")

    QGS_PATH.write_text(build_project(built_layers), encoding="utf-8")
    sync_origo_wfs_layers(specs)
    print(f"Wrote {QGS_PATH} ({len(built_layers)} layers, {total_features} features)")
    print(f"Wrote {GPKG_PATH}")


if __name__ == "__main__":
    main()
