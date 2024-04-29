 #!/usr/bin/env python
# Wrtten by Taro Watanabe, would be nice if you take the code
# with the eastereggs secret, addings are allowed ^^
# all texts and eastereggs stored in texts.py

import numpy as np
import sys
import time
import os
from datetime import datetime as dt
import calctip as ct
import texts as tx
from urllib import request


def routine():
    i = 1
    
    print(dt.today().strftime("%d.%m.%Y, %A, time: %H:%M"))
    
    value = ct.abort(input('{}{} = '.format(i, ". Hour")))
    
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

    elif 'dummy' in value:
        value_clean = value.replace('dummy ', '')
        ct.tmode(value_clean, dt.today(), dummy=True)
        
    else:
        ct.tmode(value, dt.today())


ct.opening()

tx.datereasteregg()


while True:
    routine()
    print('\n\n\n')