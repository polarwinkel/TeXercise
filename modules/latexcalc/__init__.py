#!/usr/bin/python3
'''
LaTeXcalc is a LaTeX-Calculation-library for python3.

Licenced under GPLv3 or newer
(c) 2022-2023 by Dirk Winkel
version 0.8.1

This calculates a mathematical formula written as a LaTeX-string.
It will use with a given value-dict for variables in the formula.
The return-value is int (if possible) or float if it succeeds, 
if there is an error it will return a string.

Supported features:
- apply +, -, *, / operators
- multiplication and division first, then addition and subtraction
- power ^
- brackets (), [] and {} (also with \left(..\right))
- squareroot \sqrt
- trigonometric functions \sin or \arctan (radiant)
- exponential numbers: 1e+12
- \log (base 10), \ln (natural log) and e^
- \pi or pi and e as default-values math.pi and math.e
- \frac{}{} (works as '\frac 1 2' as well)

make sure you always use '*' (or '\cdot'), because 'xy' != 'x*y', in that case xy would be a value!

All testet cases work, but there might still be wrong calculations in 
special cases, so test it for your needs!
'''

import math

debug = False

def _frac(formula, values):
    ''' dissolve fractions to divisions '''
    part0 = formula[0:formula.find(r'\frac')]
    # fix the weired fact, that 2 1/2=2+1/2 while a b/c=a*b/c:
    part0 = part0.replace(' ', '')
    if part0[-1:].isnumeric():
        part0 = part0+'+'
    #elif part0[-1:] and part0[-1:] not in ['+','-','*','/']:
    #    part0 = part0+'*'
    formula = formula[formula.find(r'\frac')+5:]
    # abbreviated form with whitespace:
    if formula.startswith(' '):
        formula = formula.split(' ',3)
        numerator = formula[1]
        denominator = formula[2]
        if len(formula)>=4:
            formula = '*'+formula[3]
        else:
            formula = ''
    # normal form: \frac{}{}:
    elif formula.startswith('{'):
        depth=1
        numerator = ''
        formula=formula[1:]
        while len(formula)>0:
            if formula.startswith('{'):
                depth=depth+1
            elif formula.startswith('}'):
                depth=depth-1
            if depth==0:
                formula=formula[1:]
                break
            else:
                numerator=numerator+formula[0]
                formula=formula[1:]
        depth=1
        formula=formula[1:]
        denominator = ''
        while len(formula)>0:
            if formula.startswith('{'):
                depth=depth+1
            elif formula.startswith('}'):
                depth=depth-1
            if depth==0:
                formula=formula[1:]
                break
            else:
                denominator=denominator+formula[0]
                formula=formula[1:]
    return _rekcalc(part0+'('+numerator+')/('+denominator+')'+formula, values)

def _brackets(formula, values, bra):
    ''' dissolve brackets '''
    part0 = formula[0:formula.find(bra[0])]
    formula = formula[formula.find(bra[0])+1:]
    depth=1
    part1 = ''
    while len(formula)>0:
        if formula.startswith(bra[0]):
            depth=depth+1
        elif formula.startswith(bra[1]):
            depth=depth-1
        if depth==0:
            formula=formula[1:]
            break
        else:
            part1=part1+formula[0]
            formula=formula[1:]
    return part0+str(_rekcalc(part1, values))+formula

def _sqrt(formula, values):
    ''' calculate sqareroot '''
    digits = '0123456789.-'
    part0 = formula[0:formula.find(r'\sqrt')]
    formula = formula[formula.find(r'\sqrt')+5:]
    part1 = ''
    part2 = ''
    for i in range(len(formula)):
        if formula[i] not in digits:
            part2 = formula[i:]
            break
        part1 = part1+formula[i]
    return part0+str(math.sqrt(_rekcalc(part1)))+part2

def _pow(formula, values):
    ''' calculate power '''
    digits = '0123456789.'
    first = formula[0:formula.find(r'^')]
    part0 = ''
    base = ''
    for i in reversed(range(len(first))):
        if (first[i] not in digits+'-') and (not first[i].isalpha()):
            part0 = first[:i+1]
            break
        base = first[i]+base
    last = formula[formula.find(r'^')+1:]
    exponent = last[0]
    last = last[1:] # first one has to be part of exponent, after that '-' is not allowed anymore
    part2 = ''
    for i in range(len(last)):
        if (last[i] not in digits) and (not last[i].isalpha()):
            part2 = last[i:]
            break
        exponent = exponent+last[i]
    return part0+str(math.pow(_rekcalc(base, values),_rekcalc(exponent, values)))+part2

def _log(formula, values, log):
    ''' calculate logarithms '''
    # does not (yet) support different bases than e ('\ln') or 10 ('\log')
    digits = '0123456789.-'
    part0 = formula[0:formula.find(log)]
    if log == r'\ln':
        formula = formula[formula.find(log)+3:]
    else:
        formula = formula[formula.find(log)+4:]
    part1 = ''
    part2 = ''
    for i in range(len(formula)):
        if (formula[i] not in digits) and (not formula[i].isalpha()):
            part2 = formula[i:]
            break
        part1 = part1+formula[i]
    if log == r'\ln':
        return part0+str(math.log(_rekcalc(part1, values)))+part2
    if log == r'\log':
        return part0+str(math.log10(_rekcalc(part1, values)))+part2

