import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Todo

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('DEBUG', False)
app.config['ENV'] = os.getenv('ENV', 'production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db)
CORS(app)

@app.route('/')
def root():
    return jsonify({ "msg": "API REST Flask"})


@app.route('/api/users/<int:id>/todos', methods=['POST'])
def user_add_todo(id):

    title = request.json.get('title')
    priority = request.json.get('priority', "low")
    done = request.json.get('done', False)

    todo = Todo()
    todo.title = title
    todo.priority = priority
    todo.done = done

    user = User.query.get(id)
    user.todos.append(todo)
    user.update()

    return jsonify(user.serialize_with_todos()), 201

@app.route('/api/users/<int:id>/todos/<int:todos_id>', methods=['DELETE'])
def user_delete_todo(id, todos_id):

    todo = Todo.query.get(todos_id)
    #todo.delete()

    user = User.query.get(id)
    user.todos.remove(todo)

    return jsonify(user.serialize_with_todos()), 201

@app.route('/api/todos', methods=['GET'])
def get_todo():
    todos = Todo.query.all()
    todos = list(map(lambda todo: todo.serialize(), todos))
    return jsonify(todos), 200

@app.route('/api/todos', methods=['POST'])
def add_todo():

    title = request.json.get('title')
    priority = request.json.get('priority', "low")
    done = request.json.get('done', False)
    users_id = request.json.get('users_id')

    todo = Todo()
    todo.title = title
    todo.priority = priority
    todo.done = done
    todo.users_id = users_id
    todo.save()

    return jsonify(todo.serialize()), 201



@app.route('/api/todos', methods=['PUT'])
def update_todo():
    pass

@app.route('/api/todos', methods=['DELETE'])
def delete_todo():
    pass


if __name__ == '__main__':
    app.run()