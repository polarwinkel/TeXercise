#!/usr/bin/python3
'''
API and helper functions for TeXercise 
syntax:
[[type,name,        options]]

data-types:
- b: boolean        correct_value
- n: random number  min, max, step
- s: solution       formula
- t: text           correct_value
'''

import random, ast, json
from math import floor, log10
from modules import latexcalc

def roundSigFig(val):
    ''' round a float to certain significant figures '''
    return round(val, -int(floor(log10(abs(val)/10000))))

def getValues(inp):
    ''' generates values for the input '''
    values = {}
    while True:
        repl = inp.partition('[[')[2].partition(']]')[0] ## stuff to be replaced
        inp = inp.partition(']]')[2]
        repl = repl.split(',')
        if repl[0] == 'f':
            if len(repl)==3: repl.append(1)
            values[str(repl[1])] = roundSigFig(random.uniform(float(repl[2]), float(repl[3])))
        elif repl[0] == 'n':
            if len(repl)==4: repl.append(1)
            values[str(repl[1])] = random.randrange(int(repl[2]), int(repl[3]), int(repl[4]))
        if inp == '': break
    return values

def revise(sheet, edit):
    ''' checks the results '''
    tasks = {}
    result = {}
    values = json.loads(edit['values'])
    for vk in values.keys():
        # use values as int or float
        try:
            values[vk] = int(values[vk])
        except ValueError:
            values[vk] = float(values[vk])
    if edit['content']:
        content = json.loads(edit['content'])
    else:
        content = None
    rest = sheet['content']
    while rest != '':
        # parse/calculate tasks-dict with results from sheet and values
        task = rest.partition('[[')[2].partition(']]')[0] # stuff to be replaced in next task
        rest = rest.partition(']]')[2] # will search for the next task in next iteration
        task = task.split(',')
        if task[0] == '':
            pass
        elif task[0] == 'b': # binary-task
            tasks[task[1]] = {'type': 'b'}
            if task[2] =='true' or task[2]=='1':
                tasks[task[1]]['result'] = True
            else:
                tasks[task[1]]['result'] = False
        elif task[0] == 'f': # float, not a task
            pass
        elif task[0] == 'n': # number, not a task
            pass
        elif task[0] == 's': # solution for calculate-task
            tasks[task[1]] = {'type': 's'}
            try:
                tasks[task[1]]['result'] = latexcalc.calc(task[2], values)
            except:
                tasks[task[1]]['result'] = None
            values[task[1]] = tasks[task[1]]['result']
        elif task[0] == 't': # text-task
            tasks[task[1]] = {'type': 't'}
            tasks[task[1]]['result'] = task[2].lower()
        elif task[0] == 'v': # (calculated) value, not a task
            # TODO: give calculated values a name and add to values?
            #       Or make it a different type to peserve "just show"?
            pass
        else:
            raise ValueError('[ERROR: type not implemented for <code>'+str(task)+'</code>]')
    for name in tasks.keys():
        # revise: compare tasks with edit-content
        if tasks[name]['type'] == 'b':
            result[name] = False
            if tasks[name]['result']:
                if content[name] in ['true', 'on', 'True', True, 1, '1']:
                    result[name] = True
            elif not tasks[name]['result']:
                if content[name] in ['false', 'off', 'False', False, 0, '0']:
                    result[name] = True
        elif tasks[name]['type'] == 's':
            if content:
                try:
                    content[name] = int(content[name])
                except ValueError:
                    try:
                        content[name] = float(str(content[name]).replace(',', '.'))
                    except:
                        content[name] = None
            try:
                res = float(tasks[name]['result'])
                if res == None or res == '':
                    result[name] = None
                elif (res * 0.95 <= content[name]) and (res * 1.05 >= content[name]):
                    # TODO: option for tolerance-percentage
                    result[name] = True
                else:
                    result[name] = False
            except TypeError:
                result[name] = None
        elif tasks[name]['type'] == 't':
            if tasks[name]['result'] == content[name].lower():
                result[name] = True
            else:
                result[name] = False
    return result

def convert(inp, values):
    ''' converts the input to html including form-elements '''
    out = ''
    while True:
        out += inp.partition('[[')[0]
        repl = inp.partition('[[')[2].partition(']]')[0] ## stuff to be replaced
        inp = inp.partition(']]')[2]
        repl = repl.split(',')
        if repl[0] == '':
            pass
        elif repl[0] == 'b':
            out += '<input type="checkbox" id="'+str(repl[1])+'" name="'+str(repl[1])+'" class="formdata" />'
        elif repl[0] == 'f':
            out += str(values[str(repl[1])])
        elif repl[0] == 'n':
            out += str(values[str(repl[1])])
        elif repl[0] == 's':
            out += '<input type="text" id="'+str(repl[1])+'" name="'+str(repl[1])+'" class="formdata" />'
        elif repl[0] == 't':
            out += '<input type="text" id="'+str(repl[1])+'" name="'+str(repl[1])+'" class="formdata" />'
        elif repl[0] == 'v':
            try:
                cvalue = latexcalc.calc(repl[1], values)
            except:
                cvalue = None
            out += str(cvalue)
        else: out += '[ERROR: type not implemented for <code>'+str(repl)+'</code>]'
        if inp == '': break
    return out
