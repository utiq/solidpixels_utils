from setuptools import setup, find_packages

setup(
    name='sp_utils',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'boto3'
    ]
)
