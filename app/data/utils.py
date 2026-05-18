import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
from shapely.ops import split


MAX_THRESHOLD = 0.10*10**6
MIN_THRESHOLD = 0.04*10**6


def remove_slivers(gdf: gpd.GeoDataFrame, minArea: float) -> gpd.GeoDataFrame:
    """
    Fjerner små polygoner (slivers) fra en GeoDataFrame og slår dem sammen med 
    det tilstøtende polygonet som de deler lengst grense med."""
    small_polygons = gdf[gdf.area < minArea*1000]
    big_polygons = gdf[gdf.area >= minArea*1000].copy()
    for idx, poly in small_polygons.iterrows():
        edge_intersections = big_polygons.geometry.intersection(poly.geometry)
        if edge_intersections.length.max() <= 0:
            continue
        best_match_idx = edge_intersections.length.idxmax()
        big_polygons.at[best_match_idx, "geometry"] = big_polygons.at[best_match_idx, "geometry"].union(poly.geometry)
    return big_polygons


def slice_polys(gdf: gpd.GeoDataFrame, maxArea: float) -> gpd.GeoDataFrame:
    """
    Deler opp polygoner som er større enn en gitt arealgrense.

    Funksjonen looper gjennom polygoner og deler dem i to (enten vertikalt 
    eller horisontalt basert på formen) via polygonets sentroid, helt til 
    ingen polygoner i datasettet har et areal som overstiger maxArea * 1000."""
    big_polygons = gdf[gdf.area >= maxArea*1000].copy()
    while not big_polygons.empty:
        new_rows = []
        for idx, poly in big_polygons.iterrows():
            min_x, min_y, max_x, max_y = poly.geometry.bounds
            poly_width = max_x - min_x
            poly_height = max_y - min_y
            poly_centroid = poly.geometry.centroid
            if poly_width > poly_height:
                mid_x = (min_x + max_x) / 2
                slice_line = LineString([(mid_x, min_y - 10), (poly_centroid.x, poly_centroid.y) , (mid_x, max_y + 10)])
                result = list(split(poly.geometry, slice_line).geoms)
                gdf.at[idx, "geometry"] = result[0]
                for additional_result in result[1:]:
                    new_row = poly.copy()
                    new_row.geometry = additional_result
                    new_rows.append(new_row)
            elif poly_width <= poly_height:
                mid_y = (min_y + max_y) / 2
                slice_line = LineString([(min_x - 10, mid_y), (poly_centroid.x, poly_centroid.y), (max_x + 10, mid_y)])
                result = list(split(poly.geometry, slice_line).geoms)
                gdf.at[idx, "geometry"] = result[0]
                for additional_result in result[1:]:
                    new_row = poly.copy()
                    new_row.geometry = additional_result
                    new_rows.append(new_row)
        if new_rows:
            new_gdf = gpd.GeoDataFrame(new_rows, crs=gdf.crs)
            gdf = pd.concat([gdf, new_gdf], ignore_index=True)
        big_polygons = gdf[gdf.area >= maxArea*1000].copy()
    return gdf


def parse_search_areas(search_areas: list[dict], minArea: float, maxArea: float) -> gpd.GeoDataFrame:
    """
    Postprosesserer søketeiger ved å fjerne små polygoner, og dele opp for store polygoner.

    Metoden antar at input-dataene er i EPSG:25833 (UTM sone 33N) for arealkalkulasjoner, 
    og transformerer resultatet til EPSG:4326 (WGS84) før det returneres som en GeoJSON-lignende dict."""
    gdf = gpd.GeoDataFrame.from_features(search_areas)
    gdf = remove_slivers(gdf, minArea)
    gdf = slice_polys(gdf, maxArea)
    return gdf.set_crs(epsg=25833).to_crs(epsg=4326).to_geo_dict()
