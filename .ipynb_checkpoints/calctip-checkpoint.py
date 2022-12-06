 #!/usr/bin/env python

import numpy as np
import sys
import os
import textwrap
from datetime import date, datetime

# Wrtten by Taro Watanabe, would be nice if you take the code
# with the eastereggs secret, addings are allowed, if you tell me^^


def pinted(text):
    wrapper = textwrap.TextWrapper(initial_indent='\t', subsequent_indent='\t')
    wrapped = textwrap.fill(text=text, width=55)
    print(wrapped)

def abort(var):
    var = str(var).lower()
    
    labort = ['exit', 'stop', 'stopp', 'abbruch', 'abbrechen']
    lhelp = ['help', 'hilfe']
    
    if var in labort:
        print('Exited session.')
        sys.exit()
        
    elif var in lhelp:
        print('\n')
        print('CALCTIP WIKI\n')
        print('-*- Program zum Ausrechnen vom Trinkgeld bei Mayras Wohnzimmercafe.')
        print('Daten werden nicht gespeichert.')
        print('Zum Starten muss der Befehl aufgerufen werden:',
              '\033[1;3mpython3 calctip.py\033[0m\n\n\n')
        
        print('EINGABE ABBRECHEN')
        text = 'Bei jeglicher Eingabe kann \033[1;3mexit\033[0m, \033[1;3mabbruch\033[0m oder \033[1;3mstop\033[0m eingegeben werden, um den gesamten Vorgang abzubrechen. Die Daten gehen dabei verloren.'
        pinted(text)
        print('\n')        
        
        print('EINGABE NAME, HOUR')
        text = 'Geben Sie bei \033[1;3mName\033[0m einen Namen und bei \033[1;3mHour\033[0m die zugehörigen Stunden als Zahl ein. Bei den Stunden dürfen keine Einheiten oder Buchstaben eingegeben werden; Dezimaltrennzeichen kann ein Komma oder Punkt sein. Gleiche Namen können eingegeben werden.'
        pinted(text)
        text = 'Als Name kann \033[1;3mhelp\033[0m, \033[1;3mexit\033[0m \033[1;3mabbruch\033[0m und \033[1;3mstop\033[0m NICHT verwendet werden.'
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
        text = 'Falls das Trinkgeld nicht nach den Regeln des Kaufmännischen Rundens gerundet wurde, wird vor der Trinkgeldtabelle die Ausgabe \033[1;3mtip adjusted correctly\033[0m gedruckt. Das in der Trinkgeldtabelle angezeigte Trinkgeld, welches auf ganze 1ct gerundet ist, bleibt zum Zweck der Kontrolle bei dem ganzen Prozess invariant.'
        pinted(text)
        print('\n\n\n\n\n')
        
        print('Zum Starten den Befehl eingeben:',
              '\033[1;3mpython3 calctip.py\033[0m\n\n\n\n')
        
        sys.exit()
        
    else:
        return var
 

