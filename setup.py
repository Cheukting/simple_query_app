from setuptools import setup, find_packages

setup(
    name='simple_query_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==7.0',
        'pandas==0.24.2',
        'pytest==5.1.2',
        'pytest-mock==1.10.4',
        'SQLAlchemy==1.3.8',
        'PyMySQL==0.9.3'
    ],
    entry_points='''
        [console_scripts]
        simple_query_app=app.app:cli
    ''',
)
