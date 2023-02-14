 #!/usr/bin/env python
# text used in calctip.py

import textwrap
from datetime import date, datetime

def pinted(text):
    wrapper = textwrap.TextWrapper(initial_indent='\t', subsequent_indent='\t')
    wrapped = textwrap.fill(text=text, width=55)
    print(wrapped)

def helpman():
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

    
def datereasteregg():
    if 1215 <= int(date.today().strftime("%m%d")) <= 1226:
        santa()
        
    elif 1229 <= int(date.today().strftime("%m%d")) or int(date.today().strftime("%m%d")) <= 104:
        newyear()
        
    elif int(date.today().strftime("%m%d")) == 214:
        valentine()
        
    elif int(date.today().strftime("%m%d")) == 504:
        leia()
    
    
def santa():
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
    print(santa)

def newyear():
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
    print(newyear)
    
def valentine():
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
    print(valentine)
    

def easteregg(string):
    string = string.lower()
    
    lthor = ['thor', 'thor, god of thunder', 'son of odin', 'strongest avenger']
    bestbarista = ['bester barista', 'besten barista', 'beste barista', 'best barista']
    lbday = ['bday', 'b-day', 'birthday', 'geburtstag', 'geburtstagskind']
    
    
    if string in lthor:
        print('access denied.')
    elif string == 'point break':
        print('I love you 3000')
    elif string == 'banner':
        print('welcome, strongest avenger')
        
    elif any(s in string for s in bestbarista):
        barista()
        
    elif any(s in string for s in lbday):
        bday()
        
    elif string == 'kaitou1412':
        kid()
    elif string == 'shellingford':
        conan()
    
    elif string == 'order 66':
        order66()
    elif string == 'may the force be with you':
        vader()
    elif string == 'i am your father':
        father()
    elif string == 'the force is strong with this one':
        yoda()
            
    elif string == 'who you gonna call':
        ghostbusters()
        
    else:
        return False

def leia():
    leia = r"""
    
                                  May the Force be with You
                                /
                            ,===
                           (@o o@
                          / \_-/       ___
                         /| |) )      /() \
                        |  \ \/__   _|_____|_
                        |   \____@=| | === | |
                        |   |      |_|  O  |_|
                        | | |       ||  O  ||
                        | | |       ||__*__||
                       /  |  \     |~ \___/ ~|
                       ~~~~~~~     /=\     /=\
_______________________(_)(__\_____[_]_____[_]_____________________
"""
    print(leia)
    
    
def barista():
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
    print(barista)

def bday():
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
    print(bday)

def kid():    
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
    print(kid)
    
def conan():
    conan = 'APTX4869'
    print(conan)
    
def order66():
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
    print(order66)
    
def vader():
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
    print(vader)
    
def father():
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
    print(father)
    
def yoda():
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
    print(yoda)
    
def ghostbusters():
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
    print(ghostbusters)

