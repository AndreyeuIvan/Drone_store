import pytest
from datetime import date

from drones.models import Drone, DroneCategory, Pilot, Competition
from django.utils.timezone import now


@pytest.fixture
def create_category(db):
    return DroneCategory.objects.create(name="Killer")


def test_drone_category_str_method(create_category):
    assert str(create_category) == "Killer"


@pytest.fixture
def create_drone(db, create_category):
    return Drone.objects.create(
        name="Maxar",
        drone_category=create_category,
        manufacturing_date=date(2022, 1, 1),
        has_it_competed=True,
        inserted_timestamp=now(),
    )


def test_drone_str_method(create_drone):
    assert str(create_drone) == "Maxar"


def test_drone_fields(create_drone, create_category):
    assert create_drone.name == "Maxar"
    assert create_drone.drone_category == create_category
    assert create_drone.manufacturing_date == date(2022, 1, 1)
    assert create_drone.has_it_competed == bool(True)


@pytest.fixture
def create_pilote(db):
    return Pilot.objects.create(
        name="Max",
        gender="Male",
        races_count=1,
        inserted_timestamp=now(),
    )


def test_pilote_str_method(create_pilote):
    assert str(create_pilote) == "Max"


def test_pilote_fields(create_pilote):
    assert create_pilote.name == "Max"
    assert create_pilote.gender == "Male"
    assert create_pilote.races_count == 1


@pytest.fixture
def create_competition(db, create_pilote, create_drone):
    return Competition.objects.create(
        pilot=create_pilote,
        drone=create_drone,
        distance_in_feet=1,
        distance_achievement_date=now(),
    )


def test_competiton_str_method(create_competition):
    assert str(create_competition) == "Max with own drone |Maxar|"


def test_competition_fields(create_competition, create_pilote, create_drone):
    assert create_competition.pilot == create_pilote
    assert create_competition.drone == create_drone
    assert create_competition.distance_in_feet == 1
