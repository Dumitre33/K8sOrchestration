from quart import request, jsonify, render_template
from . import app
from app.services import (
    create_deployment,
    create_service,
    create_configmap,
    inject_configmap,
    create_pv,
    create_pvc,
    inject_pvc,
    delete_resource,
    show_resources
)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/create-deployment', methods=['POST'])
async def create_deployment_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = create_deployment(data)
    return await render_template('result.html', message=message)

@app.route('/create-service', methods=['POST'])
async def create_service_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = create_service(data)
    return await render_template('result.html', message=message)

@app.route('/create-configmap', methods=['POST'])
async def create_configmap_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = create_configmap(data)
    return await render_template('result.html', message=message)

@app.route('/inject-configmap', methods=['POST'])
async def inject_configmap_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = inject_configmap(data)
    return await render_template('result.html', message=message)

@app.route('/create-pv', methods=['POST'])
async def create_pv_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = create_pv(data)
    return await render_template('result.html', message=message)

@app.route('/create-pvc', methods=['POST'])
async def create_pvc_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = create_pvc(data)
    return await render_template('result.html', message=message)

@app.route('/inject-pvc', methods=['POST'])
async def inject_pvc_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = inject_pvc(data)
    return await render_template('result.html', message=message)

@app.route('/delete-resource', methods=['POST'])
async def delete_resource_route():
    try:
        data = await request.form
    except Exception:
        return await render_template('result.html', message="Invalid form data")

    message, success = delete_resource(data)
    return await render_template('result.html', message=message)

@app.route('/show-deployments', methods=['GET'])
async def show_deployments():
    deployments = show_resources('deployments')
    return await render_template('resources.html', title="Deployments", resources=deployments, resource_type='deployment')

@app.route('/show-services', methods=['GET'])
async def show_services():
    services = show_resources('services')
    return await render_template('resources.html', title="Services", resources=services, resource_type='service')

@app.route('/show-pods', methods=['GET'])
async def show_pods():
    pods = show_resources('pods')
    return await render_template('resources.html', title="Pods", resources=pods, resource_type='pod')

@app.route('/show-configmaps', methods=['GET'])
async def show_configmaps():
    configmaps = show_resources('configmaps')
    return await render_template('resources.html', title="ConfigMaps", resources=configmaps, resource_type='configmap')

@app.route('/show-pvcs', methods=['GET'])
async def show_pvcs():
    pvcs = show_resources('persistentvolumeclaims')
    return await render_template('resources.html', title="PersistentVolumeClaims", resources=pvcs, resource_type='persistentvolumeclaim')

@app.route('/show-pvs', methods=['GET'])
async def show_pvs():
    pvs = show_resources('persistentvolumes')
    return await render_template('resources.html', title="PersistentVolumes", resources=pvs, resource_type='persistentvolume')
