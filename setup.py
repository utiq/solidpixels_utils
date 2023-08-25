from setuptools import setup, find_packages

setup(
    name='sp_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'boto3'
    ]
)
