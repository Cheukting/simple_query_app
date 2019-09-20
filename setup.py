from setuptools import setup, find_packages

setup(
    name='simple_query_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==7.0',
        'pandas==0.24.2',
        'pytest==5.1.2',
        'testcontainers[mysql]==2.5'
    ],
    entry_points='''
        [console_scripts]
        simple_query_app=app.app:cli
    ''',
)
