# models.py
from datetime import datetime

class Todo:
    def __init__(self, id, title, completed, priority, due_date, categories):
        self.id = id
        self.title = title
        self.completed = completed
        self.priority = priority
        self.due_date = due_date
        self.categories = categories
