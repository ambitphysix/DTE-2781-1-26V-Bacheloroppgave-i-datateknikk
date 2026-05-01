import psycopg

from app.data.teiger_sql import (
    EMPTY_FEATURE_COLLECTION,
    TEIGER_SQL_FALLBACK,
    TEIGER_SQL_WITH_EXTEND,
)


def parse_teiger_args(args):
    try:
        teiger_args = {
            "lat": float(args["lat"]),
            "lng": float(args["lng"]),
            "r50_meter": float(args["r50_meter"]),
            "extend_meter": float(args.get("extend_meter", 50)),
        }
    except (KeyError, TypeError, ValueError):
        return None, "Ugyldige parametere. Bruk lat, lng, r50_meter og valgfri extend_meter."

    if teiger_args["r50_meter"] <= 0 or teiger_args["extend_meter"] < 0:
        return None, "r50_meter må være større enn 0, og extend_meter kan ikke være negativ."

    return teiger_args, None


def fetch_teiger_feature_collection(db, teiger_args):
    try:
        db.query(
            TEIGER_SQL_WITH_EXTEND,
            teiger_args["lng"],
            teiger_args["lat"],
            teiger_args["r50_meter"],
            teiger_args["extend_meter"],
        )
    except psycopg.errors.UndefinedFunction:
        db.conn.rollback()
        db.query(
            TEIGER_SQL_FALLBACK,
            teiger_args["lng"],
            teiger_args["lat"],
            teiger_args["r50_meter"],
        )

    row = db.cursor.fetchone()
    return row[0] if row else EMPTY_FEATURE_COLLECTION
