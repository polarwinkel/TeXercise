#!/usr/bin/python3
'''
Database-IO-file of TeXercise
'''

import sqlite3, json
import os
from modules import dbInit
from datetime import datetime
from modules import normalizeString

class TtDb:
    ''' Database-Connection to the TeXercise-Database '''
    def __init__(self, dbfile):
        if not os.path.exists(dbfile):
            connection = sqlite3.connect(dbfile)
            cursor = connection.cursor()
            # activate support for foreign keys in SQLite:
            sql_command = 'PRAGMA foreign_keys = ON;'
            cursor.execute(sql_command)
            connection.commit()
            connection.close()
        self._connection = sqlite3.connect(dbfile) # _x = potected, __ would be private
        dbInit.checkTables(self)
    
    def reloadDb(self, dbfile):
        '''reloads the database file, i.e. after external changes/sync'''
        self._connection.commit() # not necessary, just to be sure
        self._connection.close()
        self._connection = sqlite3.connect(dbfile)
    
    def getSheetName(self, sid):
        '''returns a sheed-name for an id'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT name FROM sheets WHERE id=?'''
        cursor.execute(sqlTemplate, (sid, ))
        sid = cursor.fetchone()[0]
        self._connection.commit()
        if sid is None:
            return -1
        else:
            return sid
    
    def getSheetId(self, name):
        '''checks if a name is taken already for a sheet and returns the id or -1'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM sheets WHERE name=?'''
        cursor.execute(sqlTemplate, (name, ))
        sid = cursor.fetchone()[0]
        self._connection.commit()
        if sid is None:
            return -1
        else:
            return sid
    
    def getEditName(self, sheetn, name):
        ''' check if a username has an edit for a sheet already and returns it '''
        sid = self.getSheetId(sheetn)
        if sid == -1: raise ValueError('ERROR: sheet not found')
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, submitted, setvalues, content, timestamp
                FROM edits WHERE sid=? AND name=?'''
        cursor.execute(sqlTemplate, (sid, name))
        e = cursor.fetchone()
        self._connection.commit()
        if e is None:
            return False
        else:
            result = {
                    'id'        : e[0],
                    'submitted' : e[1],
                    'values'    : e[2],
                    'content'   : e[3],
                    'timestamp' : e[4]
                }
            return result
    
    def getEdit(self, eid):
        ''' returns an edit from an edit-id '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, sid, submitted, setvalues, content, timestamp
                FROM edits WHERE id=?'''
        cursor.execute(sqlTemplate, (eid, ))
        e = cursor.fetchone()
        self._connection.commit()
        if e is None:
            return False
        else:
            result = {
                    'id'        : e[0],
                    'sid'       : e[1],
                    'submitted' : e[2],
                    'values'    : e[3],
                    'content'   : e[4],
                    'timestamp' : e[5]
                }
            return result
    
    def createEditName(self, sheet, name, values):
        ''' set an edit-Username for a sheet, creating an edit with new values if not yet existing '''
        if not self.getEditName(sheet['name'], name):
            cursor = self._connection.cursor()
            sqlTemplate = '''INSERT INTO edits (sid, name, setvalues, submits)
                    VALUES (?, ?, ?, ?);'''
            cursor.execute(sqlTemplate, (sheet['id'], name, json.dumps(values), 0))
            sqlTemplate = '''SELECT id FROM edits WHERE sid=? AND name=?'''
            cursor.execute(sqlTemplate, (sheet['id'], name))
            eid = cursor.fetchone()[0]
            self._connection.commit()
            return eid;
        else:
            raise ValueError('ERRPR: edit exists for that user and sheet!')
    
    def postEdit(self, eid, edit):
        ''' writes a submitted edit to the database, incementing counter '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT submits FROM edits WHERE id=?'''
        cursor.execute(sqlTemplate, (eid, ))
        n = cursor.fetchone()[0]+1
        self._connection.commit()
        sqlTemplate = '''UPDATE edits SET submitted=true, content=?, submits=?
                WHERE id=?'''
        valuelist = (edit, n, eid)
        cursor.execute(sqlTemplate, valuelist)
        self._connection.commit()
        return 'Commit successful!';
    
    def putSheet(self, sheet):
        ''' edits or inserts a sheet, received as dictionary, into the database '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id FROM sheets WHERE name=?'''
        cursor.execute(sqlTemplate, (sheet['name'], ))
        sheetName = normalizeString.normalize(sheet['name'])
        if sheet['sid'] != '':
            # update sheet:
            sqlTemplate = '''UPDATE sheets
                    SET name=?, forceLogin=?, allowEdit=?, content=? 
                    WHERE id=?;'''
            valuelist = (sheetName,
                        sheet['forceLogin'],
                        sheet['allowEdit'],
                        sheet['content'],
                        sheet['sid']
                    )
        else:
            # new sheet:
            if cursor.fetchone():
                return 'ERROR: Name exists already. Choose a different one!'
            sqlTemplate = '''INSERT INTO sheets 
                    (name, forceLogin, allowEdit, content) 
                    VALUES (?, ?, ?, ?);'''
            valuelist = (normalizeString.normalize(sheetName),
                        sheet['forceLogin'],
                        sheet['allowEdit'],
                        sheet['content']
                    )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        sid = self.getSheetId(sheetName)
        if sid >= 0:
            return 'Success: Created as <a href="../_editSheet/'+sheetName+'">'+sheetName+'</a>!'
        else:
            return 'ERROR 500: Unknown server error after entering into database'
    
    def getSheet(self, name):
        '''returns the sheet to a given name'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, name, forceLogin, allowEdit, content FROM sheets WHERE name=?'''
        cursor.execute(sqlTemplate, (name, ))
        s = cursor.fetchone()
        self._connection.commit()
        if s is None:
            return None
        result = {
                    'id'        : s[0],
                    'name'      : s[1],
                    'forceLogin': s[2],
                    'allowEdit' : s[3],
                    'content'   : s[4]
                }
        return result
    
    def getSheetList(self):
        '''returns a List of all sheets'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, iid, name, forceLogin, allowEdit, timestamp FROM sheets ORDER BY timestamp DESC'''
        cursor.execute(sqlTemplate)
        tup = cursor.fetchall()
        self._connection.commit()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'iid'       : t[1],
                        'name'      : t[2],
                        'forceLogin': t[3],
                        'allowEdit' : t[4],
                        'timestamp' : t[5]
                    })
        return result
    
    def getEdits(self, sheet):
        '''returns a List of all edits for a sheet'''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, name, submitted, setvalues, content, submits, timestamp FROM edits WHERE sid=?'''
        cursor.execute(sqlTemplate, (sheet, ))
        tup = cursor.fetchall()
        self._connection.commit()
        if tup is None:
            return None
        result = []
        for t in tup:
            result.append({
                        'id'        : t[0],
                        'name'      : t[1],
                        'submitted' : t[2],
                        'values'    : t[3],
                        'content'   : t[4],
                        'submits'    : t[5],
                        'timestamp' : t[6]
                    })
        return result
