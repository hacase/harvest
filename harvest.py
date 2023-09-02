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


ct.opening()

tx.datereasteregg()
    
name = []
hour = []
i = 1

today = dt.today().strftime("%d.%m.%Y") + ', ' + dt.today().strftime("%A") + ', time: ' + dt.now().strftime("%H:%M")
print(today)

value = ct.abort(input('{}{} = '.format(i, ". Name")))

if value == 'tmode':
    ct.tmode()
    
elif value == 'report':
    import report
    report.report()
    
elif value == 'statistic':
    import statistic
    statistic.statistic()

elif value == 'repair':
    import repair
    repair.repair()
    
else:
    ct.normal(value, name, hour)
