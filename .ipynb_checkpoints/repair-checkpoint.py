 #!/usr/bin/env python
    
import numpy as np
import report
import sys
import os
from datetime import datetime as dt
from retry import retry

def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    
    if var in labort:
        print('Exited session.')
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
        
    time = abort(input('change time:'))
    
    if time.count(':') == 1:
        try:
            time = dt.strptime(time, "%H:%M")
        except ValueError:
            print('\ninvalid time\n')
            raise ValueError
        
        print(newdata[0][-5:])
        print(time.strftime("%H:%M"))
        
    for member in range(len(newdata[2:-7])):
        print(newdata[2:-7][member])
        hour = abort(input('change hour:'))

        if hour != '':
            try:
                hour = float(hour)
            except ValueError:
                print('\ninvalid hour\n')
                raise ValueError

            newdata[2:-7][member] = hour