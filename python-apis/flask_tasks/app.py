
from flask import Flask, request, jsonify

# Create the Flask application.
app = Flask(__name__)

# Temporary storage: task ID -> task data.
# A real project would normally use a database.
tasks = {}
next_id = 1


# CREATE: POST /tasks
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    # Read the JSON body sent by the client.
    data = request.get_json(silent=True)

    # Validate the incoming data ourselves in Flask.
    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object"}), 400

    title = data.get("title")
    completed = data.get("completed", False)

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required"}), 400

    if not isinstance(completed, bool):
        return jsonify({"error": "completed must be true or false"}), 400

    # Create and store the new task.
    task = {
        "id": next_id,
        "title": title.strip(),
        "completed": completed
    }

    tasks[next_id] = task
    next_id += 1

    # Return the new task with HTTP 201 (Created).
    return jsonify(task), 201


# READ ALL: GET /tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    # Convert stored tasks into a JSON array.
    return jsonify(list(tasks.values())), 200


# READ ONE: GET /tasks/<task_id>
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # Look up the task using its ID.
    task = tasks.get(task_id)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


# UPDATE: PUT /tasks/<task_id>
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # You cannot update a task that doesn't exist.
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object"}), 400

    title = data.get("title")
    completed = data.get("completed")

    # PUT replaces the task representation, so require both fields.
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required"}), 400

    if not isinstance(completed, bool):
        return jsonify({"error": "completed must be true or false"}), 400

    # Replace the existing task.
    tasks[task_id] = {
        "id": task_id,
        "title": title.strip(),
        "completed": completed
    }

    return jsonify(tasks[task_id]), 200


# DELETE: DELETE /tasks/<task_id>
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    # Remove the task from storage.
    del tasks[task_id]

    # 204 means success with no response body.
    return "", 204


# Start the development server when running this file directly.
if __name__ == "__main__":
    app.run(debug=True, port=5000)
