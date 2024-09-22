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

from harvest_func import abort, opening, normal_mode
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
    
    value = input('{}{} = '.format(i, ". Hour"))
    
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
        value_clean = value.replace('half', '')
        normal_mode(value_clean, dt.today(), half=True)

    elif 'dummy' in value:
        value_clean = value.replace('dummy', '')
        normal_mode(value_clean, dt.today(), dummy=True)

    elif value == 'exit':
        import statistic
        statistic.statistic()

        import ferienfeiertage as ff
        if ff.rewrite():
            git_update('ferienfeiertage')

        sys.exit()

    elif abort(is_not_float(value)):
        print('wrong input')
        
    else:
        normal_mode(value, dt.today())



subprocess.call('git pull --quiet', shell=True)

opening()

tx.datereasteregg()


while True:
    routine()
    print('\n\n\n')
