from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import Task, Project
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.auth import get_current_user
from app.rules import validate_task_transition
import uuid

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/projects/{project_id}", response_model=TaskResponse)
def create_task(
    project_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    existing_task = db.query(Task).filter(
        Task.project_id == project_id,
        Task.title.ilike(task.title)
    ).first()

    if existing_task:
        raise HTTPException(
            status_code=409,
            detail="Task title already exists in this project"
        )

    task_id = str(uuid.uuid4())

    new_task = Task(
        id=task_id,
        title=task.title,
        status="todo",
        project_id=project_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "status": new_task.status,
        "project_id": new_task.project_id,
    }


@router.get("/projects/{project_id}")
def get_tasks(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    return [
        {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "project_id": task.project_id,
        }
        for task in tasks
    ]


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    validate_task_transition(task.status, task_update.status)

    task.status = task_update.status
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "project_id": task.project_id,
    }


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}