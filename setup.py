from setuptools import setup, find_packages

# Function to read the requirements.txt file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        requirements = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name='thesis',
    version='0.1',
    packages=find_packages(where='k8sconfig'),
    package_dir={'': 'k8sconfig'},
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'thesis=k8sconfig.run:main',
        ],
    },
    package_data={
        '': ['templates/*.html', 'static/*.css'],
    },

    author='Alex Dumitre', 
    author_email='alexandru.dumitre@gmail.com', 
    description='A python quart poject for Kubernetes management with Micork8s',
    long_description=open('README.md').read(),
    long_description_content_type='text',
    url='https://github.com/Dumitre33/K8sOrchestration/tree/master/k8sconfig',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.2',  
)