 #!/usr/bin/env python

import numpy
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

def listdays(month, year):
    try:
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

        data = np.genfromtxt(path, dtype='str', delimiter='\t')
        print(data)

    except:
        print('i have a bad feeling about this')

def listfiles(day, month, year):
    try:
        path = './txt/'+ year + '/' + month + '/'

        flag = True
        files = []
        i = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in [f for f in filenames if day in f[:2]]:
                if 'ipynb_checkpoints' not in dirpath:
                    i += 1
                    print(i, os.path.join(dirpath, f))

                    files.append(os.path.join(dirpath, f))
                    flag = False
        if flag:
            print("file does not exist")

        data = np.genfromtxt(path, dtype='str', delimiter='\t')
        print(data)

    except:
        print('i have a bad feeling about this')


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