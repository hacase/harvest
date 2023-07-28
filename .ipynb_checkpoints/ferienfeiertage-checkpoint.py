import time
from datetime import datetime as dt
from deutschland import feiertage as ft
from deutschland.feiertage.api import default_api
# Defining the host is optional and defaults to https://feiertage-api.de/api
# See configuration.py for a list of all supported configuration parameters.
configuration = ft.Configuration(
    host = "https://feiertage-api.de/api"
)

def check(date, name=None):
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
            
    
    flag = False
    returnname = False

    for i in ferien:
        if i[1].replace(tzinfo=None) <= date <= i[2].replace(tzinfo=None):
            returnname, _ = i[0].split(' ', 1)
            flag = True
            
    for i in feiertage:
        if date.strftime('%d%m%Y') == i[1].strftime('%d%m%Y'):
            returnname = i[0]
            flag = True
            
    
    if name:
        return returnname
    else:
        return flag