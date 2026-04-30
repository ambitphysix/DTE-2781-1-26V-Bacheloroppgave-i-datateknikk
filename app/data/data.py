from flask import Blueprint, jsonify, request
from flask_login import login_required
import json
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
