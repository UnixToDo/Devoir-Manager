from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
API_BASE = "http://api:5000"

@app.route("/")
def home():
    priority = request.args.get("priority")
    date = request.args.get("date")
    params = {}
    if priority:
        params["priority"] = priority
    if date:
        params["date"] = date
    response = requests.get(f"{API_BASE}/todos", params=params)
    todos = response.json()
    return render_template("index.html", todos=todos, priority=priority, date=date)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form["task"]
    priority = request.form["priority"]
    date = request.form["date"]
    requests.post(f"{API_BASE}/todos", json={"task": task, "priority": priority, "date": date})
    return redirect("/")

@app.route("/update/<todo_id>", methods=["POST"])
def update_todo(todo_id):
    task = request.form["task"]
    priority = request.form["priority"]
    date = request.form["date"]
    requests.put(f"{API_BASE}/todos/{todo_id}", 
                json={"task": task, "priority": priority, "date": date})
    return redirect("/")

@app.route("/edit/<todo_id>")
def edit_todo(todo_id):
    response = requests.get(f"{API_BASE}/todos")
    todos = response.json()
    todo = next((item for item in todos if item["_id"] == todo_id), None)
    return render_template("edit.html", todo=todo)


@app.route("/delete/<todo_id>")
def delete_todo(todo_id):
    requests.delete(f"{API_BASE}/todos/{todo_id}")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

