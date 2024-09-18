import numpy as np
import sys
import time
import os
from datetime import datetime as dt
import texts as tx
import ferienfeiertage as ff
import subprocess
import socket


def opening():
    string = """     H opefully
     A ll
     R espectful
     V isitors
     E njoyed
     S ome
     T ipping"""

    typing_speed = 450

    def slow_type(t):
        for l in t:
            sys.stdout.write(l)
            sys.stdout.flush()
            time.sleep(10.0/typing_speed)
        print('\n')

    print('')
    slow_type(string)


def abort(var):
    lower_var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    lhelp = ['help', 'hilfe']
    
    if lower_var in labort:
        print('exited session.')
        sys.exit()
        
    elif lower_var in lhelp:
        tx.helpman()
        sys.exit()
        
    else:
        return var


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False
    

def git_update(message):
    loader = Loader('updating ', 'done.').start()
    
    if is_connected():
        text = "git pull --quiet\ngit add .\ngit commit --quiet -m "
        text += message + "\ngit push --quiet"
        
        with open('./update_tip.sh', 'w+') as f:
            f.writelines(text)
        subprocess.call(['sh', './update_tip.sh'])
        
    else:
        text = """
        git add .\n
        git commit --quiet -m 'delayed update tip data'\n
        git push --quiet\n"""

        with open('./delayed_update_tip.sh', 'w+') as f:
            f.writelines(text)
                
        print('no internet connection detected\ndata stored on device')

    loader.stop()


def git_delayed():
    if not is_connected():
        print('\nno internet connection\nunsaved data may be still on device\n')
        return 0
    
    if os.path.isfile('./delayed_update_tip.sh'):
        loader = Loader.('updating delayed data ', 'done.').start()
        
        subprocess.call(['sh', './delayed_update_tip.sh'])
        subprocess.call('rm ./delayed_update_tip.sh', shell=True)

        loader.stop()
        
        print('\n')


def adjust_tip(roundtip, tipsum, real):
    if np.around(sum(roundtip), decimals=3) > tipsum:
        print("tip adjusted correctly.")

        check = 5

        while np.around(sum(roundtip), decimals=3) > tipsum:
            deci = [int(i * 100) % 10 for i in real]
            hit = [i for i, j in enumerate(deci) if j == check]

            for i in hit:
                real[i] = int(real[i] * 10) / 10

            roundtip = np.around(real, decimals=1)

            check += 1
            
    return roundtip, tipsum, real


def fcalctip(hour, tipsum):
    ratio = tipsum / sum(hour)

    realtip = np.array([ratio * i for i in hour])                   
    real = np.array([ratio * i for i in hour])

    roundtip = np.around(realtip, decimals=1)

    roundtip, tipsum, real = adjust_tip(roundtip, tipsum, real)

    realtip = [int(i * 1000) / 1000. for i in realtip]
    
    return roundtip, tipsum, real, realtip, ratio


def print_table(hour, roundtip, realtip, ratio, tipsum, bar, card, date, text=None):        
        
    print('-' *  32)
    
    t_hour = '"hour": ['
    t_tip = '"tip": ['
    t_exact = '"tip_exact": ['

    for i in range(len(hour)):
        t = f'{i+1}"{" " * (3 - len(str(i+1)))}{hour[i]:5.2f}h  -> {roundtip[i]:5.1f}€  ;  {realtip[i]:6.3f}'
        print(t)
        
        t_hour += f'{hour[i]:.2f}, '
        t_tip += f'{roundtip[i]:.1f}, '
        t_exact += f'{realtip[i]:.3f}, '
        
    t_hour = t_hour[:-2] + '], '
    t_tip = t_tip[:-2] + '], '
    t_exact = t_exact[:-2] + '], '
    
    text += t_hour + t_tip + t_exact

    print('-' *  32)

    
    t = 'total hours =' + '{0:.2f}'.format(sum(hour)) + 'h'
    print(t)
    
    t = f'tip ratio = {ratio:.4} €/h'
    print(t)
    text += '"ratio": ' + f'{ratio:.4}, '
    t = f'tip sum = {tipsum:.2f}'
    text += '"sum": ' + '{0:.2f}'.format(tipsum) + ', '
    text += '"bar": ' + str(bar) + ', '
    text += '"card": ' + str(card) + ', '
    
    if is_connected():
        holidayname = ff.check(date, name=1)
    else:
        holidayname = 'offline'
    t = 'holiday : ' + holidayname + '\n'
    print(t)
    text += '"holiday": ' + '"' + holidayname + '"}'
    
    if text:
        return text


def normal_mode(value, date, half_day=False):
    hour = []
    i = 2
    count = 1
    bar = 'false'
    card = 'false'
    
    if ' ' in value:
        thour, times = value.split(' ', 1)
        count += int(times) - 1
        for j in range(int(times)):
            hour.append(float(str(thour).replace(',', '.')))

    else:
        hour.append(float(str(value)))
    
    for i in range(1, 100):
        while True:
            try:
                value = input('{}{}{}{} = '.format(i + count, '.', ' ' * (2 - len(str(i))), "Hour")).replace(',', '.')

                if '+' not in value:
                    value = abort(value)

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
    
    roundtip, tipsum, real, realtip, ratio = fcalctip(hour, tipsum)
    
    
    today = date.strftime("%d.%m.%Y, %A, time: %H:%M")
    text = '{"timestamp": "' + date.strftime('%d.%m.%Y-%H:%M", ')
    
    text = print_table(hour, roundtip, realtip, ratio, tipsum, bar, card, date, text)
    
    git_delayed()
    
    timestamp = date.strftime("%d-%a-%H-%M")
    dirname = date.strftime("./json/%Y/%m/")

    if not half_day:
        timestamp += '-WHOLE'
        
    path = dirname + '/' + timestamp +'.json'

    os.makedirs(os.path.dirname(dirname), exist_ok=True)
    with open(path, 'w+') as f:
        f.writelines(text)
    
    print('')
    git_update("'update data'")

    loader = Loader.('updating ferienfeiertage ', 'done.').start()
    if ff.rewrite():
        subprocess.call('git add .', shell=True)
        subprocess.call('git commit --quiet -m "rewrite holidays"', shell=True)
        subprocess.call('git push --quiet', shell=True)
    loader.stop()
    
