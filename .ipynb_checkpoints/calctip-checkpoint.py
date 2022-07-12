#!/usr/bin/env python

import numpy as np
import sys
import os
import textwrap


def pinted(text):
    wrapper = textwrap.TextWrapper(initial_indent='\t', subsequent_indent='\t')
    wrapped = wrapper.fill(text)
    print(wrapped)

def abort(var):
    labort = ['exit', 'Exit', 'EXIT',
              'stop', 'Stop', 'STOP',
              'stopp', 'Stopp', 'STOPP',
              'abbruch', 'Abbruch', 'ABBRUCH']
    
    lhelp = ['help', 'Help', 'HELP',
             'hilfe', 'Hilfe', 'HILFE']
    
    if var in labort:
        print('Exited session.')
        sys.exit()
        
    elif var in lhelp:
        print('\n')
        print('CALCTIP WIKI\n')
        print('-*- Program zum Ausrechnen vom Trinkgeld bei Mayras Wohnzimmercafe.')
        print('Zum Starten muss der Befehl aufgerufen werden:',
              '\033[1;3mpython3 calctip.py\033[0m\n\n\n')
        
        print('EINGABE ABBRECHEN')
        text = 'Bei jeglicher Eingabe kann \033[1;3mexit\033[0m, \033[1;3mabbruch\033[0m oder \033[1;3mstop\033[0m eingegeben werden, um den gesamten Vorgang abzubrechen. Die Daten gehen dabei verloren.'
        pinted(text)
        print('\n')        
        
        print('EINGABE NAME, HOUR')
        text = 'Geben Sie bei \033[1;3mName\033[0m einen Namen und bei \033[1;3mHour\033[0m die zugehörigen Stunden als Zahl ein. Bei den Stunden dürfen keine Einheiten oder Buchstaben eingegeben werden; Dezimaltrennzeichen kann ein Komma oder Punkt sein. Gleiche Namen können eingegeben werden.'
        pinted(text)
        text = 'Als Name kann \033[1;3mhelp\033[0m, \033[1;3mexit\033[0m, \033[1;3mabbruch\033[0m und \033[1;3mstop\033[0m NICHT verwendet werden.'
        pinted(text)
        text = 'Nach vollständiger Eingabe der Namen mit den Stunden muss bei dem Eingabefeld \033[1;3mName\033[0m eine 0 (die Zahl Null) eingegeben werden, um die Eingabe der Namen und Stunden zu beenden.'
        pinted(text)
        print('\n')
        
        print('EINGABE TOTAL TIP')
        text = 'Geben Sie bei \033[1;3mtotal tip\033[0m den geamten Betrag des Trinkgeldes als Zahl ein ohne Einheiten oder Buchstaben; Dezimaltrennzeichen kann ein Komma oder Punkt sein.'
        pinted(text)
        print('\n')
        
        print('TRINKGELDTABELLE')
        text = 'Die eingegebenen Namen und Stunden werden in der eingegebenen Reihenfolge ausgegeben. Das Trinkgeld wird nach den Regeln des Kaufmännischen Rundens gerundet und in ganze 10ct und ganze 1ct gerundete Trinkgeldbeträge ausgegeben. Nach der Tabelle werden die gesamten gearbeiteten Stunden und das Verhältnis Trinkgeld pro Stunde angezeigt.'
        pinted(text)
        print('\n')
        
        print('TRNKGELDBERECHNUNG')
        text = 'Das Trinkgeld wird auf die gesamten Stunden aufgeteilt und mit den gearbeiteten Stunden multipliziert.'
        pinted(text)
        print('\n          gesamtes Trinkgeld')
        print('          ------------------ = Trinkgeld pro Stunde')
        print('             alle Stunden')
        print('\n          Trinkgeld pro Stunde * gearbeitete Stunden = Trinkgeld\n')
        text = 'Das berechnete Trinkgeld wird dabei angepasst, sodass das herausgegebene gerundete Trinkgeld aller Personen nicht das ursprüngliche eingegebene Trinkgeld übersteigt. Falls das herausgegebene Trinkgeld das Eingegebene übersteigen sollte, wird die Rundungsregel angepasst. In diesem Program werden bei den auf 1ct gerundeten Beträgen nach 5ct Beträgen gesucht, welche nun auf 10ct abgerundet werden. Falls weiterhin das Trinkgeld übersteigt, wird nach 6ct, 7ct... Beträgen gesucht. Nach der Suche nach 9ct Beträgen kann das herausgegebene auf 10ct gerundete Trinkgeld nicht das ursprünglich eingegebene Trinkgled übersteigen.'
        pinted(text)
        text = 'Falls das Trinkgeld nicht nach den Regeln des Kaufmännischen Rundens gerundet wurde, wird vor der Trinkgeldtabelle die Ausgabe  \033[1;3mtip adjusted correctly\033[0m gedruckt. Das in der Trinkgeldtabelle angezeigte Trinkgeld, welches auf ganze 1ct gerundet ist, bleibt zum Zweck der Kontrolle bei dem ganzen Prozess invariant.'
        pinted(text)
        print('\n\n\n\n\n')
        
        print('Zum Starten den Befehl eingeben:',
              '\033[1;3mpython3 calctip.py\033[0m\n\n\n\n')
        
        sys.exit()
    else:
        return var
    

def easteregg(string):
    lthor = ['thor', 'thor, god of thunder', 'son of odin', 'strongest avenger']
    
    if string in lthor:
        print('access denied.')
    elif string == 'point break':
        print('I love you 3000')
    elif string == 'banner':
        print('welcome, strongest avenger')
    else:
        return False
    
    
name = []
hour = []
i = 1

value = abort(input('{}{} = '.format(i, ". Name")))

while True:
    if value == '0':
        print('Gib mindestens einen Namen ein!\nBei Eingabe von 0 wird die Nameneingabe abgebrochen!')
        value = abort(input('{}{} = '.format(i, ". Name")))
    
    elif easteregg(value) != False:
        value = abort(input('{}{} = '.format(i, ". Name")))
    
    else:
        break

name.append(value)
    
while '0' not in name:    
    while True:
        try:
            value = abort(input('{} = '.format("   Hour")))
            
            if easteregg(value) != False:
                continue
            
            hour.append(float(value.replace(',', '.')))
            
        except ValueError:
            print('Gib nur eine Zahl ein für die Stunden!')
            continue
            
        else:
            break
    
    i += 1
    value = abort(input('{}{} = '.format(i, ". Name")))
    
    while easteregg(value) != False:
        value = abort(input('{}{} = '.format(i, ". Name")))
        
    name.append(value)
    
name = name[:-1]
    
while True:
    try:
        tipsum = abort(input("total tip = "))
        
        if easteregg(tipsum) != False:
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