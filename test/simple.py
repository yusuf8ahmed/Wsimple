from wsimple.api import Wsimple, WSOTPUser
from getpass import getpass
import json

email = str(input("Enter email: \n>>>"))
passw = str(getpass("Enter password (Invisible text input): \n>>>"))
try:
    ws = Wsimple(email, passw)
    tokens = ws.tokens
except WSOTPUser:
    otpnumber = int(input("Enter otpnumber: \n>>>"))
    ws = Wsimple.otp_login(email, passw, otpnumber)
    tokens = ws.tokens  

# pull account info
res = ws.get_accounts(tokens)

# display account info
print(json.dumps(res, indent=4))