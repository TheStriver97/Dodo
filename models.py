# models.py
class Todo:
    def __init__(self, id, title, completed, priority, due_date, categories):
        self.id = id
        self.title = title
        self.completed = completed
        self.priority = priority
        self.due_date = due_date
        self.categories = categories

    @classmethod
    def from_db(cls, db_row):
        return cls(*db_row)
