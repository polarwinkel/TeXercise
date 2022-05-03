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
        formula = part0+str(texCalc(part1, values))+formula
    # sqrt:
    if formula.find('\sqrt')>=0:
        part0 = formula[0:formula.find('\sqrt')]
        formula = formula[formula.find('\sqrt')+5:]
        ops = ['*','/','+','-']
        num = ''
        for i in range(len(formula)):
            if formula[i] in ops:
                formula = formula[1:]
                break
            num = num+formula[i]
        return texCalc(part0+str(math.sqrt(float(num)))+formula, values)
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
