import pytest
from src import data
from src.scooter_api import ScooterApi


@pytest.fixture()
def scooter_api():
    return ScooterApi(data.scooter_url)
