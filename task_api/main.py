from typing import Optional,List
import auth
from database import get_db, Base, engine
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
import models
import schemas
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Multi-User Tasks & Notes API",
    description=" A production ready FastAPI backend with MysQL, JWT Auth, and SQLAlchemy",
    version="1.0.0",
)

# AUTHENTICATION ENDPOINTS

# Route to register new User Acocunt

@app.post(
    "/auth/register",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(
            (models.User.username==user.username) | (models.User.email==user.email)
        ).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or Email already exists",
        )
    hashed_pwd = auth.hash_password(user.password)

    new_user = models.User(
        username = user.username, email = user.email, hashed_password = hashed_pwd
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

# Route to Login and get access token

@app.post("/auth/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User).filter(
            models.User.username==form_data.username
        ).first()
    )

    if not user or not auth.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect Username or Password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    access_token = auth.create_access_token(data={"sub":user.username})

    return {"access_token":access_token, "token_type":"bearer"}



# TASKS & NOTES CRUD ENDPOINTS(PROTECTED)

# Route to create a new task assigned to the authenticated user

@app.post(
    "/tasks",
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: schemas.TaskCreate,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_task = models.Task(**task.model_dump(), owner_id=current_user.id)

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task


# Route to retrieve tasks belonging to the Authorized user

@app.get("/tasks", response_model=List[schemas.TaskOut])
def get_my_tasks(
    priority: Optional[str] = Query(
        None, description="Filter by priority (low, medium, high, critical)"
    ),
    is_completed: Optional[bool] = Query(
        None, description="Filter by completion status"
    ),
    limit: int = Query(
        default=10, ge=1, le=100, description="Number of records to return "
    ),
    skip: int = Query(
        default=0, ge=0, description="Number of records to Skip"
    ),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Task).filer(
        models.Task.owner_id == current_user.id
    )

    if priority:
        query = query.filter(models.Task.priority==priority.lower())

    if is_completed:
        query - query.filter(models.Task.is_completed==is_completed)

    tasks = query.offset(skip).limit(limit).all()

    return tasks

# Route to get specific task by its primary ID

@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_single_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id, models.Task.owner_id==current_user.id
        ).first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied",
        )

    return task


# Route to update an existing task

@app.put("/task/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    task_query = db.query(models.Task).filter(
        models.Task.id==task_id, models.Task.owner_id == current_user.id
    )

    task = task_query.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not Found or access denied",
        )

    update_data = task_update.model_dump(exclude_unset=True)

    task_query.update(update_data, synchronize_session=False)

    db.commit()

    db.refresh(task)

    return task


# Route to delete a task record

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    task = (
        db.query(models.Task).filter(
            models.Task.id == task_id, models.Task.owner_id==current_user.id
        ).first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= " Task not found or access Denied",
        )

    db.delete(task)
    db.commit()
    return None

