import pytest
from app import app, db, Task 


@pytest.fixture(scope='module')
def test_client():
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        test_task = Task(title='Test Task', description='Test', completed=False)
        db.session.add(test_task)
        db.session.commit()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.session.remove()
        db.drop_all()
