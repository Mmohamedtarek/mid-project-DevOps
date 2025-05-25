import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Task


@pytest.fixture(scope='module')
def test_client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            db.session.add(Task(title='Test Task', description='Test', completed=False))
            db.session.commit()

        yield testing_client

        with app.app_context():
            db.drop_all()
