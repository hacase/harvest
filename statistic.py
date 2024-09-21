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

from harvest_func import Loader, abort, git_update


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
LTX_EURO = '$/ \\textup{€}$'
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
            print(file)

        s_date, s_time = jData['timestamp'].split('-', 1)
        d_return["date"].append(dt.strptime(s_date, "%d.%m.%Y"))
        d_return["weekday"].append(dt.strptime(s_date, "%d.%m.%Y").weekday())

        if int(s_time[:2]) >= 18:
            d_return["time"].append('PM')
        else:
            d_return["time"].append('AM')

        d_return["hour"].append(jData["hour"])
        
        d_return["ratio"].append(float(jData["ratio"]))

        d_return["total"].append(float(jData["sum"]))

        if jData["bar"]:
            try:
                d_return["bar"].append(float(jData["bar"]))
            except ValueError:
                d_return["bar"].append(False)
        else:
            d_return["bar"].append(False)

        if jData["card"]:
            try:
                d_return["card"].append(float(jData["card"]))
            except:
                d_return["card"].append(False)
        else:
            d_return["card"].append(False)

        d_return["holiday"].append(jData["holiday"])
        
        f.close()

    return d_return


def pseudo(d_whole, d_half):
    part_ampm = [[] for _ in range(2)]
    part_whole = []
    
    for i_whole, whole in enumerate(d_whole['date']):
        match = [index for index, half in enumerate(d_half['date']) if whole.date() == half.date()]
        if len(match) == 1:
            ampm = ['PM', 'AM'].index(d_half['time'][match[0]])
            part = [[] for _ in range(3)]
            
            for i_tora, tora in enumerate(L_TORA + ['hour']):
                part[i_tora] = d_half[tora][match[0]]
    
            total = d_whole['total'][i_whole] - float(part[0])
            hour = sum(d_whole['hour'][i_whole]) - sum(part[2])
    
            ratio = total / hour
    
            row = [total, ratio]
            part_ampm[ampm].append(row + [whole, d_whole['holiday'][i_whole]])
    
    
    for i_half, half in enumerate(d_half['date']):
        prematch = [(i_half, index + i_half + 1) for index, half_b in enumerate(d_half['date'][i_half + 1:]) if half_b.date() == half.date()]
        if len(prematch) == 1:
            i_prematch = prematch[0][0]
            date = d_half['date'][i_prematch]
            part = np.zeros(3)
    
            match = [whole.date() == date.date() for index, whole in enumerate(d_whole['date'])]
            if any(match):
                for i_index in range(2):
                    part[0] += float(d_half['total'][prematch[0][i_index]])
                    part[2] += sum(d_half['hour'][prematch[0][i_index]])
    
                ratio = part[0] / part[2]
        
                row = [part[0], ratio]
                part_whole.append(row + [d_half['date'][i_prematch], d_half['holiday'][i_prematch]])

    return part_whole, part_ampm


def txtmd(string):
    return string + '  \n'


