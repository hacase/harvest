 #!/usr/bin/env python

import numpy as np
import os
from datetime import datetime as dt
import calendar
import warnings
import subprocess
import json
from urllib import request
import socket
import matplotlib.pyplot as plt

from harvest_func import abort, git_update, fcalctip, is_connected



warnings.filterwarnings("ignore", category=RuntimeWarning)

l_ignore = ['LOG', 'checkpoint', 'DS', 'edited', 'TextIOWrapper']


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


def calculate_statistic(files):
    d_return = {
        "date": [],
        "weekday": [],
        "time": [],
        "hour": [],
        "ratio": [],
        "total": [],
        "bar": [],
        "card": [],
        "holiday": [],
    }
    for file in files:
        try:
            f = open(file)
            jData = json.loads(f.read())
        except IndexError:
            print(file)

        s_date, s_time = jData['timestamp'].split('-', 1)
        d_return["date"].append(s_date)
        d_return["weekday"].append(dt.strptime(s_date, "%d.%m.%Y").weekday())

        if int(s_time[:2]) > 17:
            d_return["time"].append('PM')
        else:
            d_return["time"].append('AM')

        d_return["hour"].append(jData["hour"])
        
        d_return["ratio"].append(float(jData["ratio"]))

        d_return["total"].append(float(jData["sum"]))

        try:
            d_return["bar"].append(float(jData["bar"]))
        except ValueError:
            d_return["bar"].append(jData["ratio"])

        try:
            d_return["card"].append(float(jData["card"]))
        except ValueError:
            d_return["card"].append(jData["ratio"])

        d_return["holiday"].append(jData["holiday"])
        
        f.close()

    d_return["bar"] = list(filter(lambda item: item != 'None', d_return["bar"]))
    d_return["card"] = list(filter(lambda item: item != 'None', d_return["card"]))

    return d_return


