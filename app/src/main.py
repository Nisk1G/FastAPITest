from fastapi import FastAPI
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

#Google Sheets Authentication
Auth = "auth.json" # ここにjsonファイルのPathを入力する
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(Auth, scope)
Client = gspread.authorize(credentials)

#Sheet Key
master_data_sheet_key = "1-O0RRZyd_xCGoj1cwoHYrigngggZx1g_Yzw0zMPwBDs"

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