# tests/test_k8s_utils.py

from unittest.mock import MagicMock, patch
import pytest

from app.k8s_utils import deploy_to_microk8s

# Test function
@patch('app.k8s_utils.subprocess.run')
@pytest.mark.parametrize("deployment_config, service_config, expected_result", [
    ("deployment_config_content", "service_config_content", True),  # Test case 1: Successful deployment
    ("", "", False),  # Test case 2: Empty configurations
    ("deployment_config_content", "", False),  # Test case 3: Missing service configuration
    ("", "service_config_content", False),  # Test case 4: Missing deployment configuration
])
def test_deploy_to_microk8s(subprocess_run_mock, deployment_config, service_config, expected_result):
    # Call deploy_to_microk8s with the mocked configurations
    result = deploy_to_microk8s(deployment_config, service_config)

    # Assertions
    assert result == expected_result

    # Ensure subprocess.run was not called when configurations are empty
    if not deployment_config or not service_config:
        assert subprocess_run_mock.call_count == 0
    else:
        # Ensure subprocess.run was called with the correct arguments
        assert subprocess_run_mock.call_count == 2  # Two calls: one for deployment, one for service
        assert subprocess_run_mock.call_args_list[0][0][0] == ['microk8s', 'kubectl', 'apply', '-f', '/tmp/kubernetes_deployment.yaml']
        assert subprocess_run_mock.call_args_list[1][0][0] == ['microk8s', 'kubectl', 'apply', '-f', '/tmp/kubernetes_service.yaml']
