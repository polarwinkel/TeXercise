#!/usr/bin/python3
'''
Database-IO-file of TeXercise
'''

import sqlite3
import os

def checkTables(db):
    ''' makes sure default tables exist in the Database '''
    # sheets:
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS sheets (
            id INTEGER NOT NULL PRIMARY KEY,
            iid INTEGER instructor,
            name VARCHAR(256),
            forceLogin BOOLEAN,
            allowEdit BOOLEAN,
            content TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create sheets table')
        err.args = tuple(args)
        raise
    # edits:
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS edits (
            id INTEGER NOT NULL PRIMARY KEY,
            sid INTEGER NOT NULL,
            name VARCHAR(256),
            submitted BOOLEAN,
            setvalues TEXT,
            content TEXT,
            submits INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create edits table')
        err.args = tuple(args)
        raise
    db._connection.commit()
