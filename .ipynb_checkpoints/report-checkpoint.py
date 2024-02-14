 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt
import sys
import json

def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop']
    
    if var in labort:
        print('exited session.')
        sys.exit()
        
    else:
        return var
    
def listdays(month, year, repair=None):
    path = './json/'+ year + '/' + month + '/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if not any(s in f for s in ['checkpoint', 'DS']):
                files.append(os.path.join(dirpath, f))
                flag = False
    
    files = sorted(files, key=sorterkey)
    
    i = 0
    for f in files:
        i += 1
        print(f'{str(i):>2}.  {f[15:]}')
        
    if flag:
        print("directory does not exist")
        sys.exit()

    hit = print_hit(files, i, repair)
    
    if repair:
        return hit

def listfiles(day, month, year, repair=None):
    path = './json/'+ year + '/' + month + '/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in [f for f in filenames if day in f[:2]]:
            if not any(s in f for s in ['checkpoint', 'DS']):
                files.append(os.path.join(dirpath, f))
                flag = False
                
    files = sorted(files, key=sorterkey)
    
    i = 0
    for f in files:
        i += 1
        print(f'{str(i):>2}.  {f[25:]}')
        
    if flag:
        print("file does not exist")
        sys.exit()

    hit = print_hit(files, i, repair)
        
    if repair:
        return hit
    
def sorterkey(line):
    day = line[15:17]
    time = line[22:27].replace('-', '')
    
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
        
def print_hit(files, i, repair=None):
    if i > 1:
        number = abort(input('-> select wich file: '))
        hit = files[int(number) - 1]
        print('open file', hit, '\n')

    else:
        hit = files[0]
        print('open file', hit, '\n')

    if any(s in hit for s in ['LOG', 'edited']):
        data = np.genfromtxt(hit, dtype='str', delimiter='\n')
        for t in data:
            print(t)
    else:
        f = open(hit)
        jData = json.loads(f.read())
        date, time = jData['timestamp'].split('-')
        day = dt.strptime(date, "%d.%m.%Y").strftime("%A")
        print(date+',', day+',', 'time:', time)
        
        print('-' *  32)
        
        hour = jData['hour']
        roundtip = jData['tip']
        realtip = jData['tip_exact']
        
        for i in range(len(hour)):
            t = f'{i+1}"{" " * (4 - len(str(i+1)))}{hour[i]:4.2f}h  -> {roundtip[i]:5.1f}€  ;  {realtip[i]:6.3f}'
            print(t)
        
        print('-' *  32)
        
        t = 'total hours =' + '{0:.2f}'.format(sum(hour)) + 'h'
        print(t)
        
        t = f'tip ratio = {jData["ratio"]} €/h'
        print(t)
        
        t = f'sum = {jData["sum"]:.2f} €'
        print(t)
        
        t = f'bar = {jData["bar"]} €'
        print(t)
        
        t = f'card = {jData["card"]} €'
        print(t)
        
        t = 'holiday = ' + jData['holiday'] + '\n'
        print(t)
        
    print('')
    
    if repair:
        return hit