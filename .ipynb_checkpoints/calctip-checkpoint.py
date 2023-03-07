 #!/usr/bin/env python
# Wrtten by Taro Watanabe, would be nice if you take the code
# with the eastereggs secret, addings are allowed ^^

import numpy as np
import sys
import os
from datetime import date, datetime
import texts as tx


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
    
    
def tmode():
    count = 0
    for i in range(1, 100):
        while True:
            try:
                value = abort(input('{}{}{}{} = '.format(i + count, '.', ' ' * (2 - len(str(i))), "Hour"))).replace(',', '.')
                
                if ' ' in value:
                    thour, times = value.split(' ', 1)
                    count += int(times) - 1
                    for j in range(int(times)):
                        hour.append(float(str(thour)))
                else:
                    hour.append(float(str(value)))
                    
            except ValueError:
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

    realtip = [int(i * 1000) / 1000. for i in realtip]
    
    space = '.' + ' '
            
    print('-' *  32)

    for i in range(len(hour)):
        print(i+1, '"', ' ' * (4 - len(str(i+1))), f'{hour[i]:4.2f}h ', f' -> {roundtip[i]:5.1f}€ ', f' #  {realtip[i]:6.3f}', sep='')

    print('-' * 32)

    print(f'total hours = {sum(hour):} h')   
    print(f'tip ratio = {ratio:.4} €/h')
            
            
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

    realtip = [int(i * 1000) / 1000. for i in realtip]        

    maxstr = len(max(name, key=len))

    print('-' * (maxstr + 29))

    for i in range(len(name)):
        print('{num:{width}}'.format(num = name[i], width = maxstr), f' {hour[i]:4.2f}h', f' -> {roundtip[i]:5.1f}€', f' #  {realtip[i]:6.3f}')

    print('-' * (maxstr + 29))

    print(f'total hours = {sum(hour):} h')   
    print(f'tip ratio = {ratio:.4} €/h')
    

tx.datereasteregg()
    
name = []
hour = []
i = 1

today = date.today().strftime("%d.%m.%Y") + ', ' + date.today().strftime("%A") + ', time: ' + datetime.now().strftime("%H:%M")
print(today)

value = abort(input('{}{} = '.format(i, ". Name")))

if value == 'tmode':
    tmode()
    
else:
    normal(value, name, hour)