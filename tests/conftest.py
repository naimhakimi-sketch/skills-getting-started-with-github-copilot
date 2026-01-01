import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure src is on the import path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import app as app_module  # noqa: E402  # isort:skip


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory activities between tests."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


@pytest.fixture
def client():
    return TestClient(app_module.app)
