 #!/usr/bin/env python
# Wrtten by Taro Watanabe, would be nice if you take the code
# with the eastereggs secret, addings are allowed ^^
# all texts and eastereggs stored in texts.py

import numpy as np
import sys
import os
from datetime import datetime as dt
import texts as tx
import report as rp
import subprocess


def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    lhelp = ['help', 'hilfe']
    lcorr = ['korr', 'korrektur', 'korektur', 'korrigieren',
            'korigieren', 'correction', 'corection', 'corr',
            'korrection', 'korection', 'corrigieren', 'corigieren']
    
    if var in labort:
        print('Exited session.')
        sys.exit()
        
    elif var in lhelp:
        tx.helpman()
        sys.exit()
        
    elif var in lcorr:
        print(name)
        
    else:
        return var
    
def adjust_tip(roundtip, tipsum, real):
    if np.around(sum(roundtip), decimals=3) > tipsum:
        print("tip adjusted correctly")

        check = 5

        while np.around(sum(roundtip), decimals=3) > tipsum:
            deci = [int(i * 100) % 10 for i in real]
            hit = [i for i, j in enumerate(deci) if j == check]

            for i in hit:
                real[i] = int(real[i] * 10) / 10

            roundtip = np.around(real, decimals=1)

            check += 1
            
    return roundtip, tipsum, real        
    
    
def tmode():
    count = 0
    bar = None
    card = None
    
    for i in range(1, 100):
        while True:
            try:
                value = input('{}{}{}{} = '.format(i + count, '.', ' ' * (2 - len(str(i))), "Hour")).replace(',', '.')
                if '+' not in value:
                    value = abort(value)

                if eval(value) > 11:
                    if '+' in value:
                        bar, card = value.replace(' ', '').split('+', 1)
                
                    hour.append(eval(value))

                elif ' ' in value:
                    thour, times = value.split(' ', 1)
                    count += int(times) - 1
                    for j in range(int(times)):
                        hour.append(float(str(thour)))

                else:
                    hour.append(float(str(value)))

            except (ValueError, NameError) as error:
                print('input error')
                continue
            else:
                break

        if hour[-1] > 11:
            tipsum = float(hour.pop())
            break
    
    ratio = tipsum / sum(hour)

    realtip = np.array([ratio * i for i in hour])                   
    real = np.array([ratio * i for i in hour])

    roundtip = np.around(realtip, decimals=1)

    roundtip, tipsum, real = adjust_tip(roundtip, tipsum, real)

    realtip = [int(i * 1000) / 1000. for i in realtip]
    
    
    text = list()
    
    today = dt.today().strftime("%d.%m.%Y") + ', ' + dt.today().strftime("%A") + ', time: ' + dt.now().strftime("%H:%M")
    text.append(today + '\n')
            
    print('-' *  32)
    text.append('-' *  32 + '\n')

    for i in range(len(hour)):
        t = f'{i+1}"{" " * (4 - len(str(i+1)))}{hour[i]:4.2f}h  -> {roundtip[i]:5.1f}€  ;  {realtip[i]:6.3f}'
        print(t)
        text.append(t + '\n')

    print('-' *  32)
    text.append('-' *  32 + '\n')

    t = f'total hours = {sum(hour):} h'
    print(t)
    text.append(t + '\n')
    
    
    t = f'tip ratio = {ratio:.4} €/h'
    print(t)
    text.append(t + '\n')
    
    text.append('sum = ' + str(tipsum) + '\n')
    text.append('bar = ' + str(bar) + '\n')
    text.append('card = ' + str(card) + '\n')
    
    timestamp = dt.today().strftime("%d") + '-' + dt.today().strftime("%a") + '-' + dt.now().strftime("%H-%M")
    dirname = './txt/'+ dt.today().strftime("%Y") + '/' + dt.today().strftime("%m") + '/'
    path = dirname + '/' + timestamp +'.txt'

    os.makedirs(os.path.dirname(dirname), exist_ok=True)
    with open(path, 'w+') as f:
        f.writelines(text)
        
    subprocess.call(['sh', './update_tip.sh'])
            
            
def normal(value, name, hour):
    i = 1
    
    while True:
        if value == '0':
            print('Gib mindestens einen Namen ein!\nBei Eingabe von 0 wird die Nameneingabe abgebrochen!')
            value = abort(input('{}{} = '.format(i, ".  Name")))

        elif tx.easteregg(value) != False:
            value = abort(input('{}{} = '.format(i, ".  Name")))

        else:
            break

    name.append(value)
    
    while '0' not in name:    
        while True:
            try:
                value = abort(input('{} = '.format("   Hour")))

                if tx.easteregg(value) != False:
                    continue

                hour.append(float(value.replace(',', '.')))

            except ValueError:
                print('Gib nur eine Zahl ein für die Stunden!')
                continue

            else:
                break

        i += 1
        value = abort(input('{}{}{}{} = '.format(i, '.', ' ' * (2 - len(str(i))), "Name")))

        while tx.easteregg(value) != False:
            value = abort(input('{}{}{}{} = '.format(i, '.', ' ' * (2 - len(str(i))), "Name")))

        name.append(value)

    name = name[:-1]

    while True:
        try:
            tipsum = abort(input("total tip = "))

            if tx.easteregg(tipsum) != False:
                continue

            tipsum = float(tipsum.replace(',', '.'))

        except ValueError:
            print('Gib nur eine Zahl ein für das gesamte Trinkgeld!')
            continue

        else:
            break

    ratio = tipsum / sum(hour)

    realtip = np.array([ratio * i for i in hour])                   
    real = np.array([ratio * i for i in hour])

    roundtip = np.around(realtip, decimals=1)

    roundtip, tipsum, real = adjust_tip(roundtip, tipsum, real)

    realtip = [int(i * 1000) / 1000. for i in realtip]        

    maxstr = len(max(name, key=len))

    print('-' * (maxstr + 29))

    for i in range(len(name)):
        print('{num:{width}}'.format(num = name[i], width = maxstr), f' {hour[i]:4.2f}h', f' -> {roundtip[i]:5.1f}€', f' ;  {realtip[i]:6.3f}')

    print('-' * (maxstr + 29))

    print(f'total hours = {sum(hour):} h')   
    print(f'tip ratio = {ratio:.4} €/h')
    

tx.datereasteregg()
    
name = []
hour = []
i = 1

today = dt.today().strftime("%d.%m.%Y") + ', ' + dt.today().strftime("%A") + ', time: ' + dt.now().strftime("%H:%M")
print(today)

value = abort(input('{}{} = '.format(i, ". Name")))

if value == 'tmode':
    tmode()
    
elif value == 'report':
    rp.report()
    
else:
    normal(value, name, hour)