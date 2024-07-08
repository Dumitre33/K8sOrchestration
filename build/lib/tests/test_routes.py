import pytest
from quart.testing import QuartClient
from app import app

@pytest.fixture
@pytest.mark.asyncio
async def client():
    async with QuartClient(app) as client:
        yield client

# Test creating a deployment with valid data
@pytest.mark.asyncio
async def test_create_deployment(client):
    data = {
        "service_name": "test-deployment",
        "image": "nginx",
        "port": 8080,
        "replicas": 3
    }
    response = await client.post('/create-deployment', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Kubernetes deployment created successfully" in response_text

# Test creating a service with valid data
@pytest.mark.asyncio
async def test_create_service(client):
    data = {
        "service_name": "test-service",
        "app_label": "test1",
        "port": 8080,
        "target_port": 80,
        "protocol": "TCP",
        "type": "ClusterIP"
    }
    response = await client.post('/create-service', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Kubernetes service created successfully" in response_text

# Test creating a ConfigMap with valid data
@pytest.mark.asyncio
async def test_create_configmap(client):
    data = {
        "configmap_name": "sql1",
        "data": "key1=value1,key2=value2"
    }
    response = await client.post('/create-configmap', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Kubernetes ConfigMap deployed successfully" in response_text

# Test injecting a ConfigMap with valid data
@pytest.mark.asyncio
async def test_inject_configmap(client):
    data = {
        "deployment_name": "test1",
        "container_name": "test1",
        "configmap_name": "sql1",
        "mount_path": "/etc/config"
    }
    response = await client.post('/inject-configmap', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Kubernetes ConfigMap injected successfully" in response_text

# Test creating a deployment with missing fields
@pytest.mark.asyncio
async def test_create_deployment_missing_fields(client):
    data = {
        "service_name": "test-deployment-missing-fields"
    }
    response = await client.post('/create-deployment', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Missing required fields" in response_text

# Test creating a service with missing fields
@pytest.mark.asyncio
async def test_create_service_missing_fields(client):
    data = {
        "service_name": "test-service-missing-fields"
    }
    response = await client.post('/create-service', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Missing required fields" in response_text

# Test creating a deployment with duplicate data
@pytest.mark.asyncio
async def test_create_duplicate_deployment(client):
    data = {
        "service_name": "duplicate-deployment",
        "image": "nginx",
        "port": 8080,
        "replicas": 3
    }
    await client.post('/create-deployment', form=data)  # First attempt
    response = await client.post('/create-deployment', form=data)  # Duplicate attempt
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Duplicate deployment configuration detected" in response_text

# Test creating a service with duplicate data
@pytest.mark.asyncio
async def test_create_duplicate_service(client):
    data = {
        "service_name": "duplicate-service",
        "app_label": "test1",
        "port": 8080,
        "target_port": 80,
        "protocol": "TCP",
        "type": "ClusterIP"
    }
    await client.post('/create-service', form=data)  # First attempt
    response = await client.post('/create-service', form=data)  # Duplicate attempt
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Duplicate service configuration detected" in response_text

# Test retrieving deployments
@pytest.mark.asyncio
async def test_show_deployments(client):
    response = await client.get('/show-deployments')
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Deployments" in response_text

# Test retrieving services
@pytest.mark.asyncio
async def test_show_services(client):
    response = await client.get('/show-services')
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Services" in response_text

# Test retrieving pods
@pytest.mark.asyncio
async def test_show_pods(client):
    response = await client.get('/show-pods')
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Pods" in response_text