# -*- coding: utf-8 -*-

# Stdlib:
import os

# Thirdparty:
import ormar
import sqlalchemy
from casbin import Enforcer
from databases import Database
from pytest import fixture

# Firstparty:
from ormar_casbin_adapter import DatabasesAdapter
from tests.database import DATABASE_URL, POSTGRES_DB, database, metadata


class CasbinRule(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "casbin_rules"

    id: int = ormar.Integer(primary_key=True)
    ptype: str = ormar.String(max_length=255)
    v0: str = ormar.String(max_length=255)
    v1: str = ormar.String(max_length=255)
    v2: str = ormar.String(max_length=255, nullable=True)
    v3: str = ormar.String(max_length=255, nullable=True)
    v4: str = ormar.String(max_length=255, nullable=True)
    v5: str = ormar.String(max_length=255, nullable=True)


@fixture()
def root_engine():
    root_engine = sqlalchemy.create_engine(
        str(DATABASE_URL.replace(database="postgres")), isolation_level="AUTOCOMMIT"
    )
    return root_engine


@fixture()
def test_database(root_engine):
    with root_engine.connect() as conn:
        print(f"Creating test database '{POSTGRES_DB}'")
        conn.execute(f'DROP DATABASE IF EXISTS "{POSTGRES_DB}";')
        conn.execute(f'CREATE DATABASE "{POSTGRES_DB}"')

    yield

    with root_engine.connect() as conn:
        root_engine.execute(f'DROP DATABASE "{POSTGRES_DB}"')


@fixture()
async def db(test_database):
    # Ensure the DB has the schema we need for testing
    engine = sqlalchemy.create_engine(str(DATABASE_URL))
    metadata.create_all(engine)
    engine.dispose()

    await database.connect()
    yield
    await database.disconnect()


@fixture()
async def casbin_rule_table(db: Database):
    return CasbinRule


@fixture(scope="function")
async def setup_policies(db: Database):
    rows = [
        {"ptype": "p", "v0": "alice", "v1": "data1", "v2": "read"},
        {"ptype": "p", "v0": "bob", "v1": "data2", "v2": "write"},
        {"ptype": "p", "v0": "data2_admin", "v1": "data2", "v2": "read"},
        {"ptype": "p", "v0": "data2_admin", "v1": "data2", "v2": "write"},
        {"ptype": "g", "v0": "alice", "v1": "data2_admin"},
    ]
    await CasbinRule.objects.bulk_create([CasbinRule(**row) for row in rows])
    yield await CasbinRule.objects.all()
    casbin_rules = await CasbinRule.objects.all()
    for casbin_rule in casbin_rules:
        await casbin_rule.delete()


@fixture(scope="function")
def model_conf_path():
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + "rbac_model.conf")


@fixture(scope="function")
async def enforcer(db: Database, setup_policies, model_conf_path) -> Enforcer:
    adapter = DatabasesAdapter(model=CasbinRule)
    enforcer = Enforcer(model_conf_path, adapter)
    await enforcer.load_policy()
    return enforcer
