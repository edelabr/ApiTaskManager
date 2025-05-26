from datetime import date, datetime
from sqlmodel import Session
from app.auth.hashing import hash_password
from app.models.task import Task
from app.models.task_status import TaskStatus
from app.models.todo_list import TodoList
from app.models.user import User
from app.db.database import create_db_and_tables, drop_db_and_tables, engine

def seed_data():
    # Borrar la base de datos y las tablas existentes
    drop_db_and_tables() 
    # Crear la base de datos y las tablas
    create_db_and_tables()
    # Insertar los datos falsos
    insert_fake_data()

# Función para insertar datos falsos
def insert_fake_data():
    with Session(engine) as session:
        try:
            # Crear datos falsos para TaskStatus
            task_statuses = [
                TaskStatus(name="Pending", color="Red"),
                TaskStatus(name="In Progress", color="Yellow"),
                TaskStatus(name="Completed", color="Green"),
                TaskStatus(name="On Hold", color="Blue"),
                TaskStatus(name="Cancelled", color="Gray")
            ]
            session.add_all(task_statuses)
            session.commit()
        except Exception as e:
            print(f"Error creating TaskStatus: {e}")

        try:
            # Crear datos falsos para User
            users = [
                User(username="user_admin", email="user_admin@example.com", hashed_password=hash_password("user_admin"), role="admin", created_at=datetime.utcnow()),
                User(username="user_user", email="user_user@example.com", hashed_password=hash_password("user_user"), role="user", created_at=datetime.utcnow()),
                User(username="user_viewer", email="user_viewer@example.com", hashed_password=hash_password("user_viewer"), role="viewer", created_at=datetime.utcnow())
            ]
            session.add_all(users)
            session.commit()
        except Exception as e:
            print(f"Error creating Users: {e}")

        try:
            # Crear datos falsos para TodoList
            todo_lists = [
                TodoList(title="Groceries", description="Buy groceries for the week", owner_id=1, created_at=datetime.utcnow()),
                TodoList(title="Work Tasks", description="Complete work-related tasks", owner_id=2, created_at=datetime.utcnow()),
                TodoList(title="Gym Routine", description="Weekly gym routine", owner_id=3, created_at=datetime.utcnow())
            ]
            session.add_all(todo_lists)
            session.commit()
        except Exception as e:
            print(f"Error creating TodoLists: {e}")

        try:
            # Crear datos falsos para Task
            tasks = [
                Task(title="Buy milk", description="Buy 2 liters of milk", due_date=date(2025, 5, 20), is_completed=False, todo_list_id=1, status_id=1, created_at=datetime.utcnow()),
                Task(title="Finish report", description="Complete the quarterly report", due_date=date(2025, 5, 25), is_completed=False, todo_list_id=2, status_id=2, created_at=datetime.utcnow()),
                Task(title="Leg day", description="Complete leg exercises", due_date=date(2025, 5, 18), is_completed=False, todo_list_id=3, status_id=3, created_at=datetime.utcnow())
            ]
            session.add_all(tasks)
            session.commit()
        except Exception as e:
            print(f"Error creating Tasks: {e}")

if __name__ == "__main__":
    seed_data()
