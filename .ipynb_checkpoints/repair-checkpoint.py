 #!/usr/bin/env python
    
import numpy as np
import report
import ferienfeiertage as ff
from calctip import fcalctip
import sys
import os
from datetime import datetime as dt
from retry import retry
import json

def abort(var, newdata=None, path=None):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    ldone = ['done']
    
    if var in labort:
        print('exited session.')
        sys.exit()
        
    elif var in ldone:
        print('done repairing.\n\n')
        
        newpath = path[:-5] + '-LOG.txt'
        os.rename(path, newpath)
        
        text = list()
        
        text.append('\n')
        text.append('\n')
        text.append('-< edit ')
        text.append(dt.today().strftime("%d.%m.%Y") + ', ' + dt.today().strftime("%A") + ', time: ' + dt.now().strftime("%H:%M"))
        text.append(' >-')
        text.append('\n')
        text.append('\n')
        text.append('\n')
        
        for line in newdata:
            text.append(line + '\n')
        
        with open(newpath, "a") as f:
            f.writelines(text)
            
        data = np.genfromtxt(newpath, dtype='str', delimiter='\n')
        
        for line in data:
            if '-< edit' in line:
                print('\n\n' + line + '\n\n')
                
            else:
                print(line)
            
        date = dt.strptime(newdata[0], "%d.%m.%Y, %A, time: %H:%M")
        
        timestamp = date.strftime("%d") + '-' + date.strftime("%a") + '-' + date.strftime("%H-%M")
        dirname = './txt/'+ date.strftime("%Y") + '/' + date.strftime("%m") + '/'
        path = dirname + '/' + timestamp +'.txt'
        
        os.makedirs(os.path.dirname(dirname), exist_ok=True)
        
        text = list()
        
        for line in newdata:
            text.append(line + '\n')
            
        with open(path, 'w+') as f:
            f.writelines(text)
        
        sys.exit()
        
    else:
        return var
    
def rewrite_table(jData, tipsum, bar, card):
    roundtip, tipsum, real, realtip, ratio = fcalctip(jData['hour'], float(tipsum))
            
    jData['bar'] = str(bar)
    jData['card'] = str(card)
    jData['tip'] = roundtip
    jData['sum'] = '{0:.2f}'.format(tipsum)
    jData['tip_exact'] = realtip
    jData['ratio'] = f'{ratio:.4}'


@retry((ValueError), delay=0)
def repair():
    hit = report.report(repair=True)
    print('')
    
    f = open(hit)
    jData = json.loads(f.read())
    
    tipsum = float(jData['sum'])
    bar = jData['bar']
    card = jData['card']
    holiday = jData['holiday']
    
    
    date, time = jData['timestamp'].split('-')
    day = dt.strptime(date, "%d.%m.%Y").strftime("%A")
    print(date+',', day+',', 'time:', time)
    date = abort(input('change date: '))
    
    if date.count('.') == 2:
        day, month, year = date.split('.', 2)
        
        if len(year) == 2:
            year = '20' + year
            
        date = day +'.'+ month +'.'+ year
        try:
            date = dt.strptime(date, "%d.%m.%Y")
        except ValueError:
            print('\ninvalid date\n')
            raise ValueError
        
        jData['timestamp'] = date.strftime("%d.%m.%Y-") + time
        
        print('holiday =', ff.check(date, name=1))
        jData['holiday'] = ff.check(date, name=1)
        
        print(' --> changed data')
        
        
    print('')        
        
        
    newtime = abort(input('change time: '), newdata=jData, path=hit)
    
    if newtime.count(':') == 1:
        try:
            newtime = dt.strptime(newtime, "%H:%M")
        except ValueError:
            print('\ninvalid time\n')
            raise ValueError
        
        newdata = np.char.replace(jData['timestamp'], time, newtime.strftime("%H:%M"))
                           
        print(' --> changed data')
        
        
    print('')
    
    
    print(f'sum = {float(jData["bar"])+float(jData["card"]):.2f} €')
    print(f'bar = {jData["bar"]} €', f'card = {jData["card"]} €')
    
    value = abort(input('change tip: '), newdata=jData, path=hit).replace(',', '.')
    
    if value:
        try:
            if '+' in value:
                bar, card = value.replace(' ', '').split('+', 1)
                
                bar = float(bar)
                card = float(card)
                
                tipsum = float(bar) + float(card)
                
            else:
                tipsum = float(value)
                
            hour = jData['hour']
                
            jData = rewrite_table(jData, tipsum, bar, card)
                            
            print(' --> changed data')
        
        except ValueError:
            print('\ninvalid tip\n')
            raise ValueError
            
    
    print('')
    
            
    abort(input('change hour? '), newdata=jData, path=hit)
        
    for i in range(len(jData['hour'])):
        print(f'{i+1:2}.: {jData["hour"][i]:2.2}h')
        value = abort(input('change hour: '))

        if value != '':
            try:
                value = float(value)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            jData['hour'][i] = value

    for member in range(i, 100):
        print(f'{i+1}"{" " * (4 - len(str(i+1)))}* empty *')
        i += 1
        
        value = input('add hour: ')
                      
        if value == 'done':
            break
        else:
            abort(value)

        if value != '':
            try:
                value = float(value)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            jData['hour'].append(value)
                   
    
    jData = rewrite_table(jData, tipsum, bar, card)

    print(' --> changed data\n')
    abort('done', newdata=jData, path=hit)