 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt
import sys

def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop']
    
    if var in labort:
        print('Exited session.')
        sys.exit()
        
    else:
        return var
    
def print_hit(files, i, repair=None):
    if i > 1:
        number = input('-> select wich file: ')
        hit = files[int(number) - 1]
        print('open file', hit, '\n')

    else:
        hit = files[0]
        print('open file', hit, '\n')

    data = np.genfromtxt(hit, dtype='str', delimiter='\n')
    for t in data:
        print(t)
    
    if repair:
        return hit
    
def listdays(month, year, repair=None):
    path = './txt/'+ year + '/' + month + '/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if 'checkpoint' not in f:
                files.append(os.path.join(dirpath, f))
                flag = False
    
    files = sorted(files, key=sorterkey)
    
    i = 0
    for f in files:
        i += 1
        print(f'{str(i):>2}.  {f[14:]}')
        
    if flag:
        print("directory does not exist")
        exit()

    hit = print_hit(files, i, repair)
    
    if repair:
        return hit

def listfiles(day, month, year, repair=None):
    path = './txt/'+ year + '/' + month + '/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in [f for f in filenames if day in f[:2]]:
            if 'ipynb_checkpoints' not in dirpath:
                files.append(os.path.join(dirpath, f))
                flag = False
                
    files = sorted(files, key=sorterkey)
    
    i = 0
    for f in files:
        i += 1
        print(f'{str(i):>2}.  {f[14:]}')
        
    if flag:
        print("file does not exist")
        exit()

    hit = print_hit(files, i, repair)
        
    if repair:
        return hit
    
def sorterkey(line):
    day = line[14:16]
    time = line[21:26].replace('-', '')
    
    return (int(day), int(time))
    

def report(repair=None):
    date = abort(input('month or date: '))
    
    if date.count('.') == 2:
        day, month, year = date.split('.', 2)

        if len(year) == 2:
            year = '20' + year        
        if len(month) == 1:
            month = '0' + month

        hit = listfiles(day, month, year, repair)
        if repair:
            return hit

    elif date.count('.') == 1:
        month, year = date.split('.', 1)

        if len(year) == 2:
            year = '20' + year
        if len(month) == 1:
            month = '0' + month

        hit = listdays(month, year, repair)
        if repair:
            return hit

    else:
        month = date
        if len(month) == 1:
            month = '0' + month
        year = dt.today().strftime("%Y")

        hit = listdays(month, year, repair)
        if repair:
            return hit