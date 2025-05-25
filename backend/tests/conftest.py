import os
import pytest
from app import app, db, Task


@pytest.fixture(scope='module')
def test_client():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            test_task = Task(title='Test Task', description='Test', completed=False)
            db.session.add(test_task)
            db.session.commit()

        yield testing_client

        with app.app_context():
            db.drop_all()
