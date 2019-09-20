import os
import pandas as pd

from app import util

def test_db_api(mocker):
    mocker.patch('app.util.COMPOSE_PATH', os.path.dirname(__file__))
    status = util.spin_up_db()
    assert status
    engine = util.connect_db()
    file = pd.DataFrame({'firstname':['John','Ada','John'],
                        'lastname':['Smith','Wong','Smith'],
                        'email':['john.smith@gmail.com','a.wong@gmail.com','j.smith@gmail.com']},
                        columns = ['firstname','lastname','email'])
    util.load_file_to_db(file, engine)
    result = util.look_up_from_db('firstname', 'John', engine)
    result_df = pd.DataFrame({'firstname':['John','John'],
                             'lastname':['Smith','Smith'],
                             'email':['john.smith@gmail.com','j.smith@gmail.com']},
                             columns = ['firstname','lastname','email'])
    assert all(result == result_df)
    util.load_file_to_db(file, engine) #load duplicates
    result = util.look_up_from_db('firstname', 'John', engine)
    result_df = pd.DataFrame({'firstname':['John','John'],
                             'lastname':['Smith','Smith'],
                             'email':['john.smith@gmail.com','j.smith@gmail.com']},
                             columns = ['firstname','lastname','email'])
    assert all(result == result_df) #it should still be the same result
    util.delete_db()
