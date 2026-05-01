from flask import Blueprint, jsonify, request
from flask_login import login_required
import json
import psycopg
from app.db import mySQLDB
from app.db import myPostgresqlDB
from app.data.teiger_service import (
    fetch_teiger_feature_collection,
    parse_teiger_args,
)

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
    teiger_args, error_message = parse_teiger_args(request.args)
    if error_message:
        return jsonify({"error": error_message}), 400

    try:
        with myPostgresqlDB() as db:
            feature_collection = fetch_teiger_feature_collection(db, teiger_args)
            return jsonify(feature_collection)
    except psycopg.Error as e:
        return jsonify({
            "error": "Klarte ikke å generere teiger fra PostGIS.",
            "details": str(e)
        }), 500
