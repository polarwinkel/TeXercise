#!/usr/bin/python3
#coding: utf-8
'''
Base file of TeXercise - an auto-correcting Exercise-Server
'''

import os
import sqlite3
from flask import Flask, render_template, request, send_from_directory, make_response, jsonify
from flask import url_for, redirect
import flask_login
import json
from jinja2 import Template
from multiprocessing import Process
import mdtex2html

from modules import dbio, texerciseIo, settingsIo, normalizeString

# global settings:

dbfile = 'TeXercise.sqlite3'
settingsfile = 'TeXercise.conf'
settings = settingsIo.settingsIo(settingsfile)
host = settings.get('host')
debug = settings.get('debug')
extensions = settings.get('extensions')

# WebServer stuff:

app = Flask(__name__)

# login-stuff

app.secret_key = settings.get('secret_key')
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    #if username not in users:
    if username != settings.get('admin'):
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    #if username not in users:
    if username != settings.get('admin'):
        return
    user = User()
    user.id = username
    user.is_authenticated = settings.checkPw(request.form['password'])
    return user

# routes

@app.route('/', methods=['GET'])
def index():
    '''show index-page'''
    #if flask_login.current_user.is_anonymous:
    #    return render_template('login.html', relroot='./')
    if settings.get('admin') == '':
        return redirect('_init')
    return render_template('index.html', relroot='./')

@app.route('/_init', methods=['GET', 'POST'])
def init():
    if settings.get('admin') == '':
        if request.method == 'GET':
            return render_template('init.html', relroot='./')
        username = request.form['username']
        password = request.form['password']
        if username != '' and password != '':
            settings.set('admin', username)
            settings.set('password', password)
            return redirect('_login')
        return 'ERROR: Username and/or password was not set!'
    else:
        return 'TeXercise is already initialized!'

