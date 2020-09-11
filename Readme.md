<p align="center">
  <a>
    <img src="app/static/media/logo64.svg">
    <br>
    <img src="https://forthebadge.com/images/badges/contains-technical-debt.svg">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg">
    <img src="https://forthebadge.com/images/badges/uses-badges.svg">
  </a>
</p>

## Getting Started

  ### Project Status
  <p style="color:red;font-size:35px;margin:0px;">
  Pre-alpha v1.0
  </p>
  This project is in the pre-alpha stage. if you find any bugs please submit an issue.

  ### Prerequisites
  * python and pip is required to use/download wsimple
  * to download pip and python goto ["Download Python"](https://realpython.com/installing-python/)
  * for windows click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-windows)
  * for macos click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-macos)

  ### Installing (Not Ready)
  ```bash
  pip install wsimple
  ```
  #### start webserver (Not Ready)
  ```bash
  wsimple start
  ```
## API

#### Usage
  ```python
  from Wsimple import Wsimple
  from getpass import getpass

  ws = Wsimple("john.doe@gmail.com", "johndoepass")
  # Wsimple("gmail", "password")

  print(ws.find_securities("GOOG")) 
  # return a list of securities that include GOOG and GOOGL
  ```

#### API methods
### function init(email, password):

Initializes and gets Access and Refresh tokens. The LOGIN endpoint  
initializes a new session for the given email and password set. If  
the login is successful, access and refresh tokens are returned in  
the headers. The access token is the key for invoking all other end points.  

### function refresh_token():
Generates a new set of access and refresh tokens.
         
### function get_account():
Grabs account info of this WealthSimple Trade account.
    
### function get_historical_account_data(time: str):
The HISTORY_ACCOUNT endpoint provides historical snapshots of the  
WealthSimple account for a specified timeframe.  
1: Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] auto set 1d  
2: Where ACCOUNT is the account id received from /account/list  
Ex. rrsp-123_abc auto set to frist accounts id  
    
### function get_orders():
Get all current and past orders.  

### function buymarketorder(security_id: str, limit_price: int = 1, quantity: int = 1):
Places an market buy order for a security. Works  
    
### function sellmarketorder(security_id: str, quantity: int =1):
Places an market sell order for a security. Works  

### function buylimitorder(security_id, limit_price, account_id=None, quantity=1):
NotImplementedError  

### function selllimitorder(security_id, limit_price, account_id=None, quantity=1):
NotImplementedError  

### function delete_order(order_id: str):
Cancels a specific order by its id.  
Where ORDER is order_id from place order  
        
### function find_securities(ticker: str):
Grabs information about the security resembled by the ticker  
Where TICKER is the ticker of the company, Wealthsimple will fuzzy  
match this argument and therefore multiple results can appear.  

### function find_securities_by_id(sec_id: str) -> dict:
Grabs information about the security resembled by the security id  
    
### function find_securities_by_id_historical(sec_id: str, time: str):
Grabs information about the security resembled by the security id in a a specified timeframe.  

### function get_positions():
Get all current securities held by this WealthSimple Trade account.   
        
### function get_activities():
Provides the most recent 20 activities (deposits, dividends, orders, etc)  
on this WealthSimple Trade account.  
?type ->> ?type=deposit, ?type=dividend  
?limit ->> < 100  
?bookmark ->> where bookmark is return by each GET that can be used for the subsequent  
^> pages in following calls.  
?account-id ->> ??????  
    
### function get_activities_bookmark(bookmark):
Provides the most recent 20 activities (deposits, dividends, orders, etc)  
on the WealthSimple Trade account. used url query bookmark  
    
### function get_me():
Get Basic info of this WealthSimple Trade account.  
    
### function get_person():
Get more Advanced/Personal info of this WealthSimple Trade account.  
    
### function get_bank_accounts():
Get all linked bank accounts under the WealthSimple Trade account.
    
### function get_deposits():
Get all deposits under the WealthSimple Trade account. 

### function get_all_markets():
Get all market data-hours including the hours

