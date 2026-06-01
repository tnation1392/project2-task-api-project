from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import Project
from app.schemas import ProjectCreate, ProjectResponse
from app.auth import get_current_user
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_project = db.query(Project).filter(
        Project.owner_id == current_user["id"],
        Project.name.ilike(project.name)
    ).first()

    if existing_project:
        raise HTTPException(
            status_code=409,
            detail="Project name already exists for this user"
        )

    project_id = str(uuid.uuid4())

    new_project = Project(
        id=project_id,
        name=project.name,
        owner_id=current_user["id"],
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "id": new_project.id,
        "name": new_project.name,
        "owner_id": new_project.owner_id,
        "created_at": new_project.created_at,
        "updated_at": new_project.updated_at,
    }


@router.get("/")
def get_projects(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    projects = db.query(Project).filter(Project.owner_id == current_user["id"]).all()

    return [
        {
            "id": project.id,
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
        }
        for project in projects
    ]


@router.get("/{project_id}")
def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return {
        "id": project.id,
        "name": project.name,
        "owner_id": project.owner_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}