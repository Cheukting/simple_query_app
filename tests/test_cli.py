#!/usr/bin/env python
import click
from click.testing import CliRunner
import unittest.mock as mock
import pandas as pd

import sys
import os
# patching for the app path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
#from simple_query_app.util import *

def test_read_csv_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('fail_example.csv', 'w') as f:
            f.write('it is suppose to fail')

        result = runner.invoke(app.load, ['fail_example.csv'])
        assert result.exit_code == 0
        assert result.output == 'Loading data into database...\nAbort. Incorrect file format.\n'

def test_read_csv_success(mocker):
    #import pdb; pdb.set_trace()
    mocker.patch('app.app.load_file_to_db', autospec=True)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('success_example.csv', 'w') as f:
            f.write('firstname,lastname,email\n'
                    'John,Smith,john.smith@gmail.com\n'
                    'Ada,Wong,a.wong@gmail.com\n')

        result = runner.invoke(app.load, ['success_example.csv'])
        assert app.load_file_to_db.call_count == 1
        assert result.exit_code == 0
        assert result.output == 'Loading data into database...\n2 row(s) of data loaded.\n'

def test_search_no_match(mocker):
    result_df = pd.DataFrame()
    mocker.patch('app.app.look_up_from_db', return_value=result_df)
    runner = CliRunner()
    result = runner.invoke(app.search, ['firstname','John'])
    assert result.exit_code == 0
    assert result.output.split('\n')[0] == f"Searching for user with 'firstname' as 'John'..."
    assert result.output.split('\n')[1] == '2 matche(s) found:'

def test_search_success(mocker):
    result_df = pd.DataFrame({'firstname':['John','John'],
                              'lastname':['Smith','Smith'],
                              'email':['john.smith@gmail.com','j.smith@gmail.com']},
                              columns = ['firstname','lastname','email'])
    mocker.patch('app.app.look_up_from_db', return_value=result_df)
    runner = CliRunner()
    result = runner.invoke(app.search, ['firstname','John'])
    assert result.exit_code == 0
    assert result.output.split('\n')[0] == f"Searching for user with 'firstname' as 'John'..."
    assert result.output.split('\n')[1] == '2 matche(s) found:'


#def test_hello_world():
#    @click.command()
#    @click.argument('name')
#    def hello(name):
#        click.echo('Hello %s!' % name)
#
#    runner = CliRunner()
#    result = runner.invoke(hello, ['Peter'])
#    assert result.exit_code == 0
#    assert result.output == 'Hello Peter!\n'
