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

def texCalc(formula, values=''):
    ''' claculate the formula recursively with the given values '''
    # sqrt:
    if formula.strip().startswith('\sqrt'):
        return str(math.sqrt(float(texCalc(formula[5:], values))))
    # brackets:
    if formula.strip().startswith('('):
        n=1
        formula=formula[1:]
        part1 = ''
        while len(formula)>0:
            if formula.startswith('('):
                n=n+1
            elif formula.startswith(')'):
                n=n-1
            if n==0:
                formula=formula[1:]
                break
            part1=part1+formula[0]
            formula=formula[1:]
        formula = str(texCalc(part1, values))+formula
    # arithmetic operations:
    if formula.partition('*')[2] != '':
        a = formula.partition('*')[0]
        b = formula.partition('*')[2]
        return texCalc(a, values)*texCalc(b, values)
    elif formula.partition('/')[2] != '':
        a = formula.partition('/')[0]
        b = formula.partition('/')[2]
        return texCalc(a, values)/texCalc(b, values)
    elif formula.partition('+')[2] != '':
        a = formula.partition('+')[0]
        b = formula.partition('+')[2]
        return texCalc(a, values)+texCalc(b, values)
    elif formula.partition('-')[2] != '':
        a = formula.partition('-')[0]
        b = formula.partition('-')[2]
        return texCalc(a, values)-texCalc(b, values)
    else:
        # there are no more arithmetic operators left
        # replace values
        if formula in values:
            return values[formula]
        else:
            try:
                return int(formula)
            except ValueError:
                return float(formula)
