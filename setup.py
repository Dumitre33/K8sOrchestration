from setuptools import setup, find_packages

setup(
    name='k8s_app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'quart',
        'PyYAML',
        'pytest-asyncio',
    ],
    entry_points={
        'console_scripts': [
            'k8s_app=run:main',
        ],
    },
)

