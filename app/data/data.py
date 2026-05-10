from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.db import mySQLDB
from app.db import myPostgresqlDB
from app.data.utils import parse_search_areas
import json


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
        results = [
            {
                "type": "Feature",
                "geometry": json.loads(row[0]),
                "properties": {}
            } for row in db.cursor.fetchall()]
        return jsonify(results)


@BP.route("/searchAreas")
@login_required
def search_areas():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius')
    with myPostgresqlDB() as db:
        query = """
            WITH 
                reference AS (
                    SELECT
                        ST_Buffer(
                                st_transform(
                                    ST_SetSRID(st_makepoint(%s, %s), 4326), 
                                    25833
                                ),
                                %s
                            )
                    AS 
                        relevant_area
                
                ),
            
            geom_collection AS
                (
                /*Denne henter ut lysløyper fra lysløype-tabellen*/
                SELECT 
                    objid, ST_SetSRID(senterlinje, 25833) AS geom
                FROM 
                    n50kartdata.lysloype, reference
                WHERE
                    ST_Intersects(relevant_area, senterlinje)
                
                UNION
                    
                /*Denne henter ut veglenke-elementer fra veglenke-tabellen*/
                SELECT 
                    objid, ST_SetSRID(senterlinje, 25833) AS geom
                FROM 
                    n50kartdata.veglenke, reference
                WHERE
                    ST_Intersects(relevant_area, senterlinje)
                
                UNION
                
                /*Denne henter ut innsjø-kanter fra innsjøkant-tabellen*/
                SELECT 
                    objid, ST_SetSRID(grense, 25833) AS geom
                FROM 
                    n50kartdata.innsjokant, reference
                WHERE
                    ST_Intersects(relevant_area, grense)
                
                UNION
                
                /*Denne henter ut myr-kanter fra myr-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.myr, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)
                
                UNION
                
                
                /*Denne henter ut elvekanter fra elvekanter-tabellen*/
                SELECT 
                    objid, ST_SetSRID(grense, 25833) AS geom
                FROM 
                    n50kartdata.elvekant, reference
                WHERE
                    ST_Intersects(relevant_area, grense)
                )
                
            SELECT
                ST_AsGeoJSON((ST_Dump(ST_Transform(ST_Polygonize(geom), 4326))).geom) AS poly
            FROM 
                (
                    SELECT 
                        ST_UnaryUnion(ST_SnapToGrid(ST_Collect(geom), 5)) AS geom
                    FROM 
                        geom_collection
                ); 
        """
        db.query(query, lng, lat, radius)
        results = [{
                    "type": "Feature",
                    "geometry": json.loads(row[0]),
                    "properties": {}
                    } for row in db.cursor.fetchall()
                ]
        return jsonify(parse_search_areas(results))