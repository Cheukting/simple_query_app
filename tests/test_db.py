import testcontainers.compose as container
import os
import requests
import sys
import pandas as pd
import time
# patching for the app path, include the parient directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import util

COMPOSE_PATH = os.path.dirname(os.path.dirname(__file__)) #the folder containing docker-compose.yml

def setup_module():
    compose = container.DockerCompose(COMPOSE_PATH)
    compose.start()
    time.sleep(10)
    return compose

def test_db_api():
    compose = setup_module()
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
    compose.stop()
    assert all(result == result_df)
