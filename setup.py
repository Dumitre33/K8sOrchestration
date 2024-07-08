from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        requirements = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name='thesis',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'thesis=k8sconfig.run:main',
        ],
    },

    author='Alex Dumitre',
    author_email='alexandru.dumitre@gmail.com',
    url='https://github.com/Dumitre33/K8sOrchestration/tree/master/k8sconfig',
)
