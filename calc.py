#!/usr/bin/env python3
import csv
import os
import re
import sys
import click
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

rootd, app, db = '', None, None

def init_globals():
    global rootd, app, db
    rootd = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = '{}/sqlite.db'
    db = SQLAlchemy(app)
    logger = logging.getLoggerClass()


def parse_csv(csv_path: str):
    total_pos = 0.0
    total_neg = 0.0

    with open(csv_path, 'r') as f:
        all_rows = csv.reader(f)
        all_rows = list([a for a in all_rows])

        for cell_row_i in range(len(all_rows)):
            #cur_row = [r for r in all_rows[cell_row_i]]
            cur_row = [c for c in all_rows[cell_row_i]]
            print(cur_row)
            if len(cur_row) == 0 or cur_row[0] in ['Date','Postdate']:
                continue

            try:
                parse_type = 'me'
                pfloat = float(list(cur_row[::-1])[0])
            except:
                parse_type = 'mom'
                pfloat = float(list(cur_row)[::-1][1])

            print(parse_type, pfloat)
            if pfloat >= 0:
                total_pos += pfloat
            else:
                total_neg += pfloat

    logger.info('Positive: {:.2f} | Negative: {:.2f} | Total: {:.2f}'.format(total_pos, total_neg, total_pos + total_neg))
    return all_rows

def global_imports():
    global rootd, app, db
    gimports = ['rootd', 'app', 'db', 'fname']

@click.command()
@click.option('fname', default=['me.csv'], help='names of files to "proccess"',
            type=str, multiple=True, nargs=-1)
def main():
    global rootd, app, db = init_globals()
    print('New main test: {filenames}')
    parse_csv(csv_path=rootd + '/' + str(sys.argv[1]))

if __name__ == '__main__':
    main()