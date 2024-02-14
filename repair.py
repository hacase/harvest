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

def print_jsontable(jData, text=None):
    date, time = jData['timestamp'].split('-')
    day = dt.strptime(date, "%d.%m.%Y").strftime("%A")
    text.append(date+', '+day+', time: '+time)
    text.append('\n')

    text.append('-' *  32)
    text.append('\n')

    hour = jData['hour']
    roundtip = jData['tip']
    realtip = jData['tip_exact']

    for i in range(len(hour)):
        t = f'{i+1}"{" " * (4 - len(str(i+1)))}{hour[i]:4.2f}h  -> {roundtip[i]:5.1f}€  ;  {realtip[i]:6.3f}'
        text.append(t)
        text.append('\n')

    text.append('-' *  32)
    text.append('\n')

    t = 'total hours =' + '{0:.2f}'.format(sum(hour)) + 'h'
    text.append(t)
    text.append('\n')

    t = f'tip ratio = {jData["ratio"]} €/h'
    text.append(t)
    text.append('\n')

    t = f'sum = {float(jData["sum"]):.2f} €'
    text.append(t)
    text.append('\n')

    t = f'bar = {jData["bar"]} €'
    text.append(t)
    text.append('\n')

    t = f'card = {jData["card"]} €'
    text.append(t)
    text.append('\n')

    t = 'holiday = ' + jData['holiday'] + '\n'
    text.append(t)
    text.append('\n')
    
    if text:
        return text

def abort(var, newdata=None, path=None):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    ldone = ['done']
    
    if var in labort:
        print('exited session.')
        sys.exit()
        
    elif var in ldone:                
        f = open(path)
        jData = json.loads(f.read())
        
        jnewdata = newdata
        
        text = list()
        text.append('-< edit ')
        text.append(dt.today().strftime("%d.%m.%Y, %A, time: %H:%M"))
        text.append(' to ')
        newdate = dt.strptime(jnewdata['timestamp'], '%d.%m.%Y-%H:%M')
        text.append(newdate.strftime("%d.%m.%Y, %A, time: %H:%M"))
        text.append(' >-')
        text.append('\n')
        text = print_jsontable(jData, text = text) 
        
        date = dt.strptime(jData['timestamp'], '%d.%m.%Y-%H:%M')
        timestamp = date.strftime("%d-%a-%H-%M")
        dirname = date.strftime("./json/%Y/%m/")
        newpath = dirname + '/' + timestamp +'-edited.txt'
        
        os.makedirs(os.path.dirname(dirname), exist_ok=True)
        with open(newpath, 'w+') as f:
            f.writelines(text)
        
        text = list()
        
        text = print_jsontable(jData, text = text) 
        text.append('\n')
        text.append('\n')
        text.append('-< edit ')
        text.append(dt.today().strftime("%d.%m.%Y, %A, time: %H:%M"))
        text.append(' >-')
        text.append('\n')
        text.append('\n')
        text.append('\n')
        text.append('\n')
        
        text = print_jsontable(jnewdata, text = text)
        
        date = dt.strptime(jnewdata['timestamp'], '%d.%m.%Y-%H:%M')
        timestamp = date.strftime("%d-%a-%H-%M")
        dirname = date.strftime("./json/%Y/%m/")
        path = dirname + '/' + timestamp +'-LOG.txt'
        
        os.makedirs(os.path.dirname(dirname), exist_ok=True)
        with open(path, 'w+') as f:
            f.writelines(text)
        
        text = list()
        
        date = dt.strptime(jnewdata['timestamp'], '%d.%m.%Y-%H:%M')
        timestamp = date.strftime("%d-%a-%H-%M")
        dirname = date.strftime("./json/%Y/%m/")
        newpath = dirname + '/' + timestamp +'.json'

        print(jnewdata)
        os.makedirs(os.path.dirname(dirname), exist_ok=True)
        with open(newpath, 'w+') as f:
            json.dump(jnewdata, f)
        
        os.remove(path)
        print('done repairing.\n\n')
        sys.exit()
        
    else:
        return var
    
def rewrite_table(jData, tipsum, bar, card):
    roundtip, tipsum, real, realtip, ratio = fcalctip(jData['hour'], float(tipsum))
            
    jData['bar'] = str(bar)
    jData['card'] = str(card)
    jData['tip'] = str(roundtip)
    jData['sum'] = '{0:.2f}'.format(tipsum)
    jData['tip_exact'] = str(realtip)
    jData['ratio'] = f'{ratio:.4}'
    
    return jData


#@retry((ValueError), delay=0)
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
        
    print('time:', time)
    newtime = abort(input('change time: '), newdata=jData, path=hit)
    
    if newtime.count(':') == 1:
        try:
            newtime = dt.strptime(newtime, "%H:%M")
        except ValueError:
            print('\ninvalid time\n')
            raise ValueError
        
        jData['timestamp'] = jData['timestamp'].replace(time, newtime.strftime("%H:%M"))
                           
        print(' --> changed data')
        
        
    print('')
    
    
    print(f'sum = {float(jData["sum"]):.2f} €')
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
    print(jData['hour'])
        
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