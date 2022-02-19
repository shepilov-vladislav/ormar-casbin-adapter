ormar Adapter for PyCasbin
====

## Repo
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/shepilov-vladislav/ormar-casbin-adapter/Pytest?logo=github&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)
[![Codecov](https://img.shields.io/codecov/c/github/shepilov-vladislav/ormar-casbin-adapter?logo=codecov&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/shepilov-vladislav/ormar-casbin-adapter?logo=code%20climate&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)
[![Dependabot](https://img.shields.io/badge/dependabot-Active-brightgreen?logo=dependabot&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)


## GitHub

[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/shepilov-vladislav/ormar-casbin-adapter?label=latest%20stable&sort=semver&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter/releases)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/shepilov-vladislav/ormar-casbin-adapter?label=latest%20unstable&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/shepilov-vladislav/ormar-casbin-adapter?style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter/commits/master)

## PyPI

[![PyPI - Version](https://img.shields.io/pypi/v/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)
[![PyPI - Python Wheel](https://img.shields.io/pypi/wheel/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)
[![PyPI - Format](https://img.shields.io/pypi/format/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)
[![PyPI - Status](https://img.shields.io/pypi/status/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)
[![PyPI - Downloads](https://img.shields.io/pypi/dd/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)
[![PyPI - License](https://img.shields.io/pypi/l/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)

ormar Adapter is the [ormar](https://collerek.github.io/ormar/) adapter for [PyCasbin](https://github.com/casbin/pycasbin). With this library, Casbin can load policy from ormar supported database or save policy to it.

Based on [Officially Supported Databases](https://collerek.github.io/ormar/), The current supported databases are:

- PostgreSQL
- MySQL
- SQLite

## Installation

```
pip install ormar_casbin_adapter
```

or

```
poetry add ormar-casbin-adapter
```

## Simple Example

```python
import casbin
import databases
import ormar
from ormar_casbin_adapter import DatabasesAdapter
import sqlalchemy

database = Database("sqlite://", force_rollback=True)
metadata = sqlalchemy.MetaData()


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


adapter = DatabasesAdapter(model=CasbinRule)

e = casbin.Enforcer("path/to/model.conf", adapter, True)

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "read"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    # permit alice to read data1ormar_casbin_adapter
    pass
else:
    # deny the request, show an error
    pass
```


### Getting Help

- [PyCasbin](https://github.com/casbin/pycasbin)

### License

This project is licensed under the [Apache 2.0 license](LICENSE).
