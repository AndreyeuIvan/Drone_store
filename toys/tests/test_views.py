import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from datetime import date

from toys.models import Toy


@pytest.mark.django_db
class TestToys:
    def test__toys_list_methods__bad_request(self):
        for method in ("delete", "patch", "put"):
            call_method = getattr(APIClient(), method.lower())
            response = call_method("http://testserver/toys/")
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test__toys_details_methods__bad_request(self):
        for method in ("post", "patch"):
            call_method = getattr(APIClient(), method.lower())
            response = call_method("http://testserver/toys/5")
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.fixture
    def create_a_list_of_toys(db):
        list_of_toys = [
            Toy.objects.create(
                name=f"Toy {x}",
                description="red",
                toy_category="small",
                release_date=date(2022, 1, 1),
                was_included_in_home=bool(True),
            )
            for x in range(0, 4)
        ]
        return list_of_toys

    def test__get_toys_list__success(self, create_a_list_of_toys) -> None:
        response = APIClient().get("http://testserver/toys/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(create_a_list_of_toys)
        # check default ordering
        ids_from_response = [
            i["id"]
            for i in sorted(
                response.data,
                key=lambda x: (x["description"], x["name"], x["toy_category"]),
            )
        ]
        ids_of_testing_toys = [x.id for x in create_a_list_of_toys]
        assert ids_from_response == ids_of_testing_toys

    def test__post_toys_create_new__created(self):
        response = APIClient().post(
            "http://testserver/toys/",
            data={
                "name": "Toy Fixed",
                "description": "red",
                "toy_category": "small",
                "release_date": date(2022, 1, 1),
                "was_included_in_home": bool(True),
            },
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test__get_toys_detail__success(self, create_a_list_of_toys) -> None:
        response = APIClient().get("http://testserver/toys/1")
        toy_for_testing = create_a_list_of_toys[0]
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"], toy_for_testing.id
        assert response.data["name"], toy_for_testing.name
        assert response.data["description"] == toy_for_testing.description

    def test__delete_toys_detail__success(self, create_a_list_of_toys) -> None:
        response = APIClient().delete("http://testserver/toys/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test__put_toys_detail_bad_request(self, create_a_list_of_toys) -> None:
        response = APIClient().put(
            "http://testserver/toys/1",
            data={"name": "Toy Fixed"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test__get_toys_detail__not_found(self, create_a_list_of_toys) -> None:
        response = APIClient().get("http://testserver/toys/5")
        assert response.status_code == status.HTTP_404_NOT_FOUND
