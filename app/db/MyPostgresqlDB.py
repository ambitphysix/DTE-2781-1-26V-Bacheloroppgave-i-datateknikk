import psycopg
from app.config import config

"""
Vi bruker denne for å gjøre kall mot PostGIS-databasen vår.
"""

class myPostgresqlDB:
    def __init__(self) -> None:

        self.configuration = {
            "host": config.get("database-postgis", "dbhost"),
            "port": config.getint("database-postgis", "dbport"),
            "user": config.get("database-postgis", "dbuser"),
            "password": config.get("database-postgis", "dbpass"),
            "dbname": config.get("database-postgis", "dbname"),
        }

    def __enter__(self):
        try:
            # Establish a database connection and create a cursor
            self.conn = psycopg.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self
        except psycopg.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        try:
            # Commit changes if no exception occurred, otherwise rollback
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            # Close the cursor and connection
            self.cursor.close()
            self.conn.close()

    def query(self, sql_query, *args, **kwargs) -> None:
        # Execute a query
        if len(kwargs) > 0:
            self.cursor.execute(sql_query, kwargs)
        else:
            self.cursor.execute(sql_query, args)