def statistic():
    loader = Loader('updating statistic', 'update statistic done.').start()
    
    text = list()

    date_now = dt.today().strftime("%d.%m.%Y, %A, time: %H:%M")
    text.append(txtmd('last update: ' + date_now))
    
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
                d_temp = list(filter(lambda item: item != 'None', d[theme]))
            else:
                d_temp = d[theme]
    
            row += f'{np.mean(d_temp):6.3f} $\\pm$ {np.std(d_temp):6.3f}|'
    
        text.append(txtmd(row))
    
    
    text.append(txtmd('# Frequency'))
    
    weekday = np.zeros(7)
    for i_dict, d in enumerate(d_all):
        for day in d['weekday']:
            weekday[day] += 1
    
    pct = weekday / float(sum(weekday)) * 100

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(weekday,
                                      labels=list(calendar.day_name),
                                      autopct='',
                                      colors=COLOR,
                                      startangle=90,
                                      textprops=dict(color="black"))
    
    for i, a in enumerate(autotexts):
        a.set_text("{:.1f}%\n{}".format(pct[i], int(weekday[i])))
    
    ax.set_title("Frequency")
    
    fig.tight_layout()
    
    png_name = './png/frequency.png'
    plt.savefig(png_name, dpi=300)
    text.append(txtmd('  '))
    text.append(txtmd('![Image](' + png_name + ')'))
    
    
    part_whole, part_ampm = pseudo(d_whole, d_half)
    
    for d in part_whole:
        d_whole['total'].append(d[0])
        d_whole['ratio'].append(d[1])
        d_whole['date'].append(d[2])
        d_whole['weekday'].append(d[2].weekday())
        d_whole['holiday'].append(d[3])
        d_whole['time'].append(False)
        d_whole['hour'].append(False)
        d_whole['bar'].append(False)
        d_whole['card'].append(False)
    
    for i_part, part in enumerate(part_ampm):
        ampm = ['AM', 'PM'][i_part]
        for p in part:
            d_half['total'].append(p[0])
            d_half['ratio'].append(p[1])
            d_half['date'].append(p[2])
            d_half['weekday'].append(p[2].weekday())
            d_half['holiday'].append(p[3])
            d_half['time'].append(ampm)
            d_half['hour'].append(False)
            d_half['bar'].append(False)
            d_half['card'].append(False)
    
    
    text.append(txtmd('# Total / Ratio'))
    
    table_title = ['||total '+LTX_EURO+'|ratio '+LTX_RATIO+'|timestamp|holiday|',
                  '||ratio '+LTX_RATIO+'|total '+LTX_EURO+'|timestamp|holiday|']
    
    for i_dict, d in enumerate(d_all):
        text.append(txtmd('## ' +L_DICT[i_dict].capitalize()+ ' day'))
        for i_table, title in enumerate(table_title):    
            text.append(txtmd(title))
            text.append(txtmd('|---|---|---|---|---|'))
    
            if i_table == 0:
                top = sorted(zip(d["total"], d["ratio"], d["date"], d["time"], d["weekday"], d["holiday"]), reverse=True)[:3]
            else:
                top = sorted(zip(d["ratio"], d["total"], d["date"], d["time"], d["weekday"], d["holiday"]), reverse=True)[:3]
                
            for j in range(3):    
                row = f'|{j+1}"|'
                row += f'{top[j][0]:6.2f}|'
                row += f'{top[j][1]:6.2f}|'
                row += f'{top[j][2].strftime("%d.%m.%Y"):10} {AX_WEEKDAY[top[j][4]+1][:3]} '
                row += f'{top[j][3]}|'
                row += f'{top[j][5].capitalize()}|'
        
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
                plt.ylabel(r'\textup{€}')
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
            ax.violinplot(plt_weekday[i_ax], positions=range(1, 8), showextrema=False, showmeans=True)
    
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
    
    
    text.append(txtmd('# Make me feel Special'))
    text.append(txtmd('Special: Holidays and Weekends'))
    for i_dict, d in enumerate(d_all):
        plt_set = []
    
        text.append(txtmd('## ' +L_DICT[i_dict].capitalize()+ ' day'))
    
        fig, axs = plt.subplots(1, 2, figsize=(8, 5))
        fig.suptitle(L_DICT[i_dict].capitalize()+ ' day')
        every = [[] for _ in range(2)]
        normal = [[] for _ in range(2)]
        weekend = [[] for _ in range(2)]
        holiday = [[] for _ in range(2)]
        special = [[] for _ in range(2)]
        special_f = [[] for _ in range(2)]
    
        axs_descr = ['All',
                    'Normal',
                    'Weekend',
                    'Holiday',
                    'Special',
                    'Special\&Friday']
    
    
        for i_key, key in enumerate(L_TORA):
            every[i_key] = d[key]
    
            for i, i_day in enumerate(d['weekday']):
                if 4 < i_day < 7:
                    weekend[i_key].append(d[key][i])
                else:
                    normal[i_key].append(d[key][i])
    
            mask_h = [i.lower() not in ['false', 'offline'] for i in d['holiday']]
            holiday[i_key] = np.array(d[key])[mask_h]
    
            mask_sp = [4 < i < 7 for i in d['weekday']]
            mask_sp = [h or sp for h, sp in zip(mask_h, mask_sp)]
            special[i_key] = np.array(d[key])[mask_sp]
    
            mask_sp = [3 < i < 7 for i in d['weekday']]
            mask_sp = [h or sp for h, sp in zip(mask_h, mask_sp)]
            special_f[i_key] = np.array(d[key])[mask_sp]
    
            plt_special = [every[i_key],
                           normal[i_key],
                           weekend[i_key],
                           holiday[i_key],
                           special[i_key],
                           special_f[i_key]]
            
            plt_set.append(plt_special)
    
            axs[i_key].set_title(key.capitalize())
            axs[i_key].boxplot(plt_special)
            plt.sca(axs[i_key])
            plt.xticks(range(7), [''] + axs_descr, rotation=45)
            if i_key == 0:
                plt.ylabel(r'$\textup{€}$')
                if i_dict == 0:
                    tick = 50
                else:
                    tick = 25
            else:
                plt.ylabel(r'$\displaystyle\frac{\textup{€}}{\textup{h}}$')
                tick = .5
            major, minor = ticker(tick, [item for row in plt_special for item in row])
            plt.grid(axis = 'y', which = 'major', alpha = 0.7)
            plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
            axs[i_key].set_yticks(major)
            axs[i_key].set_yticks(minor, minor = True)
            for i in range(6):
                axs[i_key].plot(np.ones(len(plt_special[i])) *i +1, plt_special[i], ms=4, marker='o', mew=0.5, ls="none", color=COLOR[i])
            axs[i_key].violinplot(plt_special, positions=range(1, 7), showextrema=False, showmeans=True)
    
        text.append(txtmd('||total '+LTX_EURO+'|ratio '+LTX_RATIO+'|count|'))
        text.append(txtmd('|---|---|---|---|'))
        
        for i in range(len(plt_special)):
            row = '|' + axs_descr[i] + '|'
            for j in range(2):
                row += f'{np.mean(plt_set[j][i]):6.2f}'
                row += f' $\\pm$'
                row += f'{np.std(plt_set[j][i]):6.2f}|'
    
            row += f'{len(plt_special[i])}'
            text.append(txtmd(row))
    
        fig.tight_layout()
        
        png_name = './png/special_'+L_DICT[i_dict]+'.png'
        plt.savefig(png_name, dpi=300)
        text.append(txtmd('  '))
        text.append(txtmd('![Image](' + png_name + ')'))
    
    
    text.append(txtmd('# AM / PM'))
    
    d_am = {key: [] for key in d_half.keys()}
    d_pm = {key: [] for key in d_half.keys()}
    d_ampm = [d_am, d_pm]
    
    
    for i_dict, d in enumerate(d_half['time']):
        ampm = ['AM', 'PM'].index(d)
        for i_key, key in enumerate(d_half.keys()):
            d_ampm[ampm][key].append(d_half[key][i_dict])
    
    
    
    for i_dict, d in enumerate(d_ampm):
        text.append(txtmd('## ' + ['AM', 'PM'][i_dict]))
        plt_set = []
    
        fig, axs = plt.subplots(1, 2, figsize=(8, 5))
        fig.suptitle(['AM', 'PM'][i_dict])
        every = [[] for _ in range(2)]
        normal = [[] for _ in range(2)]
        weekend = [[] for _ in range(2)]
        holiday = [[] for _ in range(2)]
        special = [[] for _ in range(2)]
        special_f = [[] for _ in range(2)]
    
        axs_descr = ['All',
                    'Normal',
                    'Weekend',
                    'Holiday',
                    'Special',
                    'Special\&Friday']
    
    
        for i_key, key in enumerate(L_TORA):
            every[i_key] = d[key]
            for i_day, day in enumerate(d['weekday']):
                if 4 < day < 7:
                    weekend[i_key].append(d[key][i_day])
                else:
                    normal[i_key].append(d[key][i_day])
    
            mask_h = [i.lower() not in ['false', 'offline'] for i in d['holiday']]
            holiday[i_key] = np.array(d[key])[mask_h]
    
            mask_sp = [4 < i < 7 for i in d['weekday']]
            mask_sp = [h or sp for h, sp in zip(mask_h, mask_sp)]
            special[i_key] = np.array(d[key])[mask_sp]
    
            mask_sp = [3 < i < 7 for i in d['weekday']]
            mask_sp = [h or sp for h, sp in zip(mask_h, mask_sp)]
            special_f[i_key] = np.array(d[key])[mask_sp]
    
            plt_special = [every[i_key],
                           normal[i_key],
                           weekend[i_key],
                           holiday[i_key],
                           special[i_key],
                           special_f[i_key]]
            
            plt_set.append(plt_special)
    
            axs[i_key].set_title(key.capitalize())
            axs[i_key].boxplot(plt_special)
            plt.sca(axs[i_key])
            plt.xticks(range(7), [''] + axs_descr, rotation=45)
            if i_key == 0:
                plt.ylabel(r'$\textup{€}$')
                if i_dict == 0:
                    tick = 50
                else:
                    tick = 25
            else:
                plt.ylabel(r'$\displaystyle\frac{\textup{€}}{\textup{h}}$')
                tick = .5
            major, minor = ticker(tick, [item for row in plt_special for item in row])
            plt.grid(axis = 'y', which = 'major', alpha = 0.7)
            plt.grid(axis = 'y', which = 'minor', alpha = 0.3)
            axs[i_key].set_yticks(major)
            axs[i_key].set_yticks(minor, minor = True)
            for i in range(6):
                axs[i_key].plot(np.ones(len(plt_special[i])) *i +1, plt_special[i], ms=4, marker='o', mew=0.5, ls="none", color=COLOR[i])
            axs[i_key].violinplot(plt_special, positions=range(1, 7), showextrema=False, showmeans=True)
    
        text.append(txtmd('||total '+LTX_EURO+'|ratio '+LTX_RATIO+'|count|'))
        text.append(txtmd('|---|---|---|---|'))
        
        for i in range(len(plt_special)):
            row = '|' + axs_descr[i] + '|'
            for j in range(2):
                row += f'{np.mean(plt_set[j][i]):6.2f}'
                row += f' $\\pm$'
                row += f'{np.std(plt_set[j][i]):6.2f}|'
    
            row += f'{len(plt_special[i])}'
            text.append(txtmd(row))
    
    
        fig.tight_layout()
        
        png_name = './png/'+['AM', 'PM'][i_dict]+'.png'
        plt.savefig(png_name, dpi=300)
        text.append(txtmd('  '))
        text.append(txtmd('![Image](' + png_name + ')'))
    
    
    with open('./README.md', 'w') as f:
        f.writelines(text)

    loader.stop()

    git_update()
