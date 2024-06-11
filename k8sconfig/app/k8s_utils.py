import subprocess
import os

def deploy_to_microk8s(deployment_config, service_config):
    if not deployment_config or not service_config:
        print("Missing configurations")
        return False

    try:
        prev_deployment_config = ""
        if os.path.exists('/tmp/kubernetes_deployment.yaml'):
            with open('/tmp/kubernetes_deployment.yaml', 'r') as f:
                prev_deployment_config = f.read()

        prev_service_config = ""
        if os.path.exists('/tmp/kubernetes_service.yaml'):
            with open('/tmp/kubernetes_service.yaml', 'r') as f:
                prev_service_config = f.read()

        if deployment_config == prev_deployment_config and service_config == prev_service_config:
            print("Duplicate configurations detected.")
            return False

        with open('/tmp/kubernetes_deployment.yaml', 'w') as f:
            f.write(deployment_config)

        with open('/tmp/kubernetes_service.yaml', 'w') as f:
            f.write(service_config)

        subprocess.run(['microk8s', 'kubectl', 'apply', '-f', '/tmp/kubernetes_deployment.yaml'], check=True)
        subprocess.run(['microk8s', 'kubectl', 'apply', '-f', '/tmp/kubernetes_service.yaml'], check=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error deploying Kubernetes configurations: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def patch_deployment_with_configmap(deployment_name, patch_config):
    try:
        with open('/tmp/kubernetes_patch.yaml', 'w') as f:
            f.write(patch_config)

        subprocess.run(['microk8s', 'kubectl', 'patch', 'deployment', deployment_name, '--patch-file', '/tmp/kubernetes_patch.yaml'], check=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error patching deployment with ConfigMap: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def patch_deployment_with_pvc(deployment_name, patch_config):
    try:
        with open('/tmp/kubernetes_pvc_patch.yaml', 'w') as f:
            f.write(patch_config)

        subprocess.run(['microk8s', 'kubectl', 'patch', 'deployment', deployment_name, '--patch-file', '/tmp/kubernetes_pvc_patch.yaml'], check=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error patching deployment with PVC: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def get_kubernetes_resources(resource_type):
    try:
        result = subprocess.run(['microk8s', 'kubectl', 'get', resource_type, '-o', 'jsonpath={.items[*].metadata.name}'],
                                capture_output=True, text=True, check=True)
        resources = result.stdout.split()
        return resources
    except subprocess.CalledProcessError as e:
        print(f"Error getting Kubernetes {resource_type}: {e}")
        return []



def delete_kubernetes_resource(resource_type, resource_name):
    
    try:
        subprocess.run(['microk8s', 'kubectl', 'delete', resource_type, resource_name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error deleting Kubernetes {resource_type} '{resource_name}': {e}")
        return False