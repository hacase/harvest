 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt
import calendar
import warnings
from calctip import abort
import subprocess

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

def ticker(tick, temp):
    minTick = np.floor(np.min(temp) / tick) * tick
    maxTick = np.ceil(np.max(temp) / tick) * tick
    major = np.arange(minTick, maxTick, tick)
    minor = np.arange(minTick, maxTick, tick/2)
    
    return major, minor

def statistic():
    path = './txt/'

    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if 'ipynb_checkpoints' not in dirpath:
                if 'LOG' not in f:
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
    print('')

    print('top three: total')
    line = ' '*6 + 'total' + ' '*6 + 'ratio' + ' '*8 + 'timestamp'
    print(line)
    line = '-'*3 + '+' + '-'*9 + '+' + '-'*10 + '+' + '-'*18
    print(line)

    top = sorted(zip(total, ratio, date, time, holiday), reverse=True)[:3]
    for i in range(len(top)):
        wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
        print(f'{i+1}":  {float(top[i][0]):6.2f}€   {float(top[i][1]):5.3f}€/h   {top[i][2]:10} {wkday} {top[i][3]}')
        print(f'{" "*5}holiday -> {top[i][4].capitalize()}')
        
    print('')
    print('')
    
    print('top three: ratio')
    line = ' '*6 + 'ratio' + ' '*6 + 'total' + ' '*8 + 'timestamp'
    print(line)
    line = '-'*3 + '+' + '-'*9 + '+' + '-'*10 + '+' + '-'*18
    print(line)

    top = sorted(zip(ratio, total, date, time, holiday), reverse=True)[:3]
    for i in range(len(top)):
        wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
        print(f'{i+1}": {float(top[i][0]):5.2f}€/h   {float(top[i][1]):6.3f}€   {top[i][2]:10} {wkday} {top[i][3]}')
        print(f'{" "*5}holiday -> {top[i][4].capitalize()}')
        

    print('')
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
        
    print('')
    
    print('frequency')
    print('total:', len(weekday),
          ', AM:', (np.array(time) == 'AM').sum(),
          ', PM:', (np.array(time) == 'PM').sum())

    def chunker(part, full):
        chunks, remain = divmod(int(part * 8 / full * 100), 8)
        bar = '█' * chunks

        if remain > 0:
            bar += chr(ord('█') + (8 - remain))

        return bar

    for i in range(7):
        day = (np.array(weekday) == i).sum()
        s = chunker(day, len(weekday))
        s += f'{(np.array(weekday) == i).sum():3}, '
        s += f'{(np.array(weekday) == i).sum() / len(weekday)*100:3.1f}%'

        print(s)
        
    print('')
    print('')

    
    render = abort(input('render plot? '))        
    
    import matplotlib.pyplot as plt
    
    Ptime = [[] for _ in range(4)]
    Ptotal = [[] for _ in range(7)]
    Pbar = [[] for _ in range(7)]
    Pcard = [[] for _ in range(7)]
    Pall = [[] for _ in range(14)]

    Rtime = [[] for _ in range(4)]
    Rtotal = [[] for _ in range(7)]
    Rbar = [[] for _ in range(7)]
    Rcard = [[] for _ in range(7)]
    Rall = [[] for _ in range(14)]


    AM = [i == 'AM' for i in time]

    ferien = [i != 'False' for i in holiday]
    for i in range(len(weekday)):
            if 3 < weekday[i] < 7:
                ferien[i] = True

    for i in range(len(total)):
        if AM[i]:
            Ptime[0].append(total[i])
            Rtime[0].append(ratio[i])
        else:
            Ptime[1].append(total[i])
            Rtime[1].append(ratio[i])

        if ferien[i]:
            Ptime[2].append(total[i])
            Rtime[2].append(ratio[i])
        else:
            Ptime[3].append(total[i])
            Rtime[3].append(ratio[i])

        total[i] = float(total[i])

        Ptotal[weekday[i]].append(total[i])
        Rtotal[weekday[i]].append(ratio[i])

    for i in range(len(bar)):
        if bar[i] != 'None':
            Pbar[weekday[i]].append(bar[i])
        if card[i] != 'None':
            Pcard[weekday[i]].append(card[i])

    for i in range(1, 8):
        Pall[i *2 -2] = Pbar[i -1]
        Pall[i *2 -1] = Pcard[i -1]

    c = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']


    fig, axs = plt.subplots(2, 2)

    axs[0, 0].set_title('time, total')
    axs[0, 0].boxplot(Ptime)
    plt.sca(axs[0, 0])
    plt.xticks(range(5), ['', 'AM', 'PM', 'special', 'normal'], rotation=45)
    plt.ylabel('€')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Ptime for item in row]
    major, minor = ticker(20, temp)
    axs[0, 0].set_yticks(major)
    axs[0, 0].set_yticks(minor, minor = True)
    for i in range(4):
        axs[0, 0].plot(np.ones(len(Ptime[i])) *i +1, Ptime[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])


    axs[1, 0].set_title('time, ratio')
    axs[1, 0].boxplot(Rtime)
    plt.sca(axs[1, 0])
    plt.xticks(range(5), ['', 'AM', 'PM', 'special', 'normal'], rotation=45)
    plt.ylabel('€/h')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Rtime for item in row]
    major, minor = ticker(1, temp)
    axs[1, 0].set_yticks(major)
    axs[1, 0].set_yticks(minor, minor = True)
    for i in range(4):
        axs[1, 0].plot(np.ones(len(Rtime[i])) *i +1, Rtime[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])


    axs[0, 1].set_title('weekday, total')
    axs[0, 1].boxplot(Ptotal)
    plt.sca(axs[0, 1])
    plt.xticks(np.arange(8), ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    plt.ylabel('€')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Ptotal for item in row]
    major, minor = ticker(20, temp)
    axs[0, 1].set_yticks(major)
    axs[0, 1].set_yticks(minor, minor = True)
    #axs[0, 1].set_xticks(range(8))
    #axs[0, 1].set_xticklabels(['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    for i in range(7):
        axs[0, 1].plot(np.ones(len(Ptotal[i])) *i +1, Ptotal[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])


    axs[1, 1].set_title('weekday, ratio')
    axs[1, 1].boxplot(Rtotal)
    plt.sca(axs[1, 1])
    plt.xticks(np.arange(8), ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    plt.ylabel('€/h')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Rtotal for item in row]
    major, minor = ticker(1, temp)
    axs[1, 1].set_yticks(major)
    axs[1, 1].set_yticks(minor, minor = True)
    for i in range(7):
        axs[1, 1].plot(np.ones(len(Rtotal[i])) *i +1, Rtotal[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])


    fig.tight_layout()
    if render == 'android':
        plt.savefig('harvest.png')
        subprocess.call('termux-open harvest.png', shell=True)
        
    else:
        plt.show()
    
    
    print('render plots done.')