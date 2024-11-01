from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1


#create task
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data["title"], description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso"})


#list all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
            }
    return jsonify(output)


# list only one task
@app.route('/tasks/<int:id_task>', methods=['GET'])
def get_task(id_task):
    for task in tasks:
        if task.id == id_task:
            return jsonify(task.to_dict())
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404


# update task
@app.route('/tasks/<int:id_task>', methods=['PUT'])
def update_task(id_task):
    task_opt = None
    for task in tasks:
        if task.id == id_task:
            task_opt = task

    if task_opt == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({"message": "Tarefa atualizada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)