def datereasteregg():
    valentine = r'''
    ☆　+
　+　   _. ☆
☆  へ. /～ヽへ+
+ノ从`(｡ﾟ-ﾟ)从丶 Happy Valentine's day
ノ从从( つ ｨ⌒v⌒,丶 
""""" ﾉ ﾉ ﾉ ＼／""
+　 ☆ し"Ｊ+ ☆
　+　　☆　　+
    '''
    
    santa = r"""
    　o　　　。　　　 　.__o　　O　　 。　 　　。　°
　。　○　　o　　　　○  ／ ｨ　　　　　○　　o　　　　○
　　　　　　　　o 　  /ニﾆ)⌒⌒⌒ヽ　　　　　　　　o
　　　　o　　　　　 　(^_^)____） Merry Christmas!!
　　○　  　。  ○   ／○    ○） ／|,　O　 o
。　　o　　　　 o ∠ ∠____∠_／ ／　　　　　○
　　　　　　o  　 |／   /　|／　　○　　　。　　o　　O　
　o　　O　　　 　／￣￣/￣￣　o　　　 。 
　　　　　　　  ノ  　/　　　 o　　　　　　　　　O
　o　　　o  ∧ ∧___ﾉ)∧ ∧___ﾉ)　　　　。　　　o　　　　　
　　　o　　(ﾟ-ﾟ) 　(ﾟДﾟ*)   つ　　o　　　°　　　　　 o
　。　　　o ∪-∪'"~~ ∪-∪'"~~/　。　　。　o　　。
　　　 ___. .__.　。 　 ___.　.__.     o___.     ☆    ♪　°
  ___. |ﾛﾛ|／ ~ ＼ ___. |ﾛﾛ| ／ ~ ＼ ___|ﾛﾛL_. \(♥♥)(**)/
＿|田|_|ﾛﾛ|_| ﾛﾛ|＿|田|.|ﾛﾛ|__| ﾛﾛ|＿|田|. |ﾛ|. (__)(__)
"""   
    
    newyear = r"""
     *°*”˜˜”*°•.¸☆ ★ ☆¸.•°*”˜˜”*°•.¸☆
     ╔╗╔╦══╦═╦═╦╗╔╗ ★ ★ ★
     ║╚╝║══║═║═║╚╝║ ☆¸.•°*”˜˜”*°•.¸☆
     ║╔╗║╔╗║╔╣╔╩╗╔╝ ★ NEW YEAR ☆
     ╚╝╚╩╝╚╩╝╚╝═╚╝ ♥￥☆★☆★☆￥♥ ★☆❤♫❤♫❤
     .•*¨`*•..¸☼ ¸.•*¨`*•.♫❤♫❤♫❤
                                 .''.
       .''.             *''*    :_\/_:     .
      :_\/_:   .    .:.*_\/_*   : /\ :  .'.:.'.
  .''.: /\ : _\(/_  ':'* /\ *  : '..'.  -=:o:=-
 :_\/_:'.:::. /)\*''*  .|.* '.\'/.'_\(/_'.':'.'
 : /\ : :::::  '*_\/_* | |  -= o =- /)\    '  *
  '..'  ':::'   * /\ * |'|  .'/.\'.  '._____
      *        __*..* |  |     :      |.   |' .---"|
       _*   .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
 ___|  '-'     '    ""       '-'   '-.'    '`      |____
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~~               ~-~-~-~-~-~-~-~-~-~   /|
  ~~~~        (      ~-~-~-~-~-~-~-~  /|~       /_|\
        ~~~~_-H-__  -~-~-~-~-~-~     /_|\    -~======-~
~~~~~-\XXXXXXXXXX/~     ~-~-~-~     /__|_\ ~-~-~-~
~~~-~~~-~-~-~-~    ~-~~-~-~-~-~    ========  ~-~-~-~
"""

    if 1215 <= int(date.today().strftime("%m%d")) <= 1226:
        print(santa)
    elif 1229 <= int(date.today().strftime("%m%d")) or int(date.today().strftime("%m%d")) <= 104:
        print(newyear)
    elif int(date.today().strftime("%m%d")) == 214:
        print(valentine)

