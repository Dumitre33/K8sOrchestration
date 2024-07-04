import yaml
from .deployment_templates import KubernetesTemplates
# function to create a dicionary which represents a k8s deployment configuration
def generate_kubernetes_deployment_config(deployment_name, app_label, image, port, replicas):
    deployment_config = KubernetesTemplates.DEPLOYMENT_TEMPLATE.copy()
    deployment_config['metadata']['name'] = deployment_name
    deployment_config['spec']['replicas'] = replicas
    deployment_config['spec']['selector']['matchLabels']['app'] = app_label
    deployment_config['spec']['template']['metadata']['labels']['app'] = app_label
    deployment_config['spec']['template']['spec']['containers'][0]['name'] = deployment_name 
    deployment_config['spec']['template']['spec']['containers'][0]['image'] = image
    deployment_config['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = port
    return yaml.dump(deployment_config)

def generate_kubernetes_service_config(service_name,app_label, port, target_port, protocol, service_type):
    service_config = KubernetesTemplates.SERVICE_TEMPLATE.copy()
    service_config['metadata']['name'] = service_name
    service_config['spec']['type'] = service_type
    service_config['spec']['selector']['app'] = app_label
    service_config['spec']['ports'][0]['protocol'] = protocol
    service_config['spec']['ports'][0]['port'] = port
    service_config['spec']['ports'][0]['targetPort'] = target_port
    return yaml.dump(service_config)

def generate_kubernetes_configmap_config(configmap_name, config_data):
    configmap_config = KubernetesTemplates.CONFIGMAP_TEMPLATE.copy()
    configmap_config['metadata']['name'] = configmap_name
    configmap_config['data'] = config_data
    return yaml.dump(configmap_config)

def generate_kubernetes_patch_for_configmap(deployment_name, container_name, configmap_name, mount_path):
    patch_config = KubernetesTemplates.PATCH_CONFIGMAP_TEMPLATE.copy()
    patch_config['spec']['template']['spec']['containers'][0]['name'] = container_name
    patch_config['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = configmap_name
    patch_config['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = mount_path
    patch_config['spec']['template']['spec']['volumes'][0]['name'] = configmap_name
    patch_config['spec']['template']['spec']['volumes'][0]['configMap']['name'] = configmap_name
    return yaml.dump(patch_config)

def generate_persistent_volume_config(pv_name, capacity, access_modes):
    pv_config = KubernetesTemplates.PERSISTENT_VOLUME_TEMPLATE.copy()
    pv_config['metadata']['name'] = pv_name
    pv_config['spec']['capacity']['storage'] = capacity
    pv_config['spec']['accessModes'] = access_modes
    return yaml.dump(pv_config)

def generate_persistent_volume_claim_config(pvc_name, capacity, access_modes):
    pvc_config = KubernetesTemplates.PERSISTENT_VOLUME_CLAIM_TEMPLATE.copy()
    pvc_config['metadata']['name'] = pvc_name
    pvc_config['spec']['accessModes'] = access_modes
    pvc_config['spec']['resources']['requests']['storage'] = capacity
    return yaml.dump(pvc_config)

def generate_persistent_volume_claim_patch(deployment_name, container_name, pvc_name, mount_path):
    patch_config = KubernetesTemplates.PATCH_PVC_TEMPLATE.copy()
    patch_config['spec']['template']['spec']['containers'][0]['name'] = container_name
    patch_config['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = pvc_name
    patch_config['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = mount_path
    patch_config['spec']['template']['spec']['volumes'][0]['name'] = pvc_name
    patch_config['spec']['template']['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] = pvc_name
    return yaml.dump(patch_config)
