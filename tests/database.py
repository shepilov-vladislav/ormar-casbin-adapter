# -*- coding: utf-8 -*-

# Stdlib:
import os

# Thirdparty:
import databases
import sqlalchemy

POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = int(os.environ["POSTGRES_PORT"])
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]


DATABASE_URL = databases.DatabaseURL(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
database = databases.Database(str(DATABASE_URL))
metadata = sqlalchemy.MetaData()
