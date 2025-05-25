from datetime import datetime
from app import db, Task
from app import app


def test_task_model():
    with app.app_context():
        task = Task(
            title='Unit Test Task',
            description='This is a test task',
            completed=True
        )
        db.session.add(task)
        db.session.commit()

        assert task.id is not None
        assert task.title == 'Unit Test Task'
        assert task.completed is True
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

        task_dict = task.to_dict()
        assert isinstance(task_dict, dict)
        assert 'id' in task_dict
        assert task_dict['title'] == 'Unit Test Task'
