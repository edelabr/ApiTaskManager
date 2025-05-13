from datetime import date, datetime
from sqlmodel import Session
from models.task import Task
from models.task_status import TaskStatus
from models.todo_list import TodoList
from models.user import User
from db.database import create_db_and_tables, drop_db_and_tables, engine


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
                User(username="user1", email="user1@example.com", hashed_password="password1", created_at=datetime.utcnow()),
                User(username="user2", email="user2@example.com", hashed_password="password2", created_at=datetime.utcnow()),
                User(username="user3", email="user3@example.com", hashed_password="password3", created_at=datetime.utcnow()),
                User(username="user4", email="user4@example.com", hashed_password="password4", created_at=datetime.utcnow()),
                User(username="user5", email="user5@example.com", hashed_password="password5", created_at=datetime.utcnow())
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
                TodoList(title="Gym Routine", description="Weekly gym routine", owner_id=3, created_at=datetime.utcnow()),
                TodoList(title="Reading List", description="Books to read", owner_id=4, created_at=datetime.utcnow()),
                TodoList(title="Travel Plans", description="Plan upcoming trips", owner_id=5, created_at=datetime.utcnow())
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
                Task(title="Leg day", description="Complete leg exercises", due_date=date(2025, 5, 18), is_completed=False, todo_list_id=3, status_id=3, created_at=datetime.utcnow()),
                Task(title="Read '1984'", description="Read the book '1984' by George Orwell", due_date=date(2025, 5, 30), is_completed=False, todo_list_id=4, status_id=4, created_at=datetime.utcnow()),
                Task(title="Book flights", description="Book flights for summer vacation", due_date=date(2025, 6, 10), is_completed=False, todo_list_id=5, status_id=5, created_at=datetime.utcnow())
            ]
            session.add_all(tasks)
            session.commit()
        except Exception as e:
            print(f"Error creating Tasks: {e}")


if __name__ == "__main__":
    seed_data()
