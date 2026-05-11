import geopandas as gpd


def parse_search_areas(search_areas: list[dict]) :
    gdf = gpd.GeoDataFrame.from_features(search_areas)
    small_polygons = gdf[gdf.area < 0.04*10**6]
    big_polygons = gdf[gdf.area >= 0.04*10**6].copy()
    for idx, poly in small_polygons.iterrows():
        edge_intersections = big_polygons.geometry.intersection(poly.geometry)
        if edge_intersections.length.max() <= 0:
            continue
        best_match_idx = edge_intersections.length.idxmax()
        big_polygons.at[best_match_idx, "geometry"] = big_polygons.at[best_match_idx, "geometry"].union(poly.geometry)
    return big_polygons.set_crs(epsg=25833).to_crs(epsg=4326).to_geo_dict()
