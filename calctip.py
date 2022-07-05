#!/usr/bin/env python

import numpy as np

name = []
hour = []
i = 1

name.append(input('{}{} = '.format(i, ". Name")))
while name[-1] != "0":
    hour.append(float(input('{} = '.format("   Hour"))))
    i += 1
    name.append(input('{}{} = '.format(i, ". Name")))
    
name = name[:-1]
    
tipsum = float(input("total tip="))

ratio = tipsum / sum(hour)
print(f'tip ratio= {ratio:.4} €/h')

realtip = np.array([ratio * i for i in hour])
real = np.array([ratio * i for i in hour])

roundtip = np.around(realtip, decimals=1)

if sum(roundtip) > tipsum:
    print("tip rounded correctly")
    
    check = 5
    
    while np.around(sum(roundtip), decimals=3) > tipsum:
        deci = [int(i * 100) % 10 for i in real]
        hit = [i for i, j in enumerate(deci) if j == check]
        
        for i in range(len(roundtip)):
            if i in hit:
                real[i] = int(real[i] * 10) / 10
                
        roundtip = np.around(real, decimals=1)
        
        check += 1

maxstr = len(max(name, key=len))
print('-' * (maxstr + 27))
for i in range(len(name)):
    print('{num:{width}}'.format(num = name[i], width = maxstr), f' {hour[i]}h', f' -> {roundtip[i]:5.1f}€', f' %  {realtip[i]:5.2f}')