### function get_market_hours(exchange):
Get all market data-hours about a specific exchange ("TSX", "NYSE")

### function get_watchlist():
Get watchlist under this WealthSimple Trade account.    
          
### function delete_watchlist(sec_id):
Delete security from watchlist under this WealthSimple Trade account. 
           
### function add_watchlist(sec_id):
Add security  under this WealthSimple Trade account.  
                   
### function get_exchange_rate(self):
Current WealthSimple Trade USD/CAD exchange rates.  

### def usd_to_cad(self, amount):
use wealthsimple forex exchange to change usd to cad.  
not working correctly
    
### def get_sell_usd(self, amount: float):
use wealthsimple forex exchange to change cad to usd.  
not working correctly.  

### def get_total_value(self):
Get total account value of this wealthsimple account in cad 

### def dashboard(self):
Get dashboard need for route "/home".  

#? public functions (can be used without login in)  
### def public_find_securities_by_ticker(ticker):  
staticmethod: get a company historical data by the actual ticker  

### def public_find_securities_by_ticker_historical(ticker, time):  
staticmethod: get a company historical data based on time and by the actual ticker   

### def public_top_traded(offset=0, limit=5):  
staticmethod: get top traded companies on wealthsimple trade  

### def public_find_securities_news(ticker):  
staticmethod: get public news based on ticker name but this only work for larger stocks  

#? wealthsimple operational status also public    
### def summary_status():  
staticmethod: get current summary status/incidents of wealthsimple trade.  
json in content  
#summary contains data for [   
#Login and Account Access, Quotes iOS app Order execution  
#Security Search, Order submission, Apps, Android App  
#Order status, Trading, Market Data, Order Cancellation,  
#Linking bank accounts, Deposits and Withdrawals,  
#Account Values, Account Opening ]  
  
### def current_status():
staticmethod: get current status/incidents of wealthsimple trade.  
json is large and in content  
  
### def previous_status():
staticmethod: get previous status/incidents of wealthsimple trade.  
json is large and in content  

### def auth(email, password):  
staticmethod: checks if the given email and password is correct   

## Disclaimer
  #### **DO NOT LEVERAGE THIS IN ATTEMPT TO DISRUPT ORDERLY MARKET FUNCTIONS**.
  This software is provided so you can use Wealthsimple trade on your computer duh, but you should understand that you have a responsibility to not engage in illegal trading behaviours that can disrupt orderly market functions. This means that you should not flood the website with orders in a fast manner. You might even get banned or locked out by WealthSimple Trade.

  You would be abusing this tool if you are leveraging it to carry out tactics that would provide you illegitimate personal gains. For example, [Spoofing](https://en.wikipedia.org/wiki/Spoofing_(finance)) is a forbidden tactic that has demonstrable negative effects on the operation of the markets.

  Remember when using this website you are still in agreement with Wealthsimple Trade and Crypto terms of service and they reserve the right to terminate anyone

  My recommendation is to be very conservative about how many orders you place within a small timeframe. I have no idea what
  the maximum amount of orders is by any timeframe, but if you have a gut feeling that it is too much, then it is too much.

  Users of [wstrade-api](https://github.com/ahmedsakr/wstrade-api) have observed that trades in excess of 7 per hour are rejected by the WealthSimple Trade servers. You can use this observation as a baseline of how many trades you can perform on an hourly basis.

  #### **USE AT YOUR OWN RISK**.
  Even though this software is 1000% secure due to everyone running an independent and secluded webserver and that no data is being sent out. But I still must say that this software is not built by or affiliated in way with Wealthsimple Trade or the company Wealthsimple. The use of this software is done at your own discretion and risk and with the agreement that you will be solely responsible for any damage to your computer system or loss of data that results from such activities. By using this software you solely responsible for any damages to you or your Wealthsimple account, and that I will not be liable for any damages that you may suffer connection with downloading, installing, using, modifying or distributing this software.

  to reiterate
  >I take NO responsibility and/or liability for how you choose to use the software. By using the software, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again, ALL software here is for PERSONAL and ONLY PERSONAL use.
