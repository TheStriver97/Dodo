# routes.py
from flask import Flask, render_template, request, jsonify
from models import Todo
from db import cursor, conn
from datetime import datetime

app = Flask(__name__)
#instantiate the model 
todo_model = Todo

# Define your routes here...
# Route to get all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    return jsonify(todos)


#route to get todos by ID
@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    cursor.execute("SELECT * FROM todos WHERE id =%s",(todo_id,) )
    todo = cursor.fetchone()
    if todo:
        return jsonify({'id':todo[0],'title':todo[1],'completed':todo[2],'priority':todo[3],'due_date':todo[4]})
    else:
        return jsonify({'message': 'Todo not found'}), 404

# Route to add a new todo
@app.route('/api/todos', methods=['POST'])
def add_todo():
        data = request.get_json()
        title = data.get('title')
        completed = data.get('completed')
        priority = data.get('priority')
        due_date_str = data.get('due_date')

        # Convert the due_date string to a datetime object
        due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%S")

        # Insert the new todo into the database
        cursor.execute("INSERT INTO todos (title, completed, priority, due_date) VALUES (%s, %s, %s, %s)",
                    (title, completed, priority, due_date))
        conn.commit()

        return jsonify({'message': 'Todo added successfully'})
#Route to delete a todo
@app.route("/api/todos/<int:todo_id>",methods=['DELETE'])
def delete_todo(todo_id):
    cursor.execute("DELETE FROM todos WHERE id=%s",(todo_id,))
    conn.commit()
    return jsonify({'message':f'Todo with the id {todo_id} deleted successfully'})

#Route to update a todo
@app.route("/api/todos/<int:todo_id>", methods=['PUT'])
def update_todo(todo_id):
    data=request.get_json()
    completed= data.get('completed')
    priority= data.get('priority')
    due_date=data.get('due_date')
    categories = data.get('categories', []) 
    cursor.execute("UPDATE todos SET completed = %s, priority = %s, due_date = %s WHERE id = %s",
                   (completed, priority, due_date, todo_id))
    
    cursor.execute
    conn.commit()
    return jsonify({'message':f"Todo {todo_id} updated successfully"})