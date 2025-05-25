def test_swagger_ui(test_client):
    response = test_client.get('/api/docs')
    assert response.status_code == 200
    assert b'Task Manager API' in response.data