def _trig(formula, values, trig):
    ''' calculate trigonomic functions '''
    # radiant only, because there is no native degree-symbol (I use '^\circ')
    digits = '0123456789.-'
    part0 = formula[0:formula.find(trig)]
    if trig in [r'\arcsin',r'\arccos',r'\arctan']:
        formula = formula[formula.find(trig)+7:]
    else:
        formula = formula[formula.find(trig)+4:]
    part1 = ''
    part2 = ''
    for i in range(len(formula)):
        if (formula[i] not in digits) and (not formula[i].isalpha()):
            part2 = formula[i:]
            break
        part1 = part1+formula[i]
    if trig == r'\sin':
        return part0+str(math.sin(_rekcalc(part1)))+part2
    elif trig == r'\cos':
        return part0+str(math.cos(_rekcalc(part1)))+part2
    elif trig == r'\tan':
        return part0+str(math.tan(_rekcalc(part1)))+part2
    elif trig == r'\arcsin':
        return part0+str(math.asin(_rekcalc(part1)))+part2
    elif trig == r'\arccos':
        return part0+str(math.acos(_rekcalc(part1)))+part2
    elif trig == r'\arctan':
        return part0+str(math.atan(_rekcalc(part1)))+part2

def _rekcalc(formula, values={}):
    ''' claculate the formula recursively with the given values '''
    # \frac: (replace first because {}-braces are special here)
    while formula.find(r'\frac')>=0:
        formula = str(_frac(formula, values))
    formula = formula.replace(' ', '') # might have been {}-replacement in \frac before
    # brackets:
    brackets = [['{','}'],['\{','\}'],['[',']'],['(',')']]
    for bra in brackets:
        # preserve value-indices
        if bra[0]=='{' and formula.find(bra[0])>0:
            if formula[formula.find(bra[0])-1] == '_':
                continue
        while formula.find(bra[0])>=0:
            formula = _brackets(formula, values, bra)
    
    # sqrt:
    while formula.find(r'\sqrt')>=0:
        formula = _sqrt(formula, values)
    # power:
    while formula.find(r'^')>=0:
        formula = _pow(formula, values)
    # log:
    while formula.find(r'\ln')>=0:
        formula = _log(formula, values, r'\ln')
    while formula.find(r'\log')>=0:
        formula = _log(formula, values, r'\log')
    
    # trigonometry:
    while formula.find(r'\sin')>=0:
        formula = _trig(formula, values, r'\sin')
    while formula.find(r'\cos')>=0:
        formula = _trig(formula, values, r'\cos')
    while formula.find(r'\tan')>=0:
        formula = _trig(formula, values, r'\tan')
    while formula.find(r'\arcsin')>=0:
        formula = _trig(formula, values, r'\arcsin')
    while formula.find(r'\arccos')>=0:
        formula = _trig(formula, values, r'\arccos')
    while formula.find(r'\arctan')>=0:
        formula = _trig(formula, values, r'\arctan')
    
    # arithmetic operations:
    # since it's recursive start with addition/subtraction
    if (formula.rpartition('+')[0] != '') and (formula.rpartition('+')[0][-1:] != 'e'): # e like '2e+12'
        a = formula.rpartition('+')[0]
        b = formula.rpartition('+')[2]
        return _rekcalc(a, values)+_rekcalc(b, values)
    elif (formula.rpartition('-')[0] != '') and (formula.rpartition('-')[0][-1:] not in ['+','-','*','/','e']):
        # (if '-' follows an operator it is the algebraic sign)
        a = formula.rpartition('-')[0]
        b = formula.rpartition('-')[2]
        return _rekcalc(a, values)-_rekcalc(b, values)
    elif formula.rpartition('*')[0] != '':
        a = formula.rpartition('*')[0]
        b = formula.rpartition('*')[2]
        return _rekcalc(a, values)*_rekcalc(b, values)
    elif formula.rpartition('/')[0] != '':
        a = formula.rpartition('/')[0]
        b = formula.rpartition('/')[2]
        return _rekcalc(a, values)/_rekcalc(b, values)
    else:
        # there are no more arithmetic operators left
        # replace values:
        if formula in values:
            return values[formula]
        # replace mathematical constants if not overridden in values:
        elif formula == 'e':
            return math.e
        elif formula == '\pi' or formula == 'pi':
            return math.pi
        else:
            try:
                return int(formula)
            except ValueError:
                return float(formula)
            except:
                raise

def calc(formula, values={}):
    # replace static stuff:
    formula = formula.replace('\left', '')
    formula = formula.replace('\right', '')
    formula = formula.replace('\cdot', '*')
    formula = formula.strip()
    result = _rekcalc(formula, values)
    return result
    try:
        return result
    except ValueError as e:
        return 'ERROR in LaTeXcalc: Missing Value? Message: '+e
    except e:
        if debug:
            print(e)
            print('formula: '+str(formula))
            print('values : '+str(values))
            raise
        else:
            return 'ERROR in LaTeXcalc: Error in formula? Message: '+e
