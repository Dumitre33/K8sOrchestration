from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='thesis', 
    version='0.2',  
    packages=find_packages(), 
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'start_program=thesis.k8s_config.run:main',
        ],
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