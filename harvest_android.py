import os
from time import sleep
os.environ["MPLBACKEND"] = "TkAgg"
os.environ["DISPLAY"] = ":0.0"
print('Loading X server...')
os.system("am start --user 0 -n x.org.server/.RunFromOtherApp 2>/dev/null")
os.environ["DISPLAY"] = ":0.0"
sleep(8) # give the X server an opportunity to start
print('Done')
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1);
y = np.sin(x)
plt.plot(x, y)
plt.show()