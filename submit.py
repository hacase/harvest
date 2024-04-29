import numpy
import re
from datetime import datetime as dt
from calctip import tmode, abort


while True:
    dummy = input('dummy? ')
    if dummy:
        dummy = True
    else:
        dummy = False
        
    date = input('date: ')
    if date[-1] == '.':
        date = date[:-1]
    
    try:
        if date.find('.') == -1:
            date = dt.strptime(date + dt.today().strftime('%m%Y'), '%d%m%Y')
            break

        elif date.count('.') == 1:
            date = dt.strptime(date + dt.today().strftime('%Y'), '%d.%m%Y')
            break
            
        elif date.count('.') == 2:
            _, _, year = date.split('.')
            if len(year) == 2:
                date = dt.strptime(date, '%d.%m.%y')
            else:
                date = dt.strptime(date, '%d.%m.%Y')
            break
            
    except ValueError:
        print('date not parsable')

while True:
    time = input('time: ')
    time = re.sub(r'[^\d]+','',time)
    
    try:
        time = time[:-2] +':'+ time[-2:]
        timestamp = dt.strptime(date.strftime('%d.%m.%y.') + time, '%d.%m.%y.%H:%M')
        break
        
    except ValueError:
        print('time not parsable')

i = 1
value = abort(input('{}{} = '.format(i, ". Hour")))

tmode(value, timestamp, dummy)