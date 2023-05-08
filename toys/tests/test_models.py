from toys.models import Toy

from django.utils.timezone import now
from datetime import date
import pytest


@pytest.fixture
def create_toy(db):
    return Toy.objects.create(
        created=now(),
        name="Destroyer",
        description="A Toy Destroyer",
        toy_category="Best_of_all_times",
        release_date=date(2022, 1, 1),
        was_included_in_home=bool(True),
    )


def test_toy_fields(create_toy):
    assert create_toy.name == "Destroyer"
    assert create_toy.description == "A Toy Destroyer"
    assert create_toy.toy_category == "Best_of_all_times"
    assert create_toy.release_date == date(2022, 1, 1)
    assert create_toy.was_included_in_home == bool(True)
