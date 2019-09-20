#!/usr/bin/env python
from click.testing import CliRunner
import pandas as pd
import unittest.mock as mock
import pytest

from app import util

def test_read_csv_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('fail_example.csv', 'w') as f:
            f.write('it is suppose to fail')

        with pytest.raises(ValueError):
            result = util.read_file('fail_example.csv')

def test_read_csv_too_less():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('fail_example.csv', 'w') as f:
            f.write('firstname,lastname\n'
                    'John,Smith\n'
                    'Ada,Wong\n')

        with pytest.raises(ValueError):
            result = util.read_file('fail_example.csv')

def test_read_csv_too_much(mocker):
    # should be success as it only use the 3 columns that we want
    mocker.patch('app.util.load_file_to_db', autospec=True)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('example.csv', 'w') as f:
            f.write('firstname,lastname,email,age\n'
                    'John,Smith,john.smith@gmail.com,33\n'
                    'Ada,Wong,a.wong@gmail.com,28\n')

        result = util.read_file('example.csv')
        assert result.shape == (2,3)

def test_read_small_csv(mocker):
    mocker.patch('app.util.load_file_to_db', autospec=True)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('example.csv', 'w') as f:
            f.write('firstname,lastname,email\n'
                    'John,Smith,john.smith@gmail.com\n'
                    'Ada,Wong,a.wong@gmail.com\n')

        result = util.read_file('example.csv')
        assert result.shape == (2,3)

def test_read_repeated_csv(mocker):
    mocker.patch('app.util.load_file_to_db', autospec=True)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('example.csv', 'w') as f:
            f.write('firstname,lastname,email\n' +
                    ''.join(['John,Smith,john.smith@gmail.com\n']*10))

        result = util.read_file('example.csv')
        assert result.shape == (1,3)

def test_read_large_csv(mocker):
    mocker.patch('app.util.load_file_to_db', autospec=True)
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('example.csv', 'w') as f:
            f.write('firstname,lastname,email\n' +
                    ''.join([f'John,Smith,john.smith{count}@gmail.com\n' for count in range(10_000_000)]))

        result = util.read_file('example.csv')
        assert result.shape == (10_000_000,3)

def test_search_success(mocker):
    result_df = pd.DataFrame({'firstname':['John','John'],
                              'lastname':['Smith','Smith'],
                              'email':['john.smith@gmail.com','j.smith@gmail.com']},
                              columns = ['firstname','lastname','email'])

    mocker.patch('app.util.look_up_from_db', return_value=result_df)
    result = util.look_up_from_db('firstname','John')
    assert all(result == result_df)
