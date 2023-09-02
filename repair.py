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
        print('repair is done.\n\n')
        for line in newdata:
            print(line)
        sys.exit()
        
    else:
        return var

@retry((ValueError), delay=0)
def repair():
    hit = report.report(repair=True)
    print('')
    
    newdata = np.genfromtxt(hit, dtype='str', delimiter='\n')
    
    
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
        
        print(ff.check(date, name=1))
        newdata[-1] = 'holiday = ' + ff.check(date, name=1)
        
        print(' --> changed data\n')
        
        
    time = abort(input('change time: '), newdata=newdata, path=hit)
    
    if time.count(':') == 1:
        try:
            time = dt.strptime(time, "%H:%M")
        except ValueError:
            print('\ninvalid time\n')
            raise ValueError
        
        newdata = np.char.replace(newdata, newdata[0][-5:], time.strftime("%H:%M"))
                           
        print(' --> changed data\n')
        
        
    print(newdata[-4])
    print(newdata[-3], ';', print(newdata[-2]))
    tipsum = abort(input('change tip:'), newdata=newdata, path=hit).replace(',', '.')

    if '+' in tipsum:
        bar, card = tipsum.replace(' ', '').split('+', 1)
        
    
    hour = []
    for i in newdata[2:-7]:
        hour.append(i[5:9])

    i = 0
    for member in range(len(newdata[2:-7])):
        i += 1
        print(newdata[2:-7][member])
        value = abort(input('change hour:'), newdata=newdata, path=hit)

        if value != '':
            try:
                value = float(value)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            hour[member] = value

    for member in range(i, 100):
        i += 1
        print(f'{i+1}"{" " * (4 - len(str(i+1)))}* empty *')
        value= abort(input('add hour:'), newdata=newdata, path=hit)

        if value != '':
            try:
                value = float(value)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            hour.append(value)
            
    