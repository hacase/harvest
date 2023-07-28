 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt
import calendar
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def print_hit(files, i):
    if i > 1:
        number = input('-> select wich file: ')
        hit = files[int(number) - 1]
        print('open file', hit, '\n')

    else:
        hit = files[0]
        print('open file', hit, '\n')

    data = np.genfromtxt(hit, dtype='str', delimiter='\n')
    for t in data:
        print(t)
    
def sorterkey(line):
    year = line[6:10]
    month = line[11:13]
    day = line[14:16]
    time = line[21:26].replace('-', '')
    
    return (int(year), int(month), int(day), int(time))

def statistic():
    path = './txt/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if 'ipynb_checkpoints' not in dirpath:
                files.append(os.path.join(dirpath, f))
                flag = False

    files = sorted(files, key=sorterkey)

    date = []
    weekday = []
    time = []
    ratio = []
    total = []
    bar = []
    card = []
    holiday = []

    for file in files:
        data = np.genfromtxt(file, dtype='str', delimiter='\n')
        s_date, s_time = data[0].split(', ', 1)
        date.append(s_date)

        weekday.append(dt.strptime(s_date, "%d.%m.%Y").weekday())

        if int(s_time[-5:-3]) > 17:
            time.append('PM')
        else:
            time.append('AM')

        for line in data[1:]:
            if 'ratio' in line:
                ratio.append(float(line[12:-3]))

            elif 'sum' in line:
                total.append(float(line[6:]))

            elif 'bar' in line:
                try:
                    bar.append(float(line[6:]))
                except ValueError:
                    bar.append(line[6:])

            elif 'card' in line:
                try:
                    card.append(float(line[7:]))
                except ValueError:
                    card.append(line[7:])

            elif 'holiday' in line:
                try:
                    holiday.append(float(line[10:]))
                except ValueError:
                    holiday.append(line[10:])

    bar = list(filter(lambda item: item != 'None', bar))
    card = list(filter(lambda item: item != 'None', card))

    print(f'total: {np.mean(total):7.3f} +/- {np.std(total):6.3f}')
    print(f'ratio: {np.mean(ratio):7.3f} +/- {np.std(ratio):6.3f}')
    print(f'bar:   {np.mean(bar):7.3f} +/- {np.std(bar):6.3f}')
    print(f'card:  {np.mean(card):7.3f} +/- {np.std(card):6.3f}')

    print('')

    print('top three')
    line = ' '*6 + 'total' + ' '*6 + 'ratio' + ' '*8 + 'timestamp'
    print(line)
    line = '-'*3 + '+' + '-'*9 + '+' + '-'*10 + '+' + '-'*18
    print(line)

    top = sorted(zip(total, ratio, date, time), reverse=True)[:3]
    for i in range(len(top)):
        wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
        print(f'{i+1}":  {float(top[i][0]):6.2f}€   {float(top[i][1]):5.3f}€/h   {top[i][2]:10} {wkday} {top[i][3]}')
        print(f'{" "*5}holiday -> {holiday[i].capitalize()}')

    print('')

    total = np.array(total)
    ratio = np.array(ratio)

    print('AM')
    AM = [i == 'AM' for i in time]
    print(f'total: {np.mean(total[AM]):7.3f} +/- {np.std(total[AM]):6.3f}')
    print(f'ratio: {np.mean(ratio[AM]):7.3f} +/- {np.std(ratio[AM]):6.3f}')

    print('')

    print('PM')
    PM = [i == 'PM' for i in time]
    print(f'total: {np.mean(total[PM]):7.3f} +/- {np.std(total[PM]):6.3f}')
    print(f'ratio: {np.mean(ratio[PM]):7.3f} +/- {np.std(ratio[PM]):6.3f}')

    print('')
    print('')

    print('holidays with weekends (Fri - Sun)')   
    mask = [i != 'False' for i in holiday]
    for i in range(len(weekday)):
        if 3 < weekday[i] < 7:
            mask[i] = True

    print(f'total: {np.mean(total[mask]):7.3f} +/- {np.std(total[mask]):6.3f}')
    print(f'ratio: {np.mean(ratio[mask]):7.3f} +/- {np.std(ratio[mask]):6.3f}')

    print('')

    print('normal days')
    mask = [not i for i in mask]
    print(f'total: {np.mean(total[mask]):7.3f} +/- {np.std(total[mask]):6.3f}')
    print(f'ratio: {np.mean(ratio[mask]):7.3f} +/- {np.std(ratio[mask]):6.3f}')

    print('')
    print('')

    for i in range(0, 7):
        print(calendar.day_name[i])

        mask = [n == i for n in weekday]
        print(f'total: {np.mean(total[mask]):7.3f} +/- {np.std(total[mask]):6.3f}')
        print(f'ratio: {np.mean(ratio[mask]):7.3f} +/- {np.std(ratio[mask]):6.3f}')

        print('')