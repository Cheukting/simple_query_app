from setuptools import setup, find_packages

setup(
    name='simple_query_app',
    version='0.1',
    py_modules=['app'],
    install_requires=[
        'click == 7.0',
        #'mysql-connector == 2.2.9',
        'pandas == 0.24.2',
        'pytest == 5.1.2',
        'testcontainers[mysql]'
    ],
    entry_points='''
        [console_scripts]
        simple_query_app=app:cli
    ''',
)
