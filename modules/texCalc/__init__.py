#!/usr/bin/python3
'''
calculate a mathematical formula with a given value-dict

This might become a TeX-Calculation-library, but maybe handcalcs will
do all jobs I need, so this might also stay as basic as it is.

All it can do for now is:
- apply +, -, *, / operators
- multiplication and division first, then addition and subtraction

make sure you always use *, xy != x*y , in that case xy would be a value!

TODO:
- ~~implement brackets ()~~ done
- implement \frac{}{}
- implement \cdot
- implement \sqrt{} (works now with round brackets)
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
    # brackets:
    if formula.find('(')>=0:
        part0 = formula[0:formula.find('(')]
        formula = formula[formula.find('(')+1:]
        n=1
        part1 = ''
        while len(formula)>0:
            if formula.startswith('('):
                n=n+1
            elif formula.startswith(')'):
                n=n-1
            if n==0:
                formula=formula[1:]
                break
            else:
                part1=part1+formula[0]
                formula=formula[1:]
        formula = part0+str(_rekcalc(part1, values))+formula
    # sqrt:
    if formula.find('\sqrt')>=0:
        part0 = formula[0:formula.find('\sqrt')]
        formula = formula[formula.find('\sqrt')+5:]
        digits = '0123456789.'
        part1 = ''
        part2 = ''
        for i in range(len(formula)):
            if formula[i] not in digits:
                part2 = formula[i:]
                break
            part1 = part1+formula[i]
        formula = part0+str(math.sqrt(_rekcalc(part1)))+part2
    # arithmetic operations:
    if formula.partition('*')[2] != '':
        a = formula.partition('*')[0]
        b = formula.partition('*')[2]
        return _rekcalc(a, values)*_rekcalc(b, values)
    elif formula.partition('/')[2] != '':
        a = formula.partition('/')[0]
        b = formula.partition('/')[2]
        return _rekcalc(a, values)/_rekcalc(b, values)
    elif formula.partition('+')[2] != '':
        a = formula.partition('+')[0]
        b = formula.partition('+')[2]
        return _rekcalc(a, values)+_rekcalc(b, values)
    elif formula.partition('-')[2] != '':
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
