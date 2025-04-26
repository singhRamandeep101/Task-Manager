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

if __name__ == "__main__":
    db = TaskDatabase()
    db.add_task("Test Task", "This is a test", "2025-05-01", "Work")