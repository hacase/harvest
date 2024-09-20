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

plt.rcParams.update({
    "text.usetex": True,
})

L_IGNORE = ['LOG', 'checkpoint', 'DS', 'edited', 'TextIOWrapper']
L_DICT = ['whole', 'half']
L_TORA = ['total', 'ratio']
AX_WEEKDAY = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
COLOR = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
PATH = './json/'
SP_DAY = 3
LTX_RATIO = '$/ \\frac{\\textup{€}}{\\textup{h}}$'
LTX_EURO = '$/$ €'
L_LTX = [LTX_EURO, LTX_RATIO]


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
            print('error opening:', file)

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
            d_return["bar"].append(None)

        try:
            d_return["card"].append(float(jData["card"]))
        except ValueError:
            d_return["card"].append(jData["ratio"])

        d_return["holiday"].append(jData["holiday"])
        
        f.close()

    d_return["bar"] = list(filter(lambda item: item != 'None', d_return["bar"]))
    d_return["card"] = list(filter(lambda item: item != 'None', d_return["card"]))

    return d_return


def txtmd(string):
    return string + '  \n'


text = list()

flag = True
files_whole = []
files_half = []

i = 0
for dirpath, dirnames, filenames in os.walk(PATH):
    for f in filenames:
        if not any(s in f for s in L_IGNORE):
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

text.append(txtmd('# Overview'))

text.append(txtmd('|| whole | half |'))
text.append(txtmd('|---|---|---|'))

for theme in ['total', 'ratio', 'bar', 'card']:
    if theme == 'bar':
        keyword = 'cash'
    else:
        keyword = theme

    if keyword == 'ratio':
        keyword += ' ' + LTX_RATIO
    else:
        keyword += ' ' + LTX_EURO
    row = '|' + keyword + '|'
    for d in d_all:
        if theme in ['card', 'bar']:
            d_temp = [i for i in d[theme] if i != 0]
        else:
            d_temp = d[theme]
            
        row += f'{np.mean(d_temp):6.3f} $\\pm$ {np.std(d_temp):6.3f}|'

    text.append(txtmd(row))


text = list()

text.append(txtmd('# Total / Ratio'))

table_title = ['||total '+LTX_EURO+'|ratio '+LTX_RATIO+'|timestamp|holiday|',
              '||ratio '+LTX_RATIO+'|total '+LTX_EURO+'|timestamp|holiday|']

for i_dict, d in enumerate(d_all):
    text.append(txtmd('## ' +L_DICT[i_dict].capitalize()+ ' day'))
    for i_table, title in enumerate(table_title):    
        text.append(txtmd(title))
        text.append(txtmd('|---|---|---|---|---|'))

        if i_table == 0:
            top = sorted(zip(d["total"], d["ratio"], d["date"], d["time"], d["holiday"]), reverse=True)[:3]
        else:
            top = sorted(zip(d["ratio"], d["total"], d["date"], d["time"], d["holiday"]), reverse=True)[:3]
            
        for j in range(3):
            wkday = dt.strptime(top[j][2], '%d.%m.%Y').strftime('%a')
            if top[j][4].capitalize() == 'False':
                temp_holiday = 'False'
            else:
                temp_holiday = top[j][4].capitalize()
    
            row = f'|{j+1}"|'
            row += f'{top[j][0]:6.2f}|'
            row += f'{top[j][1]:6.2f}|'
            row += f'{top[j][2]:10} {wkday} '
            row += f'{top[j][3]}|'
            row += f'{temp_holiday}|'
    
            text.append(txtmd(row))
    
        text.append(txtmd('  \n'))

    plt_weekday = [[[] for _ in range(7)] for _ in range(2)]
    for i, i_total in enumerate(d['total']):
        plt_weekday[0][d['weekday'][i]].append(float(i_total))

    for i, i_ratio in enumerate(d['ratio']):
        plt_weekday[1][d['weekday'][i]].append(float(i_ratio))

    fig, axis = plt.subplots(1, 2, figsize=(8, 5))

    fig.suptitle(L_DICT[i_dict].capitalize()+ ' day')
    for i_ax, ax in enumerate(axis):
        ax.set_title(L_TORA[i_ax].capitalize())
        ax.boxplot(plt_weekday[i_ax])
        plt.sca(ax)
        plt.xticks(range(8), AX_WEEKDAY, rotation=45)
        if i_ax == 0:
            plt.ylabel(r'€')
            if i_dict == 0:
                tick = 50
            else:
                tick = 25
        else:
            plt.ylabel(r'$\displaystyle\frac{\textup{€}}{\textup{h}}$')
            tick = .5
        major, minor = ticker(tick, [item for row in plt_weekday[i_ax] for item in row])
        plt.grid(axis = 'y', which = 'major', alpha = 0.7)
        plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
        ax.set_yticks(major)
        ax.set_yticks(minor, minor = True)
        for i in range(7):
            ax.plot(np.ones(len(plt_weekday[i_ax][i])) *i +1, plt_weekday[i_ax][i], ms=4, marker='o', mew=0.5, ls="none", color=COLOR[i])
        ax.violinplot(plt_weekday[i_ax], positions=range(1, 8), showextrema=False)

    fig.tight_layout()

    png_name = './png/total_ratio_'+L_DICT[i_dict]+'.png'
    plt.savefig(png_name, dpi=300)
    text.append(txtmd('  '))
    text.append(txtmd('![Image](' + png_name + ')'))

    
    text.append(txtmd('# Weekday'))
    text.append(txtmd('|||whole|half|'))
    text.append(txtmd('|---|---|---|---|'))
    for i in range(7):
        row = f'|{calendar.day_name[i]}|'
        for i_key, key in enumerate(L_TORA):
            row += f'{key} {L_LTX[i_key]}|'
            for i_dict, d in enumerate(d_all):
                mask = [n == i for n in d['weekday']]
                
                row += f'{np.mean(np.array(d[key])[mask]):6.2f}'
                row += f' $\\pm$'
                row += f'{np.std(np.array(d[key])[mask]):6.2f}|'
        
            text.append(txtmd(row))
            row = '||'

# with open('./README.md', 'w') as f:
#     f.writelines(text)

# print('done')