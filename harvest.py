 #!/usr/bin/env python
# Wrtten by Taro Watanabe, would be nice if you take the code
# with the eastereggs secret, addings are allowed ^^
# all texts and eastereggs stored in texts.py

import numpy as np
import sys
import time
import os
from datetime import datetime as dt
from urllib import request
import subprocess

from harvest_func import abort, normal_mode, opening
import texts as tx


def is_not_float(var):
    try:
        float(var)
        return False
    except:
        return True

def routine():
    i = 1
    
    print(dt.today().strftime("%d.%m.%Y, %A, time: %H:%M"))
    
    value = abort(input('{}{} = '.format(i, ". Hour")))
    
    if value == 'report':
        import report
        report.report()
        
    elif value == 'statistic':
        import statistic
        statistic.statistic()
    
    elif value == 'repair':
        import repair
        repair.repair()
        
    elif value == 'submit':
        import submit
        submit.submit()

    elif 'half' in value:
        value_clean = value.replace('half ', '')
        tmode(value_clean, dt.today(), half_day=True)

    elif 'dummy' in value:
        dummy_mode()

    elif is_not_float(value):
        print('wrong input')
        
    else:
        normal_mode(value, dt.today())



subprocess.call(['sh', 'git pull --quiet'])

opening()

tx.datereasteregg()


while True:
    routine()
    print('\n\n\n')