def easteregg(string):
    string = string.lower()
    
    lthor = ['thor', 'thor, god of thunder', 'son of odin', 'strongest avenger']
    
    bday = r"""
                    ∩,,,∩
                   (´･ω･｀)
              ┌-----〇--○-----┐
　　　　　　 ∫│HAPPY BIRTHDAY!│(o)
　　 　　 　(┃└-(o)--(o)--(o)─┘ ┃)
　　　　　　|\☆  ┃ ☆  ┃  ★ ┃  ☆ ノ♪
　　　 　(::|"''--,,_____,,--―''~☆∂♪
　　　 ( )- |　　　　 　 　　 。◎+
　　  　.:O★ヽ　 　 　　 　 　o♭∴☆
　　  ☆ :∂ｉo,"'--,,_____,,--''"◇｡♪◎o
    　◇♭。:゜◎::O☆♪★∝ ☆｡∂:o゜♪☆◇｡∂ ◎
"""
    
    kid = r'''
　　 l￣￣￣￣￣l
　　 l　　　　　l
　　 l　　　　　l
　　 l＿＿＿＿＿l
　＿_l＿＿＿＿＿l_＿
　｜｜　 ｜ ￣＼l
　｜ L_＿/＿＿＿l
　▲　＼｜｜｜ ／
　　　　￣￣￣
'''
    conan = 'APTX4869'
    
    order66 = r'''                   
                                     /~\
                                    |oo )      We're doomed!
                                    _\=/_
                    ___        #   /  _  \   #
                   /() \        \\//|/.\|\\//
                 _|_____|_       \/  \_/  \/
                | | === | |         |\ /|
                |_|  O  |_|         \_ _/
                 ||  O  ||          | | |
                 ||__*__||          | | |
                |~ \___/ ~|         []|[]
                /=\ /=\ /=\         | | |
________________[_]_[_]_[_]________/_]_[_\_________________________'''
    
    vader = r"""
   _________________________________
  |:::::::::::::;;::::::::::::::::::|
  |:::::::::::'~||~~~``:::::::::::::|
  |::::::::'   .':     o`:::::::::::|
  |:::::::' oo | |o  o    ::::::::::|
  |::::::: 8  .'.'    8 o  :::::::::|
  |::::::: 8  | |     8    :::::::::|
  |::::::: _._| |_,...8    :::::::::|
  |::::::'~--.   .--. `.   `::::::::|
  |:::::'     =8     ~  \ o ::::::::|
  |::::'       8._ 88.   \ o::::::::|
  |:::'   __. ,.ooo~~.    \ o`::::::|
  |:::   . -. 88`78o/:     \  `:::::|
  |::'     /. o o \ ::      \88`::::|
  |:;     o|| 8 8 |d.        `8 `:::|
  |:.       - ^ ^ -'           `-`::|
  |::.                          .:::|
  |:::::.....           ::'     ``::|
  |::::::::-'`-        88          `|
  |:::::-'.          -       ::     |
  |:-~. . .                   :     |
  | .. .   ..:   o:8      88o       |
  |. .     :::   8:P     d888. . .  |
  |.   .   :88   88      888'  . .  |
  |   o8  d88P . 88   ' d88P   ..   |
  |  88P  888   d8P   ' 888         |
  |   8  d88P.'d:8  .- dP~ o8       |  
  |      888   888    d~ o888       |
  |_________________________________|
"""
    
    father = r"""
                        .-.
                       |_:_|
                      /(_Y_)\
 .                   ( \ M// )
  '.               _.''/'-'''._
    ':            /.--'[[[[]'--.\
      ':        /_'  : |::'| :  '.\
        ':     //   ./ |oUU| ''  :\
          ':  _:'..'  |___|_/ :   :|
            ':.  .'  |_[___]_|  :.':\
             [:: |  :  | |  :   ; : \
              '-'   " .| |.' \ .;.' |
              |\    \ '-'   :       |
              |  \   \.:    :   |   |
              |   \  |  '.   :    \ |
              /       \  :. .;       |
             /     |   |  :__/     :  \
            |  |   |    "   | \  |   ||
           /   \  : :  |:   /  |__|   /|
           |     : : :_/_|  /'._  '--|_
           /___.-/_|-'   \  \
                                 """
    
    yoda = r"""
                     ____
                  _.' :  '._
              .-.''.  ;   .''.-.
     __      / : ___\;  /___ ; \      __
   ,'_ ''--.:__;'.-.';: :'.-.':__;.--'' _',
   :' '.L''--.. '<@.';_  ',@>' ..--''J.' ':
        ':-.._J '-.-'L__ '-- ' L_..-;'
          '-.__ ;  .-'  '-.  : __.-'
              L ' /.------.\' J
               '-.   '--'   .-'
              __.l|-:_JL_;-|;.__
           .-j/'.;  ;''''  / .'\-.
         .' /:'. '-.:     .-' .'|  '.
      .-'  / ;  '-. '-..-' .-'  |    '-.
   .+'-.  | :      '-.__.-'      '-._   \
   ; \ '.| ;                    | : '+. ;
   :  ;   | ;                    | ;  : \
  : '.'-; ;  ;                  :  ;   ,/;
   ;    -: ;  :                ;  : .-''  :
   \   \    : ;             : \-'      :
     ;'.   \  ; :            ;.'_..--  / ;
    :  '-.  '-:  ;          :/.'      .'  :
     \      .-'\        /t-''   ':-+.   :
       '.  .-'    'l    __/ /'. :  ; ; \ ;
         \  .-'' .-'-.-'  .' .'j \/   ;/
          \ / -''   /.     .'.' ;_:'    ;
           :- ''-.'./-.'     /    '.___.'
                 \ t  ._  /  
                  |-.t-._:|
                  """
    
    barista = r"""
 _________________________ 
< taro ist bester barista >
 ------------------------- 
 \     ____________ 
  \    |__________|
      /           /\
     /           /  \
    /___________/___/|
    |          |     |
    |  ==\ /== |     |
    |   O   O  | \ \ |
    |     <    |  \ \|
   /|          |   \ \
  / |  \_____/ |   / /
 / /|          |  / /|
/||\|          | /||\/
    -------------|   
        | |    | | 
       <__/    \__>
       """
    
    ghostbusters = r"""
 _______________
< GHOSTBUSTERS! >
 ---------------
          \
           \
            \          __---__
                    _-       /--______
               __--( /     \ )XXXXXXXXXXX\v.
             .-XXX(   O   O  )XXXXXXXXXXXXXXX-
            /XXX(       U     )        XXXXXXX\
          /XXXXX(              )--_  XXXXXXXXXXX\
         /XXXXX/ (      O     )   XXXXXX   \XXXXX\
         XXXXX/   /            XXXXXX   \__ \XXXXX
         XXXXXX__/          XXXXXX         \__---->
 ---___  XXX__/          XXXXXX      \__         /
   \-  --__/   ___/\  XXXXXX            /  ___--/=
    \-\    ___/    XXXXXX              '--- XXXXXX
       \-\/XXX\ XXXXXX                      /XXXXX
         \XXXXXXXXX   \                    /XXXXX/
          \XXXXXX      >                 _/XXXXX/
            \XXXXX--__/              __-- XXXX/
             -XXXXXXXX---------------  XXXXXX-
                \XXXXXXXXXXXXXXXXXXXXXXXXXX/
                  ""VXXXXXXXXXXXXXXXXXXV""
                  """
    
    bestbarista = ['bester barista', 'besten barista', 'beste barista', 'best barista']
    
    lbday = ['bday', 'b-day', 'birthday', 'geburtstag', 'geburtstagskind']
    
    
    if string in lthor:
        print('access denied.')
    elif string == 'point break':
        print('I love you 3000')
    elif string == 'banner':
        print('welcome, strongest avenger')
        
    elif string == 'kaitou1412':
        print(kid)
    elif string == 'shellingford':
        print(conan)
    
    elif string == 'order 66':
        print(order66)
    elif string == 'may the force be with you':
        print(vader)
    elif string == 'i am your father':
        print(father)
    elif string == 'the force is strong with this one':
        print(yoda)
            
    elif any(s in string for s in bestbarista):
        print(barista)
    elif string == 'who you gonna call':
        print(ghostbusters)
    elif any(s in string for s in lbday):
        print(bday)
        
    else:
        return False
    
    
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

        elif easteregg(value) != False:
            value = abort(input('{}{} = '.format(i, ".  Name")))

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
        value = abort(input('{}{}{}{} = '.format(i, '.', ' ' * (2 - len(str(i))), "Name")))

        while easteregg(value) != False:
            value = abort(input('{}{}{}{} = '.format(i, '.', ' ' * (2 - len(str(i))), "Name")))

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
    

datereasteregg()
    
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