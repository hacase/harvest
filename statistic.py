 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt
import calendar
import warnings
from calctip import abort, git_update
import subprocess
import json
from urllib import request
import socket

warnings.filterwarnings("ignore", category=RuntimeWarning)

def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass

def PandR(l, text):
    print(text)
    l.append(text + '  \n')
    return l
    
def sorterkey(line):
    year = line[7:11]
    month = line[12:14]
    day = line[15:17]
    time = line[22:27].replace('-', '')
    
    return (int(year), int(month), int(day), int(time))

def ticker(tick, temp):
    minTick = np.floor(np.min(temp) / tick) * tick
    maxTick = np.ceil(np.max(temp) / tick) * tick
    major = np.arange(minTick, maxTick, tick)
    minor = np.arange(minTick, maxTick, tick/2)
    
    return major, minor

def statistic():
    path = './json/'

    text_README = list()
    text_README.append('# Statistic  \n')
    text_README.append('Holiday: Holiday in Germany and Friday till Sunday  \n')
    
    flag = True
    files = []
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if not any(s in f for s in ['LOG', 'checkpoint', 'DS', 'edited']):
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
        try:
            f = open(file)
            jData = json.loads(f.read())
        except IndexError:
            print(file)

        s_date, s_time = jData['timestamp'].split('-', 1)
        date.append(s_date)
        weekday.append(dt.strptime(s_date, "%d.%m.%Y").weekday())

        if int(s_time[:2]) > 17:
            time.append('PM')
        else:
            time.append('AM')

        ratio.append(float(jData["ratio"]))

        total.append(float(jData["sum"]))

        try:
            bar.append(float(jData["bar"]))
        except ValueError:
            bar.append(jData["ratio"])

        try:
            card.append(float(jData["card"]))
        except ValueError:
            card.append(jData["ratio"])

        holiday.append(jData["holiday"])
        
        f.close()

    bar = list(filter(lambda item: item != 'None', bar))
    card = list(filter(lambda item: item != 'None', card))

    text_README.append('## Overview  \n')
    
    text_README = PandR(text_README, f'total: {np.mean(total):7.3f} +/- {np.std(total):6.3f}')
    text_README = PandR(text_README, f'ratio: {np.mean(ratio):7.3f} +/- {np.std(ratio):6.3f}')
    text_README = PandR(text_README, f'bar:   {np.mean(bar):7.3f} +/- {np.std(bar):6.3f}')
    text_README = PandR(text_README, f'card:  {np.mean(card):7.3f} +/- {np.std(card):6.3f}')

    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')


    print('top three: total')
    text_README.append('### Top three: total  \n')
    line = ' '*6 + 'total' + ' '*6 + 'ratio' + ' '*8 + 'timestamp'
    print(line)
    text_README.append('&nbsp;|total|ratio|timestamp\n')
    text_README.append('---|---|---|---\n')
    line = '-'*3 + '+' + '-'*9 + '+' + '-'*10 + '+' + '-'*18
    print(line)

    top = sorted(zip(total, ratio, date, time, holiday), reverse=True)[:3]
    for i in range(len(top)):
        wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
        print(f'{i+1}":  {float(top[i][0]):6.2f}€   {float(top[i][1]):5.3f}€/h   {top[i][2]:10} {wkday} {top[i][3]}')
        text_README.append(f'{i+1}":|{float(top[i][0]):6.2f}€|{float(top[i][1]):5.3f}€/h|{top[i][2]:10} {wkday} {top[i][3]}\n')
        print(f'{" "*5}holiday -> {top[i][4].capitalize()}')
        text_README.append(f'&nbsp;|&nbsp;|&nbsp;|holiday -> {top[i][4].capitalize()}\n')

    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')

    print('top three: ratio')
    text_README.append('### Top three: ratio  \n')
    line = ' '*6 + 'ratio' + ' '*6 + 'total' + ' '*8 + 'timestamp'
    print(line)
    text_README.append('&nbsp;|ratio|total|timestamp\n')
    text_README.append('---|---|---|---\n')
    line = '-'*3 + '+' + '-'*9 + '+' + '-'*10 + '+' + '-'*18
    print(line)

    top = sorted(zip(ratio, total, date, time, holiday), reverse=True)[:3]
    for i in range(len(top)):
        wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
        print(f'{i+1}": {float(top[i][0]):5.2f}€/h   {float(top[i][1]):6.3f}€   {top[i][2]:10} {wkday} {top[i][3]}')
        text_README.append(f'{i+1}":|{float(top[i][0]):5.2f}€/h|{float(top[i][1]):6.3f}€|{top[i][2]:10} {wkday} {top[i][3]}')
        print(f'{" "*5}holiday -> {top[i][4].capitalize()}')
        text_README.append(f'&nbsp;|&nbsp;|&nbsp;|holiday -> {top[i][4].capitalize()}\n')


    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')

    total = np.array(total)
    ratio = np.array(ratio)

    print('AM')
    text_README.append('### AM  \n')
    AM = [i == 'AM' for i in time]
    text_README = PandR(text_README, f'total: {np.mean(total[AM]):7.3f} +/- {np.std(total[AM]):6.3f}')
    text_README = PandR(text_README, f'ratio: {np.mean(ratio[AM]):7.3f} +/- {np.std(ratio[AM]):6.3f}')

    text_README = PandR(text_README, '')

    print('PM')
    text_README.append('### PM  \n')
    PM = [i == 'PM' for i in time]
    text_README = PandR(text_README, f'total: {np.mean(total[PM]):7.3f} +/- {np.std(total[PM]):6.3f}')
    text_README = PandR(text_README, f'ratio: {np.mean(ratio[PM]):7.3f} +/- {np.std(ratio[PM]):6.3f}')

    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')

    print('holidays with weekends (Fri - Sun)')
    text_README.append('### Holidays with weekends (Fri - Sun)  \n')
    mask = [i != 'False' for i in holiday]
    for i in range(len(weekday)):
        if 3 < weekday[i] < 7:
            mask[i] = True

    text_README = PandR(text_README, f'total: {np.mean(total[mask]):7.3f} +/- {np.std(total[mask]):6.3f}')
    text_README = PandR(text_README, f'ratio: {np.mean(ratio[mask]):7.3f} +/- {np.std(ratio[mask]):6.3f}')

    text_README = PandR(text_README, '')

    print('normal days')
    text_README.append('### Normal days  \n')
    mask = [not i for i in mask]
    text_README = PandR(text_README, f'total: {np.mean(total[mask]):7.3f} +/- {np.std(total[mask]):6.3f}')
    text_README = PandR(text_README, f'ratio: {np.mean(ratio[mask]):7.3f} +/- {np.std(ratio[mask]):6.3f}')

    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')

    for i in range(0, 7):
        text_README = PandR(text_README, calendar.day_name[i])

        mask = [n == i for n in weekday]
        text_README = PandR(text_README, f'total: {np.mean(total[mask]):7.3f} +/- {np.std(total[mask]):6.3f}')
        text_README = PandR(text_README, f'ratio: {np.mean(ratio[mask]):7.3f} +/- {np.std(ratio[mask]):6.3f}')

        text_README = PandR(text_README, '')

    text_README = PandR(text_README, '')

    print('frequency')
    text_README.append('### Frequency  \n')
    text_README = PandR(text_README, 'total: '+str(len(weekday))+', AM: '+str((np.array(time) == 'AM').sum())+', PM: '+str((np.array(time) == 'PM').sum()))

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

        text_README = PandR(text_README, s)

    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')

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
    
    
    text_README.append('## Plot  \n')
    text_README.append('![Image](harvest.png)')
    
    with open('./README.md', 'w') as f:
        f.writelines(text_README)

        
    git_update("'update plot'")