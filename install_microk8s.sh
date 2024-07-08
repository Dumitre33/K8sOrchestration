#!/bin/bash
# Update package list and install snapd
sudo apt update
sudo apt install -y snapd

# Install MicroK8s
sudo snap install microk8s --classic

# Add user to microk8s group and change ownership of kube directory
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube

# Create a new group session
newgrp microk8s

# Start MicroK8s
microk8s start

# Check MicroK8s status
microk8s status --wait-ready