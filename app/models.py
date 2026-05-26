"""Modelos de datos basados en la especificación OpenAPI."""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Respuesta del health check."""
    status: str = Field(default="ok", pattern="^ok$")
    version: str = Field(default="1.0.0")


class TaskCreate(BaseModel):
    """Datos para crear una tarea (input)."""
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = Field(default=False)


class Task(BaseModel):
    """Tarea completa (output)."""
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = Field(default=False)