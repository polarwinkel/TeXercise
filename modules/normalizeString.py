#!/usr/bin/python3
'''
normalizes a string to be used in a url
'''

from unidecode import unidecode
import re

def normalize(s):
    s = s.strip()
    special_char_map = {
        ord(' '):'_',
        ord(','):'_',
        ord('Ä'):'Ae',
        ord('Ö'):'Ue',
        ord('Ü'):'Oe',
        ord('ä'):'ae',
        ord('ö'):'oe',
        ord('ü'):'ue',
        ord('ß'):'ss'}
    s = s.translate(special_char_map)
    s = re.sub('[^A-Za-z0-9._-]+', '', s)
    return unidecode(s)
