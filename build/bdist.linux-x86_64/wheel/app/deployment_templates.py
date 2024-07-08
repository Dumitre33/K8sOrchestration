# deployment_templates.py

class KubernetesTemplates:
    DEPLOYMENT_TEMPLATE = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": None
        },
        "spec": {
            "replicas": None,
            "selector": {
                "matchLabels": {
                    "app": None
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": None
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": None,
                            "image": None,
                            "ports": [
                                {
                                    "containerPort": None
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    SERVICE_TEMPLATE = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": None
        },
        "spec": {
            "type": None,
            "selector": {
                "app": None
            },
            "ports": [
                {
                    "protocol": None,
                    "port": None,
                    "targetPort": None
                }
            ]
        }
    }

    CONFIGMAP_TEMPLATE = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": None
        },
        "data": None
    }

    PATCH_CONFIGMAP_TEMPLATE = {
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": None,
                            "volumeMounts": [
                                {
                                    "name": None,
                                    "mountPath": None
                                }
                            ]
                        }
                    ],
                    "volumes": [
                        {
                            "name": None,
                            "configMap": {
                                "name": None
                            }
                        }
                    ]
                }
            }
        }
    }

    PERSISTENT_VOLUME_TEMPLATE = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": None
        },
        "spec": {
            "capacity": {
                "storage": None
            },
            "accessModes": None,
            "hostPath": {
                "path": "/mnt/data"
            }
        }
    }

    PERSISTENT_VOLUME_CLAIM_TEMPLATE = {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {
            "name": None
        },
        "spec": {
            "accessModes": None,
            "resources": {
                "requests": {
                    "storage": None
                }
            }
        }
    }

    PATCH_PVC_TEMPLATE = {
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": None,
                            "volumeMounts": [
                                {
                                    "name": None,
                                    "mountPath": None
                                }
                            ]
                        }
                    ],
                    "volumes": [
                        {
                            "name": None,
                            "persistentVolumeClaim": {
                                "claimName": None
                            }
                        }
                    ]
                }
            }
        }
    }
