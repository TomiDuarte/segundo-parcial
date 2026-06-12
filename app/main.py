"""Tasks API - implementación basada en specs/openapi.yaml."""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from app import __version__
from app.models import HealthResponse, Task, TaskCreate

app = FastAPI(
    title="Tasks API",
    description="Demo de CI/CD - Ingeniería y Calidad de SW",
    version=__version__,
)

# Storage en memoria (suficiente para la demo)
_tasks: dict[int, Task] = {}
_next_id: int = 1


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    return FileResponse("frontend.html")


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check() -> HealthResponse:
    """Verifica que el servicio esté operativo."""
    return HealthResponse(status="ok", version=__version__)


@app.get("/tasks", response_model=list[Task], tags=["Tasks"])
def list_tasks() -> list[Task]:
    """Lista todas las tareas."""
    return list(_tasks.values())


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
)
def create_task(task_data: TaskCreate) -> Task:
    """Crea una nueva tarea."""
    global _next_id
    task = Task(
        id=_next_id,
        title=task_data.title,
        completed=task_data.completed,
    )
    _tasks[_next_id] = task
    _next_id += 1
    return task


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int) -> Task:
    """Obtiene una tarea por su ID."""
    if task_id not in _tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return _tasks[task_id]