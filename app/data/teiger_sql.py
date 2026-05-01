EMPTY_FEATURE_COLLECTION = {"type": "FeatureCollection", "features": []}

TEIGER_SQL_WITH_EXTEND = """
    WITH params AS (
        -- Input normaliseres til EPSG:25833 slik at avstand og areal regnes i meter.
        SELECT
            ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 25833) AS ipp,
            %s::double precision AS r50_meter,
            %s::double precision AS extend_meter
    ),

    r50 AS (
        -- R50 brukes både som klippeflate og som ytre ring i linjenettet.
        SELECT
            ST_Buffer(ipp, r50_meter) AS area,
            ST_Boundary(ST_Buffer(ipp, r50_meter)) AS ring
        FROM params
    ),

    roads_raw AS (
        -- Hent veier som ligger i R50 eller nær nok ringen til å kunne forlenges.
        SELECT
            (ST_Dump(
                ST_CollectionExtract(
                    ST_LineMerge(ST_CurveToLine(v.senterlinje)),
                    2
                )
            )).geom AS geom
        FROM n50kartdata.veglenke v, r50, params
        WHERE
            ST_Intersects(v.senterlinje, r50.area)
            OR ST_DWithin(v.senterlinje, r50.ring, params.extend_meter)
    ),

    roads_extended AS (
        -- Forleng veier som nesten møter R50-ringen, slik at flere flater lukkes.
        SELECT
            ST_LineExtend(
                geom,
                CASE
                    WHEN ST_DWithin(ST_EndPoint(geom), r50.ring, params.extend_meter)
                    THEN params.extend_meter
                    ELSE 0
                END,
                CASE
                    WHEN ST_DWithin(ST_StartPoint(geom), r50.ring, params.extend_meter)
                    THEN params.extend_meter
                    ELSE 0
                END
            ) AS geom
        FROM roads_raw, r50, params
    ),

    roads_clipped AS (
        -- Klipp alle veilinjer til R50.
        SELECT
            (ST_Dump(
                ST_CollectionExtract(
                    ST_Intersection(geom, r50.area),
                    2
                )
            )).geom AS geom
        FROM roads_extended, r50
        WHERE NOT ST_IsEmpty(ST_Intersection(geom, r50.area))
    ),

    linework AS (
        -- Kombiner veiene med R50-ringen før noding og polygonisering.
        SELECT geom FROM roads_clipped
        UNION ALL
        SELECT ring AS geom FROM r50
    ),

    noded AS (
        -- Snap og node linjenettet slik at kryss og nesten-møter kan danne lukkede flater.
        SELECT
            ST_Node(
                ST_Snap(
                    ST_Collect(geom),
                    ST_Collect(geom),
                    0.5
                )
            ) AS geom
        FROM linework
    ),

    polygons AS (
        -- Lag polygoner av alle lukkede linjeringer.
        SELECT
            (ST_Dump(ST_Polygonize(geom))).geom AS geom
        FROM noded
    ),

    filtered AS (
        -- Behold teiger inne i R50 og fjern svært små flater.
        SELECT
            ST_Intersection(polygons.geom, r50.area) AS geom
        FROM polygons, r50
        WHERE
            ST_Area(polygons.geom) > 1000
            AND ST_Within(ST_PointOnSurface(polygons.geom), r50.area)
    )

    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', COALESCE(
            json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::json,
                    'properties', json_build_object(
                        'area_m2', ROUND(ST_Area(geom)::numeric, 1)
                    )
                )
            ),
            '[]'::json
        )
    )
    FROM filtered;
"""

TEIGER_SQL_FALLBACK = """
    WITH params AS (
        -- Fallback bruker samme R50, men uten ST_LineExtend.
        SELECT
            ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 25833) AS ipp,
            %s::double precision AS r50_meter
    ),

    r50 AS (
        SELECT
            ST_Buffer(ipp, r50_meter) AS area,
            ST_Boundary(ST_Buffer(ipp, r50_meter)) AS ring
        FROM params
    ),

    roads_clipped AS (
        SELECT
            (ST_Dump(
                ST_CollectionExtract(
                    ST_Intersection(ST_CurveToLine(v.senterlinje), r50.area),
                    2
                )
            )).geom AS geom
        FROM n50kartdata.veglenke v, r50
        WHERE ST_Intersects(v.senterlinje, r50.area)
    ),

    linework AS (
        SELECT geom FROM roads_clipped
        UNION ALL
        SELECT ring AS geom FROM r50
    ),

    noded AS (
        SELECT
            ST_Node(
                ST_Snap(
                    ST_Collect(geom),
                    ST_Collect(geom),
                    0.5
                )
            ) AS geom
        FROM linework
    ),

    polygons AS (
        SELECT
            (ST_Dump(ST_Polygonize(geom))).geom AS geom
        FROM noded
    ),

    filtered AS (
        SELECT
            ST_Intersection(polygons.geom, r50.area) AS geom
        FROM polygons, r50
        WHERE
            ST_Area(polygons.geom) > 1000
            AND ST_Within(ST_PointOnSurface(polygons.geom), r50.area)
    )

    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', COALESCE(
            json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::json,
                    'properties', json_build_object(
                        'area_m2', ROUND(ST_Area(geom)::numeric, 1),
                        'fallback', true,
                        'fallback_reason', 'ST_LineExtend er ikke tilgjengelig; veier er klippet uten forlengelse.'
                    )
                )
            ),
            '[]'::json
        )
    )
    FROM filtered;
"""
