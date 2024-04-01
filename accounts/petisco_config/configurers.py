import os

from petisco import ApplicationConfigurer, databases
from petisco.extra.sqlalchemy import (
    SqliteConnection,
    # MySqlConnection,
    SqlDatabase,
)

DATABASE_NAME = "sql-accounts"
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
SQL_SERVER = os.getenv("SQL_SERVER", "sqlite")


class DatabasesConfigurer(ApplicationConfigurer):
    def execute(self, testing: bool = True) -> None:
        if testing or (SQL_SERVER == "sqlite"):
            test_db_filename = "accounts.db"
            connection = SqliteConnection.create("sqlite", test_db_filename)
        else:
            connection = SqliteConnection.create("sqlite", test_db_filename)
            # connection = MySqlConnection.from_environ()

        sql_database = SqlDatabase(alias=DATABASE_NAME, connection=connection)

        databases.add(sql_database)
        databases.initialize()


configurers = [DatabasesConfigurer()]
