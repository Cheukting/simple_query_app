#!/usr/bin/env python

import click
from .util import *

@click.group()
def cli():
    pass

@cli.command()
@click.argument('file_name')
def load(file_name):
    click.echo('Loading data into database...')
    try:
        file = read_file(file_name)
    except:
        click.echo('Abort. Incorrect file format.')
        return None
    engine= connect_db()
    load_file_to_db(file, engine)
    click.echo(f'{file.shape[0]} row(s) of data loaded.')

@cli.command()
@click.argument('key')
@click.argument('value')
def search(key,value):
    click.echo(f"Searching for user with '{key}' as '{value}'...")
    engine = connect_db()
    result = look_up_from_db(key, value, engine)
    if result is None or result.shape[0] == 0:
        click.echo('No matches found.')
    else:
        click.echo(f'{result.shape[0]} matche(s) found:')
        click.echo(result)

if __name__ == '__main__':
    cli()
