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
        query = f"""
                WITH RECURSIVE connected_network AS (
                    SELECT objid, senterlinje FROM n50kartdata.veglenke 
                    WHERE ST_DWithin(senterlinje, ST_Transform(ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326), 25833), 10.0)
                    UNION ALL
                    SELECT objid, senterlinje FROM n50kartdata.lysloype 
                    WHERE ST_DWithin(senterlinje, ST_Transform(ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326), 25833), 10.0)
                    UNION ALL
                    SELECT objid, grense AS senterlinje FROM n50kartdata.elvekant
                    WHERE ST_DWithin(grense, ST_Transform(ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326), 25833), 10.0)
                    UNION ALL
                    SELECT objid, senterlinje FROM n50kartdata.elvbekk
                    WHERE ST_DWithin(senterlinje, ST_Transform(ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326), 25833), 10.0)

                    UNION

                    SELECT al.objid, al.senterlinje
                    FROM (
                        SELECT objid, senterlinje FROM n50kartdata.veglenke
                        UNION ALL
                        SELECT objid, senterlinje FROM n50kartdata.lysloype
                        UNION ALL
                        SELECT objid, grense AS senterlinje FROM n50kartdata.elvekant
                        UNION ALL
                        SELECT objid, senterlinje FROM n50kartdata.elvbekk
                    ) al
                    INNER JOIN connected_network cn ON ST_Intersects(al.senterlinje, cn.senterlinje)
                    WHERE ST_DWithin(al.senterlinje, ST_Transform(ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326), 25833), {radius})
                )
                SELECT DISTINCT ST_AsGeoJSON(ST_Transform(ST_CurveToLine(senterlinje), 4326)) FROM connected_network;
        """
        db.query(query)
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
    minArea = request.args.get('minAreaValue')
    maxArea = request.args.get('maxAreaValue')
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

                UNION
                
                /*Denne henter ut elvbekk fra elvbekk-tabellen*/
                SELECT 
                    objid, ST_SetSRID(senterlinje, 25833) AS geom
                FROM 
                    n50kartdata.elvbekk, reference
                WHERE
                    ST_Intersects(relevant_area, senterlinje)

                UNION
                
                /*Denne henter ut park-kanter fra park-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.park, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION
                
                /*Denne henter ut skytefelt-kanter fra skytefelt-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.skytefelt, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut tettbebyggelse-kanter fra tettbebyggelse-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.tettbebyggelse, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut innsjøregulert-kanter fra innsjøregulert-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.innsjoregulert, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut industriområde-kanter fra industriområde-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.industriomrade, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut havflate-kanter fra havflate-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.havflate, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut gravplass-kanter fra gravplass-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.gravplass, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut golfbane-kanter fra golfbane-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.golfbane, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut dyrketmark-kanter fra dyrketmark-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.dyrketmark, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)

                UNION

                /*Denne henter ut bymessigbebyggelse-kanter fra bymessigbebyggelse-tabellen*/
                SELECT 
                    objid, ST_Boundary(ST_SetSRID(omrade, 25833)) AS geom
                FROM 
                    n50kartdata.bymessigbebyggelse, reference
                WHERE
                    ST_Intersects(relevant_area, omrade)
                )
                
            SELECT
                ST_AsGeoJSON((ST_Dump(ST_Polygonize(geom))).geom) AS poly
            FROM 
                (
                    SELECT 
                        ST_UnaryUnion(ST_SnapToGrid(ST_Collect(geom), 20)) AS geom
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
        return jsonify(parse_search_areas(results, float(minArea), float(maxArea)))