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
    radius = request.args.get('radius')
    with myPostgresqlDB() as db:
        query = """
                WITH RECURSIVE connected_roads AS (
                    SELECT 
                        v.senterlinje, 
                        v.objid
                    FROM 
                        n50kartdata.veglenke v
                    WHERE 
                        ST_DWithin(
                            v.senterlinje, 
                            ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 25833), 
                            10.0
                        )

                    UNION

                    SELECT 
                        v.senterlinje, 
                        v.objid
                    FROM 
                        n50kartdata.veglenke v
                    INNER JOIN 
                        connected_roads cr ON ST_Intersects(v.senterlinje, cr.senterlinje)
                    WHERE 
                        ST_DWithin(
                            v.senterlinje, 
                            ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 25833), 
                            %s
                        )
                )

                SELECT DISTINCT st_asgeojson(st_transform(st_curvetoline(senterlinje), 4326)) as geom FROM connected_roads;
        """
        db.query(query, lng, lat, lng, lat, radius)
        rows = db.cursor.fetchall()
        geojson_list = [json.loads(row[0]) for row in rows]
        
        return jsonify(geojson_list)
