import geopandas as gpd


def parse_search_areas(search_areas: list[dict]) :
    gdf = gpd.GeoDataFrame.from_features(search_areas)
    small_polys = gdf[gdf.area < 1]
    return gdf.set_crs(epsg=25833).to_crs(epsg=4326).to_geo_dict()