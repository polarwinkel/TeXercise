#!/usr/bin/python3
'''
calculate a mathematical formula with a given value-dict
returns int or float

version 0.4

This might become a TeX-Calculation-library, but maybe handcalcs will
do all jobs I need, so this might also stay as basic as it is.

All it can do for now is:
- apply +, -, *, / operators
- multiplication and division first, then addition and subtraction
- power ^
- brackets () (only round ones yet)
- trigonometric functions \sin or \arctan
- expoential numbers: 1e+12
- \log and e^
- and more by now, see code below!

make sure you always use '*', because 'xy' != 'x*y', in that case xy would be a value!

TODO:
- ~~implement brackets ()~~ done
- implement \frac{}{}
- ~~implement \cdot~~ done
- implement \sqrt{} (works now with round brackets already)
- ~~implement ^~~ done
- ~~implement default value for pi~~ done
- ~~implement e^() and \log()~~ done
'''

import math

def calc(formula, values=''):
    # replace static stuff:
    formula = formula.replace(' ', '')
    formula = formula.replace('\left', '')
    formula = formula.replace('\right', '')
    formula = formula.replace('\pi', '3.141592654')
    formula = formula.replace('\cdot', '*')
    #try:
    return _rekcalc(formula, values)
    #except
    #    return None
    #except ValueError as e:
    #    #raise ValueError('syntax not valid for texCalc')
    #    print(e)
    #    print(formula)
    #    print(values)
    #    return None

def _rekcalc(formula, values=''):
    ''' claculate the formula recursively with the given values '''
    print(formula)
    digits = '0123456789.-'
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
    # power:
    if formula.find(r'^')>=0:
        first = formula[0:formula.find(r'^')]
        if first.endswith('e'):
            # handle e^
            first = first[:-1]+str(math.exp(1))
        part0 = ''
        base = ''
        for i in reversed(range(len(first))):
            if first[i] not in digits:
                part0 = first[:i+1]
                break
            base = first[i]+base
        last = formula[formula.find(r'^')+1:]
        exponent = ''
        part2 = ''
        for i in range(len(last)):
            if last[i] not in digits:
                part2 = last[i:]
                break
            exponent = exponent+last[i]
        formula = part0+str(math.pow(_rekcalc(base),_rekcalc(exponent)))+part2
    # log:
    if formula.find(r'\log')>=0:
        part0 = formula[0:formula.find(r'\log')]
        formula = formula[formula.find(r'\log')+4:]
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.log(_rekcalc(part1)))+part2
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
    # since it's recursive start with addition/subtraction and reverse
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
        else:
            try:
                return int(formula)
            except ValueError:
                return float(formula)
