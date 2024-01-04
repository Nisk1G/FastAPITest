from fastapi import FastAPI
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Google Sheets Authentication
Auth = "auth.json" # ここにjsonファイルのPathを入力する
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(Auth, scope)
Client = gspread.authorize(credentials)

#Sheet Key
bus_time_sheet_key = "1-O0RRZyd_xCGoj1cwoHYrigngggZx1g_Yzw0zMPwBDs"

app = FastAPI()

@app.get("/")
def hello_world():
    print("Hello world")
    return {"message": "Hello World"}

@app.get("/bus")
def get_bus_time():
    SpreadSheet = Client.open_by_key(bus_time_sheet_key)
    RawData = SpreadSheet.worksheet("シート1")
    Data = pd.DataFrame(RawData.get_all_values())
    print(Data)