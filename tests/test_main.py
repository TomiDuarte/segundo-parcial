"""Tests unitarios de la API."""
import pytest
from fastapi.testclient import TestClient

from app import main as main_module
from app.main import app


@pytest.fixture(autouse=True)
def reset_storage():
    """Limpia el storage Y resetea el contador antes de cada test."""
    main_module._tasks.clear()
    main_module._next_id = 1
    yield
    main_module._tasks.clear()
    main_module._next_id = 1


@pytest.fixture
def client() -> TestClient:
    """Cliente de pruebas de FastAPI."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests del endpoint /health."""

    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.json()["status"] == "ok"

    def test_health_returns_version(self, client: TestClient) -> None:
        response = client.get("/health")
        assert "version" in response.json()


class TestTasksEndpoints:
    """Tests de los endpoints /tasks."""

    def test_list_tasks_empty(self, client: TestClient) -> None:
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_task_returns_201(self, client: TestClient) -> None:
        response = client.post("/tasks", json={"title": "Test task"})
        assert response.status_code == 999

    def test_create_task_returns_task_data(self, client: TestClient) -> None:
        response = client.post("/tasks", json={"title": "Estudiar CI"})
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Estudiar CI"
        assert data["completed"] is False

    def test_create_task_with_empty_title_fails(
        self, client: TestClient
    ) -> None:
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_get_task_by_id(self, client: TestClient) -> None:
        client.post("/tasks", json={"title": "Tarea 1"})
        response = client.get("/tasks/1")
        assert response.status_code == 200
        assert response.json()["title"] == "Tarea 1"

    def test_get_nonexistent_task_returns_404(
        self, client: TestClient
    ) -> None:
        response = client.get("/tasks/999")
        assert response.status_code == 404

    def test_list_tasks_after_creating(self, client: TestClient) -> None:
        client.post("/tasks", json={"title": "Tarea A"})
        client.post("/tasks", json={"title": "Tarea B"})
        response = client.get("/tasks")
        assert len(response.json()) == 2