def statistic():
    path = './json/'
    
    text_README = list()
    text_README.append('last update: ' + dt.today().strftime("%d.%m.%Y, %A, time: %H:%M") + '\n')
    text_README.append('# Statistic  \n')
    text_README.append('Special: Holiday in Germany NRW and Friday until Sunday  \n')
    text_README.append('Currency is in Euro, ratio is in €/h  \n')
    
    flag = True
    files_whole = []
    files_half = []
    l_dict = ['whole', 'half']
    
    i = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if not any(s in f for s in l_ignore):
                if 'whole' in f.lower():
                    files_whole.append(os.path.join(dirpath, f))
                else:
                    files_half.append(os.path.join(dirpath, f))
                    
                flag = False
    
    files_whole = sorted(files_whole, key=sorterkey)
    files_half = sorted(files_half, key=sorterkey)
    
    d_whole = calculate_statistic(files_whole)
    d_half = calculate_statistic(files_half)
    d_all = [d_whole, d_half]
    
    
    print('# OVERVIEW')
    text_README.append('## Overview  \n')
    text_README = PandR(text_README, f'{" "*15}whole{" "*7} {" "*8}half')
    text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    
    temp_res = ''
    for d in d_all:
        temp_res += f'{np.mean(d["total"]):7.3f} +/- {np.std(d["total"]):6.3f}'
        if d != d_all[-1]:
            temp_res += '   '
    text_README = PandR(text_README, f'total   {temp_res}')
    
    temp_res = ''
    for d in d_all:
        temp_res += f'{np.mean(d["ratio"]):7.3f} +/- {np.std(d["ratio"]):6.3f}'
        if d != d_all[-1]:
            temp_res += '   '
    text_README = PandR(text_README, f'ratio   {temp_res}')
    
    temp_res = ''
    for d in d_all:
        l_temp = [i for i in d["bar"] if i != 0]
        temp_res += f'{np.mean(l_temp):7.3f} +/- {np.std(l_temp):6.3f}'
        if d != d_all[-1]:
            temp_res += '   '
    text_README = PandR(text_README, f'bar     {temp_res}')
    
    temp_res = ''
    for d in d_all:
        l_temp = [i for i in d["card"] if i != 0]
        temp_res += f'{np.mean(l_temp):7.3f} +/- {np.std(l_temp):6.3f}'
        if d != d_all[-1]:
            temp_res += '   '
    text_README = PandR(text_README, f'card    {temp_res}')
    
    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')
    
    
    print('# TOP THREE')
    text_README.append('## Top three  \n')
    
    print('-# TOTAL')
    text_README.append('### Total  \n')
    line = ' '*6 + 'total' + ' '*3 + 'ratio' + ' '*10 + 'timestamp'
    print(line)
    text_README.append('&nbsp;|total|ratio|timestamp\n')
    text_README.append('---|---|---|---\n')
    
    line = '-'*3 + '+' + '-'*8 + '+' + '-'*7 + '+' + '-'*27
    for index, d in enumerate(d_all):
        print(line)
        print(f'   {l_dict[index].upper()} DAY')
        print(line)
        
        top = sorted(zip(d["total"], d["ratio"], d["date"], d["time"], d["holiday"]), reverse=True)[:3]
        for i in range(len(top)):
            wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
            if top[i][4].lower() == 'true':
                temp_holiday = 'holiday'
            else:
                temp_holiday = 'normal'
                
            print(f'{i+1}"   {float(top[i][0]):6.2f}   {float(top[i][1]):5.3f}   {top[i][2]:10} {wkday} {top[i][3]} {temp_holiday}')
            text_README.append(f'{i+1}":|{float(top[i][0]):6.2f}€|{float(top[i][1]):5.3f}€/h|{top[i][2]:10} {wkday} {top[i][3]}\n')
    
    text_README = PandR(text_README, '')
    
    print('-# RATIO')
    text_README.append('### Ratio  \n')
    line = ' '*5 + 'ratio' + ' '*4 + 'total' + ' '*10 + 'timestamp'
    print(line)
    text_README.append('&nbsp;|ratio|total|timestamp\n')
    text_README.append('---|---|---|---\n')
    
    line = '-'*3 + '+' + '-'*7 + '+' + '-'*8 + '+' + '-'*27
    for index, d in enumerate(d_all):
        print(line)
        print(f'   {l_dict[index].upper()} DAY')
        print(line)
        
        top = sorted(zip(d["ratio"], d["total"], d["date"], d["time"], d["holiday"]), reverse=True)[:3]
        for i in range(len(top)):
            wkday = dt.strptime(top[i][2], '%d.%m.%Y').strftime('%a')
            if top[i][4].lower() == 'true':
                temp_holiday = 'holiday'
            else:
                temp_holiday = 'normal'
                
            print(f'{i+1}"   {float(top[i][0]):5.3f}   {float(top[i][1]):6.2f}   {top[i][2]:10} {wkday} {top[i][3]} {temp_holiday}')
            text_README.append(f'{i+1}":|{float(top[i][0]):6.2f}€|{float(top[i][1]):5.3f}€/h|{top[i][2]:10} {wkday} {top[i][3]}\n')
    
    
    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')
    
    
    whole_total = np.array(d_whole["total"])
    whole_ratio = np.array(d_whole["ratio"])
    
    half_total = np.array(d_half["total"])
    half_ratio = np.array(d_half["ratio"])
    
    
    print('# NORMAL TO SPECIAL')
    text_README.append('## Normal to Special  \n')
    
    whole_mask = [i.lower() != 'false' for i in d_whole["holiday"]]
    for i in range(len(d_whole["weekday"])):
        if 3 < d_whole["weekday"][i] < 7:
            whole_mask[i] = True
    
    half_mask = [i.lower() != 'false' for i in d_half["holiday"]]
    for i in range(len(d_half["weekday"])):
        if 3 < d_half["weekday"][i] < 7:
            half_mask[i] = True
    
    
    text_README = PandR(text_README, f'{" "*15}whole{" "*7} {" "*8}half')
    
    text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    print('   NORMAL DAY')
    text_README.append('### Normal day  \n')
    text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    
    whole_mask = [not i for i in whole_mask]
    half_mask = [not i for i in half_mask]
    
    temp_total = f'{np.mean(whole_total[whole_mask]):7.3f} +/- {np.std(whole_total[whole_mask]):6.3f}   '
    temp_ratio = f'{np.mean(whole_ratio[whole_mask]):7.3f} +/- {np.std(whole_ratio[whole_mask]):6.3f}   '
    
    temp_total += f'{np.mean(half_total[half_mask]):7.3f} +/- {np.std(half_total[half_mask]):6.3f}'
    temp_ratio += f'{np.mean(half_ratio[half_mask]):7.3f} +/- {np.std(half_ratio[half_mask]):6.3f}'
    
    text_README = PandR(text_README, f'total   {temp_total}')
    text_README = PandR(text_README, f'ratio   {temp_ratio}')
    
    text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    print('   SPECIAL DAY')
    text_README.append('### Special day  \n')
    text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    
    
    whole_mask = [not i for i in whole_mask]
    half_mask = [not i for i in half_mask]
    
    temp_total = f'{np.mean(whole_total[whole_mask]):7.3f} +/- {np.std(whole_total[whole_mask]):6.3f}   '
    temp_ratio = f'{np.mean(whole_ratio[whole_mask]):7.3f} +/- {np.std(whole_ratio[whole_mask]):6.3f}   '
    
    temp_total += f'{np.mean(half_total[half_mask]):7.3f} +/- {np.std(half_total[half_mask]):6.3f}'
    temp_ratio += f'{np.mean(half_ratio[half_mask]):7.3f} +/- {np.std(half_ratio[half_mask]):6.3f}'
    
    text_README = PandR(text_README, f'total   {temp_total}')
    text_README = PandR(text_README, f'ratio   {temp_ratio}')
    
    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')
    
    
    print('# WEEKDAY')
    text_README.append('## Weekday  \n')
    
    text_README = PandR(text_README, f'{" "*15}whole{" "*7} {" "*8}half')
    for i in range(0, 7):
        text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
        print('  ', calendar.day_name[i].upper())
        text_README.append(f'### {calendar.day_name[i]}  \n')
    
        whole_mask = [n == i for n in d_whole["weekday"]]
        half_mask = [n == i for n in d_half["weekday"]]
    
        temp_total = f'{np.mean(whole_total[whole_mask]):7.3f} +/- {np.std(whole_total[whole_mask]):6.3f}   '
        temp_ratio = f'{np.mean(whole_ratio[whole_mask]):7.3f} +/- {np.std(whole_ratio[whole_mask]):6.3f}   '
    
        temp_total += f'{np.mean(half_total[half_mask]):7.3f} +/- {np.std(half_total[half_mask]):6.3f}'
        temp_ratio += f'{np.mean(half_ratio[half_mask]):7.3f} +/- {np.std(half_ratio[half_mask]):6.3f}'
    
        text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    
        text_README = PandR(text_README, f'total:  {temp_total}')
        text_README = PandR(text_README, f'ratio:  {temp_ratio}')
    
    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')
    
    
    print('# HALF DAY')
    text_README.append('## Half day  \n')
    
    print('-# AM TO PM')
    text_README.append('### AM to PM  \n')
    
    AM = [i == 'AM' for i in d["time"]]
    temp_total = f'{np.mean(half_total[AM]):7.3f} +/- {np.std(half_total[AM]):6.3f}   '
    temp_ratio = f'{np.mean(half_ratio[AM]):7.3f} +/- {np.std(half_ratio[AM]):6.3f}   '
    
    PM = [i == 'PM' for i in d["time"]]
    temp_total += f'{np.mean(half_total[PM]):7.3f} +/- {np.std(half_total[PM]):6.3f}'
    temp_ratio += f'{np.mean(half_ratio[PM]):7.3f} +/- {np.std(half_ratio[PM]):6.3f}'
    
    text_README = PandR(text_README, f'{" "*17}AM{" "*9} {" "*9}PM')
    text_README = PandR(text_README, f'{"-"*6}+{"-"*20}+{"-"*20}')
    
    text_README = PandR(text_README, f'total   {temp_total}')
    text_README = PandR(text_README, f'ratio   {temp_ratio}')
    
    text_README = PandR(text_README, '')
    
    print('-# FREQUENCY')
    text_README.append('### Frequency  \n')
    text_README = PandR(text_README, 'total: '+str(len(d_half["weekday"]))+', AM: '+str((np.array(d_half["time"]) == 'AM').sum())+', PM: '+str((np.array(d_half["time"]) == 'PM').sum()))
    
    def chunker(part, full):
        chunks, remain = divmod(int(part * 8 / full * 100), 8)
        bar = '█' * chunks
    
        if remain > 0:
            bar += chr(ord('█') + (8 - remain))
    
        return bar
    
    for i in range(7):
        day = (np.array(d_half["weekday"]) == i).sum()
        s = chunker(day, len(d_half["weekday"]))
        s += f'{(np.array(d_half["weekday"]) == i).sum():3}, '
        s += f'{(np.array(d_half["weekday"]) == i).sum() / len(d_half["weekday"])*100:3.1f}%'
    
        text_README = PandR(text_README, s)
    
    text_README = PandR(text_README, '')
    text_README = PandR(text_README, '')
        
    
    Ptime = [[] for _ in range(4)]
    Ptotal = [[] for _ in range(7)]
    
    Rtime = [[] for _ in range(4)]
    Rtotal = [[] for _ in range(7)]
    
    time = d_half['time']
    holiday = d_half['holiday']
    weekday = d_half['weekday']
    total = d_half['total']
    ratio = d_half['ratio']
    
    AM = [i == 'AM' for i in time]
    
    ferien = [i.lower() != 'false' for i in holiday]
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
            Ptime[3].append(total[i])
            Rtime[3].append(ratio[i])
        else:
            Ptime[2].append(total[i])
            Rtime[2].append(ratio[i])
    
        total[i] = float(total[i])
    
        Ptotal[weekday[i]].append(total[i])
        Rtotal[weekday[i]].append(ratio[i])
    
    c = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
    
    
    fig, axs = plt.subplots(4, 2, figsize=(8,20))
    
    axs[0, 0].set_title('half day, total')
    axs[0, 0].boxplot(Ptime)
    plt.sca(axs[0, 0])
    plt.xticks(range(5), ['', 'AM', 'PM', 'normal', 'special'], rotation=45)
    plt.ylabel('€')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Ptime for item in row]
    major, minor = ticker(20, temp)
    axs[0, 0].set_yticks(major)
    axs[0, 0].set_yticks(minor, minor = True)
    for i in range(4):
        axs[0, 0].plot(np.ones(len(Ptime[i])) *i +1, Ptime[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[0, 0].violinplot(Ptime, positions=range(1, 5), showextrema=False)
    
    
    axs[1, 0].set_title('half day, ratio')
    axs[1, 0].boxplot(Rtime)
    plt.sca(axs[1, 0])
    plt.xticks(range(5), ['', 'AM', 'PM', 'normal', 'special'], rotation=45)
    plt.ylabel('€/h')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Rtime for item in row]
    major, minor = ticker(1, temp)
    axs[1, 0].set_yticks(major)
    axs[1, 0].set_yticks(minor, minor = True)
    for i in range(4):
        axs[1, 0].plot(np.ones(len(Rtime[i])) *i +1, Rtime[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[1, 0].violinplot(Rtime, positions=range(1, 5), showextrema=False)
    
    
    axs[0, 1].set_title('half day, total')
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
    for i in range(7):
        axs[0, 1].plot(np.ones(len(Ptotal[i])) *i +1, Ptotal[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[0, 1].violinplot(Ptotal, positions=range(1, 8), showextrema=False)
    
    
    axs[1, 1].set_title('half day, ratio')
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
    axs[1, 1].violinplot(Rtotal, positions=range(1, 8), showextrema=False)
    
    
    
    
    Ptime = [[] for _ in range(2)]
    Ptotal = [[] for _ in range(7)]
    
    Rtime = [[] for _ in range(2)]
    Rtotal = [[] for _ in range(7)]
    
    time = d_whole['time']
    holiday = d_whole['holiday']
    weekday = d_whole['weekday']
    total = d_whole['total']
    ratio = d_whole['ratio']
    
    ferien = [i.lower() != 'false' for i in holiday]
    for i in range(len(weekday)):
            if 3 < weekday[i] < 7:
                ferien[i] = True
    
    for i in range(len(total)):
        if ferien[i]:
            Ptime[1].append(total[i])
            Rtime[1].append(ratio[i])
        else:
            Ptime[0].append(total[i])
            Rtime[0].append(ratio[i])
    
        total[i] = float(total[i])
    
        Ptotal[weekday[i]].append(total[i])
        Rtotal[weekday[i]].append(ratio[i])
    
    
    axs[2, 0].set_title('whole day, total')
    axs[2, 0].boxplot(Ptime)
    plt.sca(axs[2, 0])
    plt.xticks(range(3), ['',  'normal', 'special'], rotation=45)
    plt.ylabel('€')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Ptime for item in row]
    major, minor = ticker(40, temp)
    axs[2, 0].set_yticks(major)
    axs[2, 0].set_yticks(minor, minor = True)
    for i in range(2):
        axs[2, 0].plot(np.ones(len(Ptime[i])) *i +1, Ptime[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[2, 0].violinplot(Ptime, positions=range(1, 3), showextrema=False)
    
    
    axs[3, 0].set_title('whole day, ratio')
    axs[3, 0].boxplot(Rtime)
    plt.sca(axs[3, 0])
    plt.xticks(range(3), ['',  'normal', 'special'], rotation=45)
    plt.ylabel('€/h')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Rtime for item in row]
    major, minor = ticker(.5, temp)
    axs[3, 0].set_yticks(major)
    axs[3, 0].set_yticks(minor, minor = True)
    for i in range(2):
        axs[3, 0].plot(np.ones(len(Rtime[i])) *i +1, Rtime[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[3, 0].violinplot(Rtime, positions=range(1, 3), showextrema=False)
    
    
    axs[2, 1].set_title('whole day, total')
    axs[2, 1].boxplot(Ptotal)
    plt.sca(axs[2, 1])
    plt.xticks(np.arange(8), ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    plt.ylabel('€')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Ptotal for item in row]
    major, minor = ticker(40, temp)
    axs[2, 1].set_yticks(major)
    axs[2, 1].set_yticks(minor, minor = True)
    for i in range(7):
        axs[2, 1].plot(np.ones(len(Ptotal[i])) *i +1, Ptotal[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[2, 1].violinplot(Ptotal, positions=range(1, 8), showextrema=False)
    
    
    axs[3, 1].set_title('whole day, ratio')
    axs[3, 1].boxplot(Rtotal)
    plt.sca(axs[3, 1])
    plt.xticks(np.arange(8), ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    plt.ylabel('€/h')
    plt.grid(axis = 'y', which = 'major', alpha = 0.7)
    plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
    temp = [item for row in Rtotal for item in row]
    major, minor = ticker(.5, temp)
    axs[3, 1].set_yticks(major)
    axs[3, 1].set_yticks(minor, minor = True)
    for i in range(7):
        axs[3, 1].plot(np.ones(len(Rtotal[i])) *i +1, Rtotal[i], ms=4, marker='o', mew=0.5, ls="none", color=c[i])
    axs[3, 1].violinplot(Rtotal, positions=range(1, 8), showextrema=False)
    
    
    fig.tight_layout()
    plt.savefig('harvest.png', dpi=300)
    
    
    text_README.append('## Plot  \n')
    text_README.append('![Image](harvest.png)')
    
    with open('./README.md', 'w') as f:
        f.writelines(text_README)
        

    show_plot = abort(input('show plot? [/y]: '))
    
    if show_plot == 'android':
        subprocess.call('termux-open harvest.png', shell=True)

    elif show_plot:
        plt.show()


    print('presenting plots done.')

        
    git_update("'update plot'")