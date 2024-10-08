from pathlib import Path

import pytest


@pytest.fixture
def rootdir():
    return Path(__file__).parent.parent

@pytest.fixture(autouse=True)
def run_from_rootdir(request, monkeypatch):
    monkeypatch.chdir(Path(__file__).parent.parent)
