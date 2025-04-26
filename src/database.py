import sqlite3

class TaskDatabase:
    def __init__(self, db_name = "data/task_manager.db"):
        self.db_name = db_name

        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        due_date TEXT NOT NULL,
                        category TEXT NOT NULL
                    )
                """)
                conn.commit()

    def add_task(self, title, description, due_date, category):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tasks (title, description, due_date, category) VALUES (?, ?, ?, ?)",
                    (title, description, due_date, category)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            return False
        
    def view_tasks(self, category=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if category:
                    cursor.execute("SELECT * FROM tasks WHERE category = ?", (category,))
                else:
                    cursor.execute("SELECT * FROM tasks")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing tasks: {e}")
            return []
                
    def update_task(self, task_id, title=None, description=None, due_date=None, category=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                updates = []
                values = []
                if title:
                    updates.append("title = ?")
                    values.append(title)
                if description:
                    updates.append("description = ?")
                    values.append(description)
                if due_date:
                    updates.append("due_date = ?")
                    values.append(due_date)
                if category:
                    updates.append("category = ?")
                    values.append(category)
                if not updates:
                    return False
                values.append(task_id)
                query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating task: {e}")
            return False
        
if __name__ == "__main__":
    db = TaskDatabase()
    # Add a task
    if db.add_task("Test Task", "This is a test", "2025-05-01", "Work"):
        print("Task added successfully")
    else:
        print("Failed to add task")
    # Update the task
    if db.update_task(1, title="Updated Task", due_date="2025-06-01"):
        print("Task updated successfully")
    else:
        print("Failed to update task")
    # View tasks to confirm
    tasks = db.view_tasks("Work")
    print("Work tasks:", tasks)
    tasks = db.view_tasks()
    print("All tasks:", tasks)