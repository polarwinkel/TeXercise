#!/usr/bin/python3
'''
calculate a mathematical formula with a given value-dict
returns int or float

version 0.2

This might become a TeX-Calculation-library, but maybe handcalcs will
do all jobs I need, so this might also stay as basic as it is.

All it can do for now is:
- apply +, -, *, / operators
- multiplication and division first, then addition and subtraction
- trigonometric functions

make sure you always use *, xy != x*y , in that case xy would be a value!

TODO:
- ~~implement brackets ()~~ done
- implement \frac{}{}
- implement \cdot
- ~~implement \sqrt{}~~ (works now with round brackets)
- implement ^
- implement default values for pi and e that the user can override
'''

import math

def calc(formula, values=''):
    #try:
    return _rekcalc(formula, values)
    #except ValueError as e:
    #    #raise ValueError('syntax not valid for texCalc')
    #    print(e)
    #    print(formula)
    #    print(values)
    #    return None

def _rekcalc(formula, values=''):
    ''' claculate the formula recursively with the given values '''
    digits = '0123456789.'
    # brackets:
    if formula.find('(')>=0:
        part0 = formula[0:formula.find('(')]
        formula = formula[formula.find('(')+1:]
        depth=1
        part1 = ''
        while len(formula)>0:
            if formula.startswith('('):
                depth=depth+1
            elif formula.startswith(')'):
                depth=depth-1
            if depth==0:
                formula=formula[1:]
                break
            else:
                part1=part1+formula[0]
                formula=formula[1:]
        formula = part0+str(_rekcalc(part1, values))+formula
        formula = str(_rekcalc(formula, values)) #resolve remaining brackets
    # sqrt:
    if formula.find(r'\sqrt')>=0:
        part0 = formula[0:formula.find(r'\sqrt')]
        formula = formula[formula.find(r'\sqrt')+5:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.sqrt(_rekcalc(part1)))+part2
    # trigonometry:
    if formula.find(r'\sin')>=0:
        part0 = formula[0:formula.find(r'\sin')]
        formula = formula[formula.find(r'\sin')+4:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.sin(_rekcalc(part1)))+part2
    if formula.find(r'\cos')>=0:
        part0 = formula[0:formula.find(r'\cos')]
        formula = formula[formula.find(r'\cos')+4:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.cos(_rekcalc(part1)))+part2
    if formula.find(r'\tan')>=0:
        part0 = formula[0:formula.find(r'\tan')]
        formula = formula[formula.find(r'\tan')+4:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.tan(_rekcalc(part1)))+part2
    if formula.find(r'\arcsin')>=0:
        part0 = formula[0:formula.find(r'\arcsin')]
        formula = formula[formula.find(r'\arcsin')+7:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.asin(_rekcalc(part1)))+part2
    if formula.find(r'\arccos')>=0:
        part0 = formula[0:formula.find(r'\arccos')]
        formula = formula[formula.find(r'\arccos')+7:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.acos(_rekcalc(part1)))+part2
    if formula.find(r'\arctan')>=0:
        part0 = formula[0:formula.find(r'\arctan')]
        formula = formula[formula.find(r'\arctan')+7:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.atan(_rekcalc(part1)))+part2
    # arithmetic operations:
    if formula.partition('*')[2] != '':
        a = formula.partition('*')[0]
        b = formula.partition('*')[2]
        return _rekcalc(a, values)*_rekcalc(b, values)
    elif formula.partition('/')[2] != '':
        # TODO: this gives wrong results for '1/1/10' because the last part will be calculated first!!!
        a = formula.partition('/')[0]
        b = formula.partition('/')[2]
        return _rekcalc(a, values)/_rekcalc(b, values)
    elif formula.partition('+')[2] != '':
        a = formula.partition('+')[0]
        b = formula.partition('+')[2]
        return _rekcalc(a, values)+_rekcalc(b, values)
    elif formula.partition('-')[2] != '':
        # TODO: this causes errors with negative numbers!!!
        a = formula.partition('-')[0]
        b = formula.partition('-')[2]
        return _rekcalc(a, values)-_rekcalc(b, values)
    else:
        # there are no more arithmetic operators left
        # replace values:
        if formula in values:
            return values[formula]
        else:
            try:
                return int(formula)
            except ValueError:
                return float(formula)
