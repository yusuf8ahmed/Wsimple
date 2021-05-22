from wsimple.api import Wsimple

# login to Wealthsimple
def get_otp():
    return input("Enter otpnumber: \n>>>")

email = str(input("Enter email: \n>>>"))
password = str(input("Enter password: \n>>>"))

ws = Wsimple(email, password, otp_callback=get_otp) 

print(ws.get_market_hours(exchange="NYSE"))