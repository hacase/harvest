import numpy
import re
from datetime import datetime as dt
import sys

from harvest_func import abort, tmode



def submit():
    while True:
        half_day = input('half day? [/y]: ')
        if half_day:
            half_day = True
        else:
            half_day = False

        date = False
        while date == False:
            date = abort(input('date: '))
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
        time = abort(input('time: '))
        if time:
            time = re.sub(r'[^\d]+','',time)
        else:
            time = '1900'
        
        try:
            time = time[:-2] +':'+ time[-2:]
            timestamp = dt.strptime(date.strftime('%d.%m.%y.') + time, '%d.%m.%y.%H:%M')
            break
            
        except ValueError:
            print('time not parsable')
    
    i = 1
    value = abort(input('{}{} = '.format(i, ". Hour")))
    
    tmode(value, timestamp, half_day)