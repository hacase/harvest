 #!/usr/bin/env python
    
import numpy as np
import report
import ferienfeiertage as ff
from calctip import calctip
import sys
import os
from datetime import datetime as dt
from retry import retry

def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    ldone = ['done']
    
    if var in labort:
        print('Exited session.')
        sys.exit()
        
    elif var in ldone:
        print('repair is done.')
        sys.exit()
        
    else:
        return var

@retry((ValueError), delay=0)
def repair():
    hit = report.report(repair=True)
    print('')
    
    newdata = np.genfromtxt(hit, dtype='str', delimiter='\n')
    
    
    print(newdata[0])
    date = abort(input('change date:'))
    
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
        
        print(newdata[0][:-13]) #= date.strftime("%d.%m.%Y")
        print(date.strftime("%d.%m.%Y, %A"))
        
        print(ff.check(date, name=1))
        newdata[-1] = 'holiday =' + ff.check(date, name=1)
        
        
    time = abort(input('change time:'))
    
    if time.count(':') == 1:
        try:
            time = dt.strptime(time, "%H:%M")
        except ValueError:
            print('\ninvalid time\n')
            raise ValueError
        
        print(newdata[0][-5:])
        print(time.strftime("%H:%M"))
        
        
    print(newdata[-4])
    print(newdata[-3], ';', print(newdata[-2]))
    tipsum = abort(input('change tip:')).replace(',', '.')

    if '+' in tipsum:
        bar, card = tipsum.replace(' ', '').split('+', 1)
        
    
    hour = []
    for i in newdata[2:-7]:
        hour.append(i[5:9])

    i = 0
    for member in range(len(newdata[2:-7])):
        i += 1
        print(newdata[2:-7][member])
        value = abort(input('change hour:'))

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
        value= abort(input('add hour:'))

        if value != '':
            try:
                value = float(value)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            hour.append(value)
            
    