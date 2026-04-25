import mysql.connector
from config import config
from werkzeug.security import generate_password_hash


class mySQLDB:
    def __init__(self) -> None:

        self.configuration = {
            "host": config.get("database", "host"),
            "port": config.getint("database", "port"),
            "user": config.get("database", "user"),
            "password": config.get("database", "password"),
            "database": config.get("database", "database"),
        }

    def __enter__(self):
        try:
            # Establish a database connection and create a cursor
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor(dictionary=True)
            return self
        except mysql.connector.Error as e:
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