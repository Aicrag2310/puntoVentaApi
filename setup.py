from setuptools import find_packages, setup

setup(
    name='punto-venta-api',
    version='1.0',
    packages=find_packages(exclude=('test', 'test.*', 'tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
)
