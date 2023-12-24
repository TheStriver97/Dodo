# routes.py
from flask import Flask, request, jsonify
from models import Todo
from db import cursor, conn
from datetime import datetime

app = Flask(__name__)

# Route to get all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()

    # Convert the raw database results into Todo objects
    todos = [Todo.from_db(todo) for todo in todos]

    return jsonify([todo.__dict__ for todo in todos])

# Route to get todos by ID
@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    todo = cursor.fetchone()
    if todo:
        todo_obj = Todo.from_db(todo)
        return jsonify(todo_obj.__dict__)
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
    categories=data.get('categories')

    # Convert the due_date string to a datetime object
    due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%S")

    # Create a new Todo object
    new_todo = Todo(None, title, completed, priority, due_date, None)

    # Insert the new todo into the database
    cursor.execute("INSERT INTO todos (title, completed, priority, due_date) VALUES (%s, %s, %s, %s)",
                   (new_todo.title, new_todo.completed, new_todo.priority, new_todo.due_date))
    conn.commit()

    return jsonify({'message': 'Todo added successfully'})
# Route to delete a todo
@app.route("/api/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    cursor.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
    conn.commit()
    return jsonify({'message': f'Todo with the id {todo_id} deleted successfully'})


# Route to update a 
@app.route("/api/todos/<int:todo_id>", methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    completed = data.get('completed')
    priority = data.get('priority')
    due_date = data.get('due_date')
    category_name = data.get('category')  # Assuming 'category' is sent as a string

    # Retrieve the category_id based on the category_name
    cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
    category_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

    cursor.execute("UPDATE todos SET completed = %s, priority = %s, due_date = %s, category_id = %s WHERE id = %s",
                   (completed, priority, due_date, category_id, todo_id))

    conn.commit()
    return jsonify({'message': f"Todo {todo_id} updated successfully"})
if __name__ == '__main__':
    app.run(debug=True)
