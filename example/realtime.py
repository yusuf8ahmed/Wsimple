import asyncio
import json

from wsimple.api import Wsimple
# access realtime data - pip install websockets
# websockets requires Python ≥ 3.6.1
import websockets 

# login to Wealthsimple
def get_otp():
    return int(input("Enter otpnumber: \n>>>"))

email = str(input("Enter email: \n>>>"))
password = str(input("Enter password: \n>>>"))

ws = Wsimple(email, password, otp_callback=get_otp) 

def event_greeting(data):
    print(data)
    
def event_account(data):
    print(data)
    
def event_price_quote(data):
    print(data)  

async def ws_realtimedata():
    uri = ws.get_websocket_uri() 
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if data["type"] == "GREETING":
                await event_greeting(data)
            elif data["type"] == "ACCOUNT":
                await event_account(data)
            elif data["type"] == "PRICE_QUOTE":
                await event_price_quote(data)
            else:
                print("unsupported event: {}", data["type"]) 
                                         
asyncio.get_event_loop().run_until_complete(ws_realtimedata())
