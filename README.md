# A simple query app with a simple MySQL database that runs on Docker

## Installation

### 1. Cloning the project
First clone this repo form GitHub, assume you have git already:


### 2. Setup virtual environment
If you have your own virtual environment set up it's great. Otherwise, you can use virtualenv.

If you are on Mac OS X or Linux, do the following:
```
$ sudo pip install virtualenv
```
Once you have virtualenv installed, enter the directory of the project and create your own environment.
```
$ cd simple_query_app
$ virtualenv venv
```
Activate it by:
```
$ . venv/bin/activate
```
When you are done and want to go back, you can use the command `$ deactivate` but we will leave it activated for now.

### 3. Install the package
Then you can install the package using the `pip`:
```
$ pip install .
```
make sure you are in the `simple_query_app` directory. If you want to edit the code (e.g. future development), do this instead:
```
$ pip install --editable .
```

## Usage

To start the database:
```
$ simple_query_app init
```

To load a csv file:
```
$ simple_query_app load <file_path>
```
while <file_path> is the path to your file including filename (e.g. example.csv)

Here we use `email` as a unique key (assuming that it is unique amount users), duplicate records with same emails will not be loaded to the database twice.

To search for a user with `firstname`:
```
$ simple_query_app search fristname <name>
```
while <name> is the name for search for, similarly
```
$ simple_query_app search lastname <name>
```
will search for lastname instead.

You can also search using email in similar manner:
```
$ simple_query_app search email <email>
```

After you have done, you may want to shut down the database. There are two ways of doing that. If you want to preserve your data, you can do:
```
$ simple_query_app stop
```

The data will be preserved in your local volume, however, if you want to wipe clean the database, you can do:
```
$ simple_query_app stop -d
```
This will **DELETE** all your data in the Database

## Testing

The application use pytest for testing (including integration test). Just do:
```
$ pytest tests/
```
It will run all the tests.

For separate testing, `test_util.py` and `test_cil.py` will test for the functionality of the app and the command line interface of the app. `test_db.py` will spin up a test container with a separate volume different from production to test the integration of the database.
