#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


def poly2latex(p, var='x', name='y=', reversed=True, short_latex=True, digit=2):
    def format_one(value, power, var):
        if digit > 0:
            base = ('{:+1.'+str(digit)+'f}').format(value)
        else:
            base = '{:+1d}'.format(int(value))

        if power == 0:
            return base

        if power == 1:
            return '{base}{var}'.format(**locals())
        return '{base}{var}^{power}'.format(**locals())

    power = 0
    result = list()
    latex = '$' if short_latex else '$$'
    for value in p:
        result.append(format_one(value, power, var))
        power += 1

    if reversed:
        result.reverse()
    result_str = ''.join(result)
    return '{latex}{name}{}{latex}'.format(result_str[1:] if result_str.startswith('+') else result_str, **locals())
