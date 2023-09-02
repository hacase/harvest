 #!/usr/bin/env python
    
import numpy as np
import report
import ferienfeiertage as ff
from calctip import fcalctip
import sys
import os
from datetime import datetime as dt
from retry import retry

def abort(var, newdata=None, path=None):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    ldone = ['done']
    
    if var in labort:
        print('exited session.')
        sys.exit()
        
    elif var in ldone:
        print('doen repairing.\n\n')
        
        newpath = path[:-4] + '-LOG.txt'
        os.rename(path, newpath)
        
        text = list()
        
        text.append('\n\n')
        text.append('-< edited on ')
        text.append(dt.today().strftime("%d.%m.%Y") + ', ' + dt.today().strftime("%A") + ', time: ' + dt.now().strftime("%H:%M"))
        text.append(' >-')
        text.append('\n\n\n')
        
        for line in newdata:
            text.append(line + '\n')
        
        with open(newpath, "a") as f:
            f.writelines(text)
            
            
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
    
def rewrite_table(newdata, hour, tipsum, bar, card, holiday):
    roundtip, tipsum, real, realtip, ratio = fcalctip(hour, float(tipsum))
            
    for i in range(len(hour)):
        t = f'{i+1}"{" " * (4 - len(str(i+1)))}{hour[i]:4.2f}h  -> {roundtip[i]:5.1f}€  ;  {realtip[i]:6.3f}'

        newdata[2+i] = np.char.replace(newdata[2+i], newdata[2+i], t)
        
    newdata[-7] = np.char.replace(newdata[-7], newdata[-7], '-' *  32)
    
    t = f'total hours = {sum(hour):} h'
    newdata[-6] = np.char.replace(newdata[-6], newdata[-6], t)
    
    t = f'tip ratio = {ratio:.4} €/h'
    newdata[-5] = np.char.replace(newdata[-5], newdata[-5], t)
    
    t = 'sum = ' + str(tipsum)
    newdata[-4] = np.char.replace(newdata[-4], newdata[-4], t)
    
    t = 'bar = ' + str(bar)
    newdata[-3] = np.char.replace(newdata[-3], newdata[-3], t)
    
    t = 'card = ' + str(card)
    newdata[-2] = np.char.replace(newdata[-2], newdata[-2], t)
                       
    t = 'holiday = ' + holiday
    newdata[-1] = np.char.replace(newdata[-1], newdata[-1], t)


@retry((ValueError), delay=0)
def repair():
    hit = report.report(repair=True)
    print('')
    
    newdata = np.genfromtxt(hit, dtype='str', delimiter='\n')
    
    tipsum = newdata[-4][6:]
    bar = newdata[-3][6:]
    card = newdata[-2][7:]
    holiday = newdata[-1][10:]
    
    
    print(newdata[0])
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
        
        oldtime = newdata[0][-5:]
        newdata = np.char.replace(newdata, newdata[0], date.strftime("%d.%m.%Y, %A, time: ") + oldtime)
        
        print('holiday =', ff.check(date, name=1))
        newdata[-1] = 'holiday = ' + ff.check(date, name=1)
        
        print(' --> changed data')
        
        
    print('')        
        
        
    time = abort(input('change time: '), newdata=newdata, path=hit)
    
    if time.count(':') == 1:
        try:
            time = dt.strptime(time, "%H:%M")
        except ValueError:
            print('\ninvalid time\n')
            raise ValueError
        
        newdata = np.char.replace(newdata, newdata[0][-5:], time.strftime("%H:%M"))
                           
        print(' --> changed data')
        
        
    print('')
    
    
    print(newdata[-4])
    print(newdata[-3], ';', newdata[-2])
    
    value = abort(input('change tip: '), newdata=newdata, path=hit).replace(',', '.')
    
    if value:
        try:
            if '+' in value:
                bar, card = value.replace(' ', '').split('+', 1)
                
                bar = float(bar)
                card = float(card)
                
                tipsum = float(bar) + float(card)
                
            else:
                tipsum = float(value)
                
            hour = []
            for i in newdata[2:-7]:
                hour.append(float(i[5:9]))
                
            rewrite_table(newdata, hour, tipsum, bar, card, holiday)
                
            print(' --> changed data')
        
        except ValueError:
            print('\ninvalid tip\n')
            raise ValueError
            
    
    print('')
    
            
    abort(input('change hour? '), newdata=newdata, path=hit)
        
    hour = []
    for i in newdata[2:-7]:
        hour.append(float(i[5:9]))
        
    i = 0
    for member in range(len(newdata[2:-7])):
        i += 1
        print(newdata[2:-7][member])
        value = abort(input('change hour: '))

        if value != '':
            try:
                value = float(value)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            hour[member] = value

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

            hour.append(value)
            
    added = i - len(newdata[2:-7]) - 1
    newdata = np.insert(newdata, -8, [''] * added)
        
    
    rewrite_table(newdata, hour, tipsum, bar, card, holiday)

    print(' --> changed data\n')
    abort('done', newdata=newdata, path=hit)