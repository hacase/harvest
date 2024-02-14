import ferien as fr
import time
import os
import numpy as np
import json
import calctip as cp
from datetime import datetime as dt
from deutschland import feiertage as ft
from deutschland.feiertage.api import default_api
# Defining the host is optional and defaults to https://feiertage-api.de/api
# See configuration.py for a list of all supported configuration parameters.
configuration = ft.Configuration(
    host = "https://feiertage-api.de/api"
)

def check(date, name=None):
    flag = "false"
    returnname = "false"
        
    try:
        year = int(date.strftime('%Y'))

        ferien = []
        for i in fr.state_vacations('NW', year):
            ferien.append((i.name, i.start, i.end))

        # Enter a context with an instance of the API client
        with ft.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = default_api.DefaultApi(api_client)
            jahr = str(year) # str | Welches Jahr?
            nur_land = "NW" # str | Welches Bundesland? (optional)
            nur_daten = 1 # int | Nur Daten oder auch Hinweise? (optional)

            try:
                # Get Feiertage
                api_response = api_instance.get_feiertage(jahr, nur_land=nur_land, nur_daten=nur_daten)
                feiertage = list(api_response.items())
            except ft.ApiException as e:
                print("Exception when calling DefaultApi->get_feiertage: %s\n" % e)


        for i in ferien:
            if i[1].replace(tzinfo=None) <= date <= i[2].replace(tzinfo=None):
                returnname, _ = i[0].split(' ', 1)
                flag = "true"

        for i in feiertage:
            if date.strftime('%d%m%Y') == i[1].strftime('%d%m%Y'):
                returnname = i[0]
                flag = "true"
                
    except:
        returnname = 'offline'
    
    if name:
        return returnname
    else:
        return flag

def rewrite():
    offline = []
    flag = False

    root_dir = './json/'
    for root, dirs, files in os.walk(root_dir, onerror=None):
        for filename in files:
            if not any(s in filename for s in ['LOG', 'checkpoint', 'DS', 'edited']):
                file_path = os.path.join(root, filename)

                f = open(file_path)
                jData = json.loads(f.read())

                if jData['holiday'] == 'offline':
                    flag = True
                    jData['holiday'] = check(dt.strptime(jData['timestamp'], '%d.%m.%Y-%H:%M'))

                    with open(file_path, 'w') as ff:
                        json.dump(jData, ff)

    cp.git_update("'rewrite offline holidays'")
    
    return flag