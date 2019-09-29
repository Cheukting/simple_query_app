#!/usr/bin/env python
from click.testing import CliRunner
import pandas as pd

from app import app

def test_init_db_success(mocker):
    mocker.patch('app.app.spin_up_db', autospec=True, return_value=True)
    runner = CliRunner()
    result = runner.invoke(app.init)
    assert app.spin_up_db.call_count == 1
    assert result.exit_code == 0
    assert result.output == 'Initializing database...\nDatabase is running.\n'

def test_init_db_fail(mocker):
    mocker.patch('app.app.spin_up_db', autospec=True, return_value=False)
    runner = CliRunner()
    result = runner.invoke(app.init)
    assert app.spin_up_db.call_count == 1
    assert result.exit_code == 0
    assert result.output == 'Initializing database...\nDatabase cannot be initiated.\n'

def test_stop_db(mocker):
    mocker.patch('app.app.stop_db', autospec=True)
    runner = CliRunner()
    result = runner.invoke(app.stop)
    assert app.stop_db.call_count == 1
    assert result.exit_code == 0
    assert result.output == 'Stopping database...\nDatabase is stopped. Start again by `init`.\n'

def test_delete_db(mocker):
    mocker.patch('app.app.delete_db', autospec=True)
    runner = CliRunner()
    result = runner.invoke(app.stop, ['-d'])
    assert app.delete_db.call_count == 1
    assert result.exit_code == 0
    assert result.output == 'Stopping database...\nDatabase is deleted.\n'

def test_read_csv_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('fail_example.csv', 'w') as f:
            f.write('it is suppose to fail')

        result = runner.invoke(app.load, ['fail_example.csv'])
        assert result.exit_code == 0
        assert result.output == 'Loading data into database...\nAbort. Incorrect file format.\n'

def test_load_csv_success(mocker):
    mocker.patch('app.app.connect_db', autospec=True)
    mocker.patch('app.app.load_file_to_db', autospec=True, return_value=[])
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

def test_load_csv_duplicate(mocker):
    mocker.patch('app.app.connect_db', autospec=True)
    mocker.patch('app.app.load_file_to_db', autospec=True, return_value=[0])
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
        assert result.output.split('\n')[0] == 'Loading data into database...'
        assert result.output.split('\n')[1] == 'The following already exist in database:'
        assert result.output.split('\n')[-2] == '1 row(s) of data loaded.'

def test_search_fail(mocker):
    mocker.patch('app.app.connect_db', autospec=True)
    result_df = None
    mocker.patch('app.app.look_up_from_db', return_value=result_df)
    runner = CliRunner()
    result = runner.invoke(app.search, ['firstname','John'])
    assert app.connect_db.call_count == 1
    assert result.exit_code == 0
    assert result.output.split('\n')[0] == f"Searching for user with 'firstname' as 'John'..."
    assert result.output.split('\n')[1] == 'No matches found.'

def test_search_no_match(mocker):
    mocker.patch('app.app.connect_db', autospec=True)
    result_df = pd.DataFrame()
    mocker.patch('app.app.look_up_from_db', return_value=result_df)
    runner = CliRunner()
    result = runner.invoke(app.search, ['firstname','John'])
    assert app.connect_db.call_count == 1
    assert result.exit_code == 0
    assert result.output.split('\n')[0] == f"Searching for user with 'firstname' as 'John'..."
    assert result.output.split('\n')[1] == 'No matches found.'

def test_search_success(mocker):
    mocker.patch('app.app.connect_db', autospec=True)
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