@app.route('/_login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.current_user.is_anonymous:
            return render_template('login.html', relroot='./')
        return redirect('_instructor')
    username = request.form['username']
    if username == settings.get('admin'):
        if settings.checkPw(request.form['password']):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect('_instructor')
    return 'Bad login'

@app.route('/_logout')
def logout():
    flask_login.logout_user()
    return redirect('./')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/_static/<filename>', methods=['GET'])
def sendStatic(filename):
    '''send static files like css or js'''
    return send_from_directory('static', filename)

@app.route('/_createSheet/', methods=['GET'])
@flask_login.login_required
def createSheet():
    '''show create-sheet page'''
    return render_template('putSheet.html', relroot='../', sid='', name='', content='')

@app.route('/_editSheet/<sheetn>', methods=['GET'])
@flask_login.login_required
def editSheet(sheetn):
    '''show edit-sheet page'''
    db = dbio.TtDb(dbfile)
    sheet = db.getSheet(sheetn)
    return render_template('putSheet.html', relroot='../', sid=sheet['id'],
            name=sheet['name'], allowEdit=sheet['allowEdit'], content=sheet['content'])

@app.route('/_putSheet/<sheetn>', methods=['PUT'])
@flask_login.login_required
def putSheet(sheetn):
    '''save a new or edited sheet'''
    db = dbio.TtDb(dbfile)
    result = db.putSheet(request.json)
    return str(result)

@app.route('/_putEditName/', methods=['PUT'])
def putEditName():
    '''set name for a sheet, creating a new entry if not set before for the sheet, and return the sheet as json'''
    db = dbio.TtDb(dbfile)
    sheetn = request.json['sheetn']
    sheet = db.getSheet(sheetn)
    name = normalizeString.normalize(request.json['name'])
    edit = db.getEditName(sheetn, name)
    if not edit:
        values = texerciseIo.getValues(sheet['content'])
        eid = db.createEditName(sheet, name, values)
    return name

@app.route('/<sheetn>', methods=['GET'])
def sheet(sheetn):
    '''show sheet-page'''
    db = dbio.TtDb(dbfile)
    sheet = db.getSheet(sheetn)
    if sheet is not None:
        return render_template('sheet.html', relroot='./', sheetn=sheet['name'], allowEdit=sheet['allowEdit'], name='')
    else:
        return 'Sheet not found!'

@app.route('/<path:path>', methods=['GET'])
def sheetUser(path):
    '''show sheet-page for sheet/user'''
    db = dbio.TtDb(dbfile)
    sheetn = path.partition('/')[0]
    name = path.partition('/')[2]
    try:
        sheet = db.getSheet(sheetn)
        edit = db.getEditName(sheetn, name)
    except Exception as e:
        return render_template('404.html'), 404
    return render_template('sheet.html', relroot='../', sheetn=sheet['name'], allowEdit=sheet['allowEdit'], name=name)
@app.route('/_loadSheetUser/<path:path>', methods=['PUT'])
def loadSheetUser(path):
    '''load a sheet-json for sheet/user'''
    db = dbio.TtDb(dbfile)
    result = {}
    sheetn = request.json['sheetn']
    sheet = db.getSheet(sheetn)
    name = request.json['name']
    #name = normalizeString.normalize(request.json['name'])
    edit = db.getEditName(sheetn, name)
    if not edit:
        values = texerciseIo.getValues(sheet['content'])
        eid = db.createEditName(sheet, name, values)
    else:
        values = json.loads(edit['values'])
        eid = edit['id']
        result['content'] = edit['content']
    mdhtml = mdtex2html.convert(sheet['content'], extensions)
    result['sheetcontent'] = texerciseIo.convert(mdhtml, values)
    result['eid'] = eid
    return result
    # TODO: return results if already edited?

@app.route('/_postEdit/<eid>', methods=['POST'])
def postEdit(eid):
    '''post an individual edit for a sheet'''
    db = dbio.TtDb(dbfile)
    result = db.postEdit(eid, json.dumps(request.json))
    return str(result)

@app.route('/_getRevision/', methods=['PUT'])
def getRevision():
    '''just get the revision without posting a new edit'''
    db = dbio.TtDb(dbfile)
    req = request.json
    sheet = db.getSheet(req['sheetn'])
    eid = db.getEdit(req['eid'])
    revision = texerciseIo.revise(sheet, eid)
    return json.dumps(revision)

@app.route('/_results/<sheet>', methods=['GET'])
@flask_login.login_required
def results(sheet):
    '''show results of all sheet-edits'''
    db = dbio.TtDb(dbfile)
    sheet = db.getSheet(sheet)
    edits = db.getEdits(sheet['id'])
    resultlist = '<table><tr><th>Name</th><th>right</th><th>wrong</th><th>submits</th><th>timestamp</th><th>delete</th></tr>\n'
    for edit in edits:
        values = json.loads(edit['values'])
        if edit['content'] is not None:
            content = json.loads(edit['content'])
            right = 0
            wrong = 0
            revision = texerciseIo.revise(sheet, edit)
            for v in revision.values():
                if v[0]:
                    right += 1
                elif v[0] == False:
                    wrong += 1
        else:
            right = '-'
            wrong = '-'
        resultlist += '<tr><td><a href="../'+sheet['name']+'/'+edit['name']+'">'+edit['name']+'</a></td>'
        resultlist += '<td>'+str(right)+'</td>'
        resultlist += '<td>'+str(wrong)+'</td>'
        resultlist += '<td>'+str(edit['submits'])+'</td>'
        resultlist += '<td>'+str(edit['timestamp'])+'</td>'
        resultlist += '<td><a onclick="pa.boolean(\'Really delete this edit?\', \'../_deleteEdit/'+str(sheet['id'])+'/'+str(edit['id'])+'\')">delete</a></td></tr>\n'
    resultlist += '</table>\n'
    return render_template('results.html', relroot='../', sheet=sheet['name'], resultlist=resultlist)

@app.route('/_instructor', methods=['GET'])
@flask_login.login_required
def instructor():
    '''show instructor-page'''
    db = dbio.TtDb(dbfile)
    sheetList = db.getSheetList()
    return render_template('instructor.html', relroot='./', sheetList=sheetList, authuser=flask_login.current_user.id)

@app.route('/_deleteEdit/<sid>/<eid>', methods=['DELETE'])
@flask_login.login_required
def deleteEdit(sid, eid):
    '''delete an edit'''
    db = dbio.TtDb(dbfile)
    db.deleteEdits(sid, eid)
    return 'ok'

@app.route('/_deleteSheet/<sid>', methods=['DELETE'])
@flask_login.login_required
def deleteSheet(sid):
    '''delete a sheet with all edits'''
    db = dbio.TtDb(dbfile)
    db.deleteSheet(sid)
    return 'ok'

# run it:

if __name__ == '__main__':
    app.run(host=host, debug=debug)
