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

if __name__ == "__main__":
    db = TaskDatabase()