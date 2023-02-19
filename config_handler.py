import json
import datetime
import socket
import time

global LISTEN_PORT
global DATE 
global DATE_TOLERANCE
global GEOCITIES_FIX
global QUICK_IMAGES
global WAYBACK_API
global CONTENT_TYPE_ENCODING
global SILENT
global SETTINGS_PAGE

try:
    with open("config.json") as f:
        data = json.loads(f.read())
        LISTEN_PORT = data["LISTEN_PORT"]
        DATE_TOLERANCE = data["DATE_TOLERANCE"]
        GEOCITIES_FIX = data["GEOCITIES_FIX"]
        QUICK_IMAGES = data["QUICK_IMAGES"]
        WAYBACK_API = data["WAYBACK_API"]
        CONTENT_TYPE_ENCODING = data["CONTENT_TYPE_ENCODING"]
        SILENT = data["SILENT"]
        SETTINGS_PAGE = data["SETTINGS_PAGE"]
except EnvironmentError as e:
    print("Wops! Error opening config.json")

def get_remote_date():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('10.0.0.2', 123))
            data = s.recv(1024)
            remote_time = datetime.datetime.fromtimestamp(int.from_bytes(data[40:48], byteorder='big'))
            return remote_time.strftime('%Y%m%d')
    except Exception as e:
        print(e)
        return '19991231'

DATE = get_remote_date()

while True:
    time.sleep(5)
    new_date = get_remote_date()
    if new_date != DATE:
        DATE = new_date
        print("Date updated to: ", DATE)
