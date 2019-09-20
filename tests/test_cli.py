#!/usr/bin/env python
import click
from click.testing import CliRunner
import unittest.mock as mock
import pandas as pd

import sys
import os
# patching for the app path, include the parient directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

class MockConn:
    def close(self):
        pass

def test_read_csv_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('fail_example.csv', 'w') as f:
            f.write('it is suppose to fail')

        result = runner.invoke(app.load, ['fail_example.csv'])
        assert result.exit_code == 0
        assert result.output == 'Loading data into database...\nAbort. Incorrect file format.\n'

def test_read_csv_success(mocker):
    mocker.patch('app.app.connect_db', autospec=True, return_value=MockConn())
    mocker.patch('app.app.load_file_to_db', autospec=True)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('success_example.csv', 'w') as f:
            f.write('firstname,lastname,email\n'
                    'John,Smith,john.smith@gmail.com\n'
                    'Ada,Wong,a.wong@gmail.com\n')

        result = runner.invoke(app.load, ['success_example.csv'])
        assert app.connect_db.call_count == 1
        assert app.load_file_to_db.call_count == 1
        assert result.exit_code == 0
        assert result.output == 'Loading data into database...\n2 row(s) of data loaded.\n'

def test_search_no_match(mocker):
    mocker.patch('app.app.connect_db', autospec=True, return_value=MockConn())
    result_df = pd.DataFrame()
    mocker.patch('app.app.look_up_from_db', return_value=result_df)
    runner = CliRunner()
    result = runner.invoke(app.search, ['firstname','John'])
    assert app.connect_db.call_count == 1
    assert result.exit_code == 0
    assert result.output.split('\n')[0] == f"Searching for user with 'firstname' as 'John'..."
    assert result.output.split('\n')[1] == 'No matches found.'

def test_search_success(mocker):
    mocker.patch('app.app.connect_db', autospec=True, return_value=MockConn())
    result_df = pd.DataFrame({'firstname':['John','John'],
                              'lastname':['Smith','Smith'],
                              'email':['john.smith@gmail.com','j.smith@gmail.com']},
                              columns = ['firstname','lastname','email'])
    mocker.patch('app.app.look_up_from_db', return_value=result_df)
    runner = CliRunner()
    result = runner.invoke(app.search, ['firstname','John'])
    assert app.connect_db.call_count == 1
    assert result.exit_code == 0
    assert result.output.split('\n')[0] == f"Searching for user with 'firstname' as 'John'..."
    assert result.output.split('\n')[1] == '2 matche(s) found:'
