import requests
import re
from app.config_generator import (
    generate_kubernetes_deployment_config,
    generate_kubernetes_service_config,
    generate_kubernetes_configmap_config,
    generate_kubernetes_patch_for_configmap,
    generate_persistent_volume_config,
    generate_persistent_volume_claim_config,
    generate_persistent_volume_claim_patch
)
from app.k8s_utils import deploy_to_microk8s, patch_deployment_with_configmap, patch_deployment_with_pvc, get_kubernetes_resources, delete_kubernetes_resource


def is_valid_kubernetes_name(name):
    
    pattern = re.compile(r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?$')
    return pattern.match(name) is not None

def check_docker_image_exists(image_name):
    try:
        # Split the image name to get repository and image
        repository, image = image_name.split('/')
    except ValueError:
        repository = 'library'
        image = image_name

    # Docker Hub API URL
    url = f"https://hub.docker.com/v2/repositories/{repository}/{image}/tags/latest/"

    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False




submitted_configs = {}

def create_deployment(data):
    service_name = data.get('service_name')
    app_label = data.get('app_label')
    image = data.get('image')
    port = data.get('port')
    replicas = data.get('replicas')

    if not service_name or not image or not port or not replicas:
        return "Missing required fields", False

    if not is_valid_kubernetes_name(service_name):
        return "Invalid service name. Must be lowercase, contain only alphanumeric characters, '-', and '.', and start and end with an alphanumeric character.", False

    if not is_valid_kubernetes_name(app_label):
        return "Invalid app label. Must be lowercase, contain only alphanumeric characters, '-', and '.', and start and end with an alphanumeric character.", False

    # Validate image existence on Docker Hub
    if not check_docker_image_exists(image):
        return "Docker image does not exist on Docker Hub", False

    try:
        port = int(port)
        replicas = int(replicas)
    except ValueError:
        return "Invalid port or replicas", False

    deployment_config = generate_kubernetes_deployment_config(service_name, app_label, image, port, replicas)

    if deploy_to_microk8s(deployment_config, deployment_config):
        submitted_configs[(service_name, image, port, replicas)] = True
        return "Kubernetes deployment created successfully", True
    else:
        return "Failed to create Kubernetes deployment", False


def create_service(data):
    service_name = data.get('service_name')
    app_label = data.get('app_label')
    port = data.get('port')
    target_port = data.get('target_port')
    protocol = data.get('protocol')
    service_type = data.get('type')


    if not service_name or not app_label or not port or not target_port or not protocol or not service_type:
        return "Missing required fields", False

    if not is_valid_kubernetes_name(service_name):
        return "Invalid service name. Must be lowercase, contain only alphanumeric characters, '-', and '.', and start and end with an alphanumeric character.", False

    if not is_valid_kubernetes_name(app_label):
        return "Invalid app label. Must be lowercase, contain only alphanumeric characters, '-', and '.', and start and end with an alphanumeric character.", False

    try:
        port = int(port)
        target_port = int(target_port)
    except ValueError:
        return "Invalid port or target port", False

    service_config = generate_kubernetes_service_config(service_name, app_label, port, target_port, protocol, service_type)

    if deploy_to_microk8s(service_config, service_config):
        submitted_configs[(service_name, app_label, port, target_port, protocol, service_type)] = True
        return "Kubernetes service created successfully", True
    else:
        return "Failed to create Kubernetes service", False


def create_configmap(data):
    configmap_name = data.get('configmap_name')
    config_data = data.get('data')

    if not configmap_name or not config_data:
        return "Missing required fields", False

    config_data = dict(item.split('=') for item in config_data.split(','))

    configmap_config = generate_kubernetes_configmap_config(configmap_name, config_data)

    if deploy_to_microk8s(configmap_config, configmap_config):
        return "Kubernetes ConfigMap deployed successfully", True
    else:
        return "Failed to deploy Kubernetes ConfigMap", False

def inject_configmap(data):
    deployment_name = data.get('deployment_name')
    container_name = data.get('container_name')
    configmap_name = data.get('configmap_name')
    mount_path = data.get('mount_path')

    if not deployment_name or not container_name or not configmap_name or not mount_path:
        return "Missing required fields", False

    patch_config = generate_kubernetes_patch_for_configmap(deployment_name, container_name, configmap_name, mount_path)

    if patch_deployment_with_configmap(deployment_name, patch_config):
        return "Kubernetes ConfigMap injected successfully", True
    else:
        return "Failed to inject Kubernetes ConfigMap", False

def create_pv(data):
    pv_name = data.get('pv_name')
    capacity = data.get('capacity')
    access_modes = data.get('access_modes')

    if not pv_name or not capacity or not access_modes:
        return "Missing required fields", False

    access_modes = access_modes.split(',')

    pv_config = generate_persistent_volume_config(pv_name, capacity, access_modes)

    if deploy_to_microk8s(pv_config, pv_config):
        return "PersistentVolume created successfully", True
    else:
        return "Failed to create PersistentVolume", False

def create_pvc(data):
    pvc_name = data.get('pvc_name')
    capacity = data.get('capacity')
    access_modes = data.get('access_modes')

    if not pvc_name or not capacity or not access_modes:
        return "Missing required fields", False

    access_modes = access_modes.split(',')

    pvc_config = generate_persistent_volume_claim_config(pvc_name, capacity, access_modes)

    if deploy_to_microk8s(pvc_config, pvc_config):
        return "PersistentVolumeClaim created successfully", True
    else:
        return "Failed to create PersistentVolumeClaim", False

def inject_pvc(data):
    deployment_name = data.get('deployment_name')
    container_name = data.get('container_name')
    pvc_name = data.get('pvc_name')
    mount_path = data.get('mount_path')

    if not deployment_name or not container_name or not pvc_name or not mount_path:
        return "Missing required fields", False

    patch_config = generate_persistent_volume_claim_patch(deployment_name, container_name, pvc_name, mount_path)

    if patch_deployment_with_pvc(deployment_name, patch_config):
        return "PersistentVolumeClaim injected successfully", True
    else:
        return "Failed to inject PersistentVolumeClaim", False

def delete_resource(data):
    resource_type = data.get('resource_type')
    resource_name = data.get('resource_name')

    if not resource_type or not resource_name:
        return "Missing required fields", False

    if delete_kubernetes_resource(resource_type, resource_name):
        return f"{resource_type.capitalize()} '{resource_name}' deleted successfully", True
    else:
        return f"Failed to delete {resource_type} '{resource_name}'", False

def show_resources(resource_type):
    resources = get_kubernetes_resources(resource_type)
    return resources
