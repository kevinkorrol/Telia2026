import importlib
import sys
from pathlib import Path

import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    monkeypatch.chdir(tmp_path)

    app_module = importlib.import_module("app")
    db_module = importlib.import_module("db")
    seed = importlib.import_module("mock")

    with app_module.app.app_context():
        db_module.db.drop_all()
        db_module.db.create_all()
        seed.seed_database(app_module.app, reset=True)

    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as client:
        yield client
