#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root or use sudo."
    exit 1
fi

# Install necessary dependencies
apt update
apt install -y python3 python3-pip git

# Clone the repository
git clone https://github.com/Dumitre33/K8sOrchestration.git
cd K8sOrchestration

# Install the wheel
pip install dist/thesis-0.4-py3-none-any.whl


./install_microk8s.sh


# Run the application
cd k8sconfig/
python3 run.py
