import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from app import app as myapp 
import nose
import pytest
from quart.testing import QuartClient

client_under_test = None

def setup_module():
    client_under_test=QuartClient(myapp)
    assert client_under_test != None

def teardown_module():
    client_under_test=None

@pytest.mark.asyncio
@nose.with_setup(setup_module, teardown_module)
async def test_create_deployment():    
    data = {
        "service_name": "test-deployment",
        "image": "nginx",
        "port": 8080,
        "replicas": 3
    }
    response = await client_under_test.post('/create-deployment', form=data)
    assert response.status_code == 200

    response_text = await response.get_data(as_text=True)
    assert "Kubernetes deployment created successfully" in response_text


# Test creating a service with valid data
@nose.with_setup(setup_module, teardown_module)
def test_create_service():
    data = {
        "service_name": "test-service",
        "port": 8080,
        "target_port": 80,
        "protocol": "TCP",
        "type": "ClusterIP"
    }
    response = client_under_test.post('/create-service', form=data)
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Kubernetes service created successfully" in response_text

# Test creating a ConfigMap with valid data
@nose.with_setup(setup_module, teardown_module)
def test_create_configmap():
    data = {
        "configmap_name": "test-configmap",
        "data": "key1=value1,key2=value2"
    }
    response = client_under_test.post('/create-configmap', form=data)
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Kubernetes ConfigMap deployed successfully" in response_text

# Test injecting a ConfigMap with valid data
@nose.with_setup(setup_module, teardown_module)
def test_inject_configmap():
    data = {
        "deployment_name": "qq",
        "container_name": "qq",
        "configmap_name": "sql1",
        "mount_path": "/etc/config"
    }
    response = client_under_test.post('/inject-configmap', form=data)
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Kubernetes ConfigMap injected successfully" in response_text

# Test creating a deployment with missing fields
@nose.with_setup(setup_module, teardown_module)
def test_create_deployment_missing_fields():
    data = {
        "service_name": "test-deployment-missing-fields"
    }
    response = client_under_test.post('/create-deployment', form=data)
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Missing required fields" in response_text

# Test creating a service with missing fields
@nose.with_setup(setup_module, teardown_module)
def test_create_service_missing_fields():
    data = {
        "service_name": "test-service-missing-fields"
    }
    response = client_under_test.post('/create-service', form=data)
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Missing required fields" in response_text

# Test creating a deployment with duplicate data
@nose.with_setup(setup_module, teardown_module)
def test_create_duplicate_deployment():
    data = {
        "service_name": "duplicate-deployment",
        "image": "nginx",
        "port": 8080,
        "replicas": 3
    }
    client_under_test.post('/create-deployment', form=data)  # First attempt
    response = client_under_test.post('/create-deployment', form=data)  # Duplicate attempt
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Duplicate deployment configuration detected" in response_text

# Test creating a service with duplicate data
@nose.with_setup(setup_module, teardown_module)
async def test_create_duplicate_service():
    data = {
        "service_name": "duplicate-service",
        "port": 8080,
        "target_port": 80,
        "protocol": "TCP",
        "type": "ClusterIP"
    }
    client_under_test.post('/create-service', form=data)  # First attempt
    response = client_under_test.post('/create-service', form=data)  # Duplicate attempt
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Duplicate service configuration detected" in response_text

# Test retrieving deployments
@nose.with_setup(setup_module, teardown_module)
async def test_show_deployments():
    response = client_under_test.get('/show-deployments')
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Deployments" in response_text

# Test retrieving services
@nose.with_setup(setup_module, teardown_module)
async def test_show_services():
    response = client_under_test.get('/show-services')
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Services" in response_text

# Test retrieving pods
@nose.with_setup(setup_module, teardown_module)
async def test_show_pods():
    response = client_under_test.get('/show-pods')
    assert response.status_code == 200

    response_text = response.get_data(as_text=True)
    assert "Pods" in response_text


if __name__ == '__main__':
    nose.run(defaultTest=__name__)