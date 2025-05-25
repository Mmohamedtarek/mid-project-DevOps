import json
from backend.app import app


def test_get_tasks(test_client):
    """Test GET /api/tasks endpoint"""
    response = test_client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'title' in data[0]


def test_create_task(test_client):
    """Test POST /api/tasks endpoint"""
    test_data = {
        'title': 'New Test Task',
        'description': 'New Description',
        'completed': False
    }
    response = test_client.post(
        '/api/tasks',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Test Task'
    assert data['completed'] is False


def test_update_task(test_client):
    """Test PUT /api/tasks/<id> endpoint"""
    with app.app_context():
        from backend.app import Task
        task = Task.query.first()
        test_data = {
            'title': 'Updated Title',
            'completed': True
        }
        response = test_client.put(
            f'/api/tasks/{task.id}',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
        assert data['completed'] is True


def test_delete_task(test_client):
    """Test DELETE /api/tasks/<id> endpoint"""
    with app.app_context():
        from backend.app import Task
        task = Task.query.first()
        response = test_client.delete(f'/api/tasks/{task.id}')
        assert response.status_code == 204
        
       
        deleted_task = Task.query.get(task.id)
        assert deleted_task is None


def test_health_check(test_client):
    """Test health check endpoint"""
    response = test_client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['database'] == 'connected'