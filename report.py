 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt

def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop']
    
    if var in labort:
        print('Exited session.')
        sys.exit()
        
    else:
        return var
    
def print_hit(files, i):
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
    
def listdays(month, year):
    path = './txt/'+ year + '/' + month + '/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if 'checkpoint' not in f:
                i += 1
                print(str(i) + '.', f)

                files.append(os.path.join(dirpath, f))
                flag = False
    if flag:
        print("directory does not exist")

    print_hit(files, i)

def listfiles(day, month, year):
    path = './txt/'+ year + '/' + month + '/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in [f for f in filenames if day in f[:2]]:
            if 'ipynb_checkpoints' not in dirpath:
                i += 1
                print(str(i) + '.', f)

                files.append(os.path.join(dirpath, f))
                flag = False
    if flag:
        print("file does not exist")

    print_hit(files, i)

def report():
    date = abort(input('month or date: '))
    
    if date.count('.') == 2:
        day, month, year = date.split('.', 2)

        if len(year) == 2:
            year = '20' + year        
        if len(month) == 1:
            month = '0' + month

        listfiles(day, month, year)

    elif date.count('.') == 1:
        month, year = date.split('.', 1)

        if len(year) == 2:
            year = '20' + year
        if len(month) == 1:
            month = '0' + month

        listdays(month, year)

    else:
        month = date
        if len(month) == 1:
            month = '0' + month
        year = dt.today().strftime("%Y")

        listdays(month, year)