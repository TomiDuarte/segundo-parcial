"""
Tests de contrato basados en specs/openapi.yaml (Spec Driven Development).

Estos tests validan que la implementación cumple con la especificación.
Si el spec dice que /tasks devuelve un array de Task con id, title, completed,
estos tests fallan si la implementación no respeta el contrato.
"""
import schemathesis
from fastapi.testclient import TestClient

from app.main import app, _tasks

# Carga el spec desde el archivo YAML (fuente de verdad)
schema = schemathesis.from_path("specs/openapi.yaml", app=app)


@schema.parametrize()
def test_api_conforms_to_spec(case):
    """
    Cada endpoint del spec se prueba automáticamente.
    Schemathesis valida:
      - Que la respuesta cumpla con el schema definido en el spec.
      - Que los status codes sean los esperados.
      - Que los content-types coincidan.
    """
    _tasks.clear()  # limpia storage entre casos
    client = TestClient(app)
    response = case.call(session=client)
    case.validate_response(response)