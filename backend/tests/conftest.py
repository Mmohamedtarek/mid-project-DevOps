import sys
import os
import pytest

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)

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

            db.session.add(
                Task(title='Test Task', description='Test', completed=False)
            )
            db.session.commit()

        yield testing_client

        with app.app_context():
            db.drop_all()
