import pytest
from backend.app import app, db
from backend.app import Task
import os

@pytest.fixture(scope='module')
def test_client():
    # استخدام قاعدة بيانات مؤقتة للاختبارات
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            # إضافة بيانات اختبارية
            test_task = Task(
                title='Test Task',
                description='Test Description',
                completed=False
            )
            db.session.add(test_task)
            db.session.commit()
        yield testing_client
        with app.app_context():
            db.drop_all()