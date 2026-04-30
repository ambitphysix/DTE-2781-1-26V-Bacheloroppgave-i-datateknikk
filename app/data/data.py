from flask import Blueprint, jsonify, request
from flask_login import login_required
import json
import psycopg
from app.db import mySQLDB
from app.db import myPostgresqlDB

BP = Blueprint(
    "data", __name__, static_folder="static", template_folder="templates"
)


@BP.route("/radii/<missingPersonCategory>")
@login_required
def radii(missingPersonCategory):
    with mySQLDB() as db:
        query = "SELECT * from missing_categories WHERE kategori=%s;"
        db.query(query, missingPersonCategory)
        return jsonify(db.cursor.fetchone())


@BP.route("/missingPersonCategories")
@login_required
def missingPersonCategories():
    with mySQLDB() as db:
        query = "SELECT kategori FROM missing_categories;"
        db.query(query)
        return jsonify(db.cursor.fetchall())

@BP.route("/spokes")
@login_required
def spokes():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    with myPostgresqlDB() as db:
        query = """
            SELECT ST_AsGeoJSON(
                ST_Transform(
                    ST_LineMerge(
                        ST_Node( -- 2. Deler linjene i alle krysspunkter
                            ST_Snap( -- 1. Drar endepunkter mot hverandre (0.2m toleranse)
                                geom_collection, 
                                geom_collection, 
                                0.2
                            )
                        )
                    ), 
                4326)
            )
            FROM (
                SELECT ST_Collect(ST_CurveToLine(senterlinje)) AS geom_collection
                FROM n50kartdata.veglenke
                WHERE ST_DWithin(
                    senterlinje, 
                    ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 25833),
                    500
                )
            ) AS subquery;
        """
        db.query(query, lng, lat)
        rows = db.cursor.fetchall()
        geojson_list = [json.loads(row[0]) for row in rows]
        
        return jsonify(geojson_list)


@BP.route("/teiger")
@login_required
def teiger():
    try:
        lat = float(request.args["lat"])
        lng = float(request.args["lng"])
        r50_meter = float(request.args["r50_meter"])
        extend_meter = float(request.args.get("extend_meter", 50))
    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Ugyldige parametere. Bruk lat, lng, r50_meter og valgfri extend_meter."
        }), 400

    if r50_meter <= 0 or extend_meter < 0:
        return jsonify({
            "error": "r50_meter må være større enn 0, og extend_meter kan ikke være negativ."
        }), 400

    query = """
        WITH params AS (
            SELECT
                ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 25833) AS ipp,
                %s::double precision AS r50_meter,
                %s::double precision AS extend_meter
        ),

        r50 AS (
            SELECT
                ST_Buffer(ipp, r50_meter) AS area,
                ST_Boundary(ST_Buffer(ipp, r50_meter)) AS ring
            FROM params
        ),

        roads_raw AS (
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
                            'area_m2', ROUND(ST_Area(geom)::numeric, 1)
                        )
                    )
                ),
                '[]'::json
            )
        )
        FROM filtered;
    """

    fallback_query = """
        WITH params AS (
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

    try:
        with myPostgresqlDB() as db:
            try:
                db.query(query, lng, lat, r50_meter, extend_meter)
            except psycopg.errors.UndefinedFunction:
                db.conn.rollback()
                db.query(fallback_query, lng, lat, r50_meter)

            row = db.cursor.fetchone()
            feature_collection = row[0] if row else {"type": "FeatureCollection", "features": []}
            return jsonify(feature_collection)
    except psycopg.Error as e:
        return jsonify({
            "error": "Klarte ikke å generere teiger fra PostGIS.",
            "details": str(e)
        }), 500
