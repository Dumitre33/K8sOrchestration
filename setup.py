from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        requirements = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return requirements


setup(
    name='thesis',
    version='0.4',
    packages=find_packages(include=['k8sconfig', 'k8sconfig.*']),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'thesis=k8sconfig.run:main',
        ],
    },
    package_data={
        'k8sconfig': [
            'templates/*.html',
            'static/*.css',
            'tests/*.py',
        ],
    },
    data_files=[
        ('k8sconfig', [
            'k8sconfig/locustfile.py',
            'k8sconfig/run.py',
            'k8sconfig/pytest.ini'
        ]),
    ],

    author='Alex Dumitre',
    author_email='alexandru.dumitre@gmail.com',
    url='https://github.com/Dumitre33/K8sOrchestration/tree/master/k8sconfig',
)
