from fastapi import FastAPI
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import googlemaps
import pprint

#Google Sheets Authentication
Auth = "auth.json" # ここにjsonファイルのPathを入力する
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(Auth, scope)
Client = gspread.authorize(credentials)

#Google Map Authentication
map_key = "AIzaSyBuB8FxDFCich3vPRNGuGEhgizio86bDjI"
map_client = googlemaps.Client(map_key)

#Sheet Key
master_data_sheet_key = "1-O0RRZyd_xCGoj1cwoHYrigngggZx1g_Yzw0zMPwBDs"

#constraints
mozu_lat = 34.5450379
mozu_lng = 135.5066057
sugi_lat = 34.5906436
sugi_lng = 135.504993

app = FastAPI()

@app.get("/")
def hello_world():
    print("Hello world")
    return [{"message": "Hello World"}, {"message": "Test"}]

@app.get("/bus")
def get_bus_time():
    #read
    SpreadSheet = Client.open_by_key(master_data_sheet_key)
    RawData = SpreadSheet.worksheet("bus_schedule")
    Data = pd.DataFrame(RawData.get_all_values())
    #process
    Data.columns = Data.iloc[0]
    Data = Data[1:]
    json_data = Data.to_json(orient='records')
    res = json.loads(json_data)
    
    print(Data)
    print(res)
    return res

@app.get("/mozu_food")
def get_mozu_food():
    loc = {'lat': mozu_lat, 'lng': mozu_lng}
    place_results = map_client.places_nearby(location=loc, radius=500, keyword='レストラン',language='ja') 
    pprint.pprint(place_results)
    results = []
    photos = []
    for place_result in place_results['results']:
        results.append(place_result)
        if not 'photos' in place_result.keys():
            photo = 'no image'
            photos.append(photo)
        else:
            p_value = place_result['photos'][0]['photo_reference']
            photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,map_key)
            photos.append(photo)
    pprint.pprint(results)
    
    return {'infos': results, 'photos' : photos}

@app.get("/sugi_food")
def get_sugi_food():
    loc = {'lat': sugi_lat, 'lng': sugi_lng}
    place_results = map_client.places_nearby(location=loc, radius=500, keyword='レストラン',language='ja') 
    pprint.pprint(place_results)
    results = []
    photos = []
    for place_result in place_results['results']:
        results.append(place_result)
        if not 'photos' in place_result.keys():
            photo = 'no image'
            photos.append(photo)
        else:
            p_value = place_result['photos'][0]['photo_reference']
            photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,map_key)
            photos.append(photo)
    pprint.pprint(results)
    
    return {'infos': results, 'photos' : photos}

