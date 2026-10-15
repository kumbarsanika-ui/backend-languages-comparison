from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_app()) as test_client:
        yield test_client


def test_health_and_list_employees(client: TestClient) -> None:
    health_response = client.get("/health")
    employees_response = client.get("/employees")

    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}
    assert employees_response.status_code == 200
    assert employees_response.json() == [
        {"id": 1, "name": "Ada Lovelace", "email": "ada@example.com"}
    ]


def test_employee_crud(client: TestClient) -> None:
    created = client.post(
        "/employees",
        json={"name": "Grace Hopper", "email": "grace@example.com"},
    )

    assert created.status_code == 201
    employee = created.json()
    assert employee == {
        "id": 2,
        "name": "Grace Hopper",
        "email": "grace@example.com",
    }
    assert client.get("/employees/2").json() == employee

    updated = client.put(
        "/employees/2",
        json={"name": "Grace Brewster Hopper", "email": "grace@example.com"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Grace Brewster Hopper"

    deleted = client.delete("/employees/2")
    assert deleted.status_code == 204
    assert client.get("/employees/2").status_code == 404


def test_validation_and_missing_employee_errors(client: TestClient) -> None:
    invalid_employee = client.post(
        "/employees", json={"name": "", "email": "not-an-email"}
    )

    assert invalid_employee.status_code == 422
    assert client.get("/employees/999").status_code == 404
    assert client.put(
        "/employees/999",
        json={"name": "Nobody", "email": "nobody@example.com"},
    ).status_code == 404
    assert client.delete("/employees/999").status_code == 404