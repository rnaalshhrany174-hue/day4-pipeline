import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_asset():
    return {
        'asset_id': 'A123',
        'name': 'Generator',
        'asset_type': 'Electrical',
        'location': 'Warehouse',
        'criticality': 'High',
        'status': 'active',
        'last_inspection_date': '2023-01-01',
        'operating_hours': 100,
        'notes': 'Routine check'
    }

def test_list_assets():
    response = client.get('/assets')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_asset(sample_asset):
    client.post('/assets', json=sample_asset)
    response = client.get('/assets/A123')
    assert response.status_code == 200
    assert response.json()['name'] == 'Generator'

def test_create_asset(sample_asset):
    response = client.post('/assets', json=sample_asset)
    assert response.status_code == 200
    assert response.json()['asset_id'] == 'A123'

def test_update_asset(sample_asset):
    client.post('/assets', json=sample_asset)
    updated_asset = sample_asset.copy()
    updated_asset['name'] = 'Updated Generator'
    response = client.put('/assets/A123', json=updated_asset)
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated Generator'

def test_delete_asset(sample_asset):
    client.post('/assets', json=sample_asset)
    response = client.delete('/assets/A123')
    assert response.status_code == 200
    assert response.json()['detail'] == 'Asset deleted'
    response = client.get('/assets/A123')
    assert response.status_code == 404