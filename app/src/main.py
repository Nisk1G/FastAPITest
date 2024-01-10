from fastapi import FastAPI
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import googlemaps
import pprint
import pytz
from datetime import datetime, time

#Google Sheets Authentication
auth = "auth.json"
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(auth, scope)
client = gspread.authorize(credentials)

#Sheet Key
master_data_sheet_key = "1-O0RRZyd_xCGoj1cwoHYrigngggZx1g_Yzw0zMPwBDs"

app = FastAPI()

'''
input : sheet_name at spreadsheet(https://docs.google.com/spreadsheets/d/1-O0RRZyd_xCGoj1cwoHYrigngggZx1g_Yzw0zMPwBDs/edit#gid=2010775418)
output : pd.DataFrame format
'''
def read_spreadsheet(sheet_name):
    #read
    spread_sheet = client.open_by_key(master_data_sheet_key)
    raw_data = spread_sheet.worksheet(sheet_name)
    data = pd.DataFrame(raw_data.get_all_values())
    
    return data

# string(time)⇒time object
def parse_time(time_str):
    if time_str == "0:00":
        return time(23, 59, 59)
    return datetime.strptime(time_str, '%H:%M').time()

# open_now value check
def is_open(row, current_weekday, current_time):
    if row['regular_holiday'] == current_weekday:
        return 'FALSE'
    
    lunch_open = parse_time(row['lunch_opening_hour'])
    lunch_close = parse_time(row['lunch_closing_hour'])
    dinner_open = parse_time(row['dinner_opening_hour'])
    dinner_close = parse_time(row['dinner_closing_hour'])

    if lunch_open <= current_time <= lunch_close or dinner_open <= current_time <= dinner_close:
        return 'TRUE'
    else:
        return 'FALSE'


@app.get("/")
def hello_world():
    print("Hello world")
    return [{"message": "Hello World"}, {"message": "Test"}]

#bus api
@app.get("/bus")
def get_bus_info():
    data = read_spreadsheet("bus_schedule")
    #process
    data.columns = data.iloc[0]
    data = data[1:]
    json_data = data.to_json(orient='records')
    res = json.loads(json_data)
    return res

#food api　(campus : string)
@app.get("/food")
def get_food_info(campus):
    data = read_spreadsheet("food_shop")
    ##process
    data.columns = data.iloc[0]
    data = data[1:]
    #process(campus)
    campus_string = campus
    data = data[data['campus'] == campus_string]
    #process(open_now)
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    time = now.time()
    weekday = now.strftime('%a')
    data['open_now'] = data.apply(is_open, axis=1, current_weekday = weekday, current_time = time)
    json_data = data.to_json(orient='records')
    res = json.loads(json_data)
    return res

