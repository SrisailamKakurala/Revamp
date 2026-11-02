
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Create the FastAPI application.
app = FastAPI(title="Task Manager API")

# Temporary storage, just like the Flask project.
tasks = {}
next_id = 1


# Define the shape of data clients send when creating a task.
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool = False


# Define the complete data required to replace a task.
# Both fields are optional
class TaskPatch(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    
    
# Define the complete data required to replace a task.
class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool = None


# CREATE: POST /tasks
@app.post("/tasks", status_code=201)
def create_task(data: TaskCreate):
    global next_id

    # FastAPI validates the JSON body using TaskCreate.
    task = {
        "id": next_id,
        "title": data.title.strip(),
        "completed": data.completed
    }

    if not task["title"]:
        raise HTTPException(status_code=422, detail="Title cannot be blank")

    tasks[next_id] = task
    next_id += 1

    return task


# READ ALL: GET /tasks
@app.get("/tasks")
def get_tasks():
    return list(tasks.values())


# READ ONE: GET /tasks/{task_id}
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)

    if task is None:
        # FastAPI converts this exception into an HTTP error response.
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# UPDATE: PUT /tasks/{task_id}
@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    # Replace the existing task with the validated request data.
    tasks[task_id] = {
        "id": task_id,
        "title": data.title.strip(),
        "completed": data.completed
    }

    if not tasks[task_id]["title"]:
        raise HTTPException(status_code=422, detail="Title cannot be blank")

    return tasks[task_id]


# DELETE: DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[task_id]

    # No return body is needed for HTTP 204.
    return None


# PATCH: PATCH /tasks/{task_id}
@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, data: TaskPatch):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get only the fields actually provided by the client
    updates = data.model_dump(exclude_unset=True)

    # Validate title if the user provided it
    if "title" in updates:
        if not updates["title"].strip():
            raise HTTPException(status_code=422, detail="Title cannot be blank")

        updates["title"] = updates["title"].strip()

    # Update only the provided fields
    tasks[task_id].update(updates)

    return tasks[task_id]