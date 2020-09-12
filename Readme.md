<p align="center">
  <a>
    <img src="app/static/media/logo64.svg">
    <br>
    <img src="https://forthebadge.com/images/badges/contains-technical-debt.svg">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg">
    <img src="https://forthebadge.com/images/badges/uses-badges.svg">
    <img src="https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg">
  </a>
</p>

### What is the Wsimple project
Welcome! This project is a . 
. 
. Also Wsimple allows the access API wrapper without the use of the web interface
(See => [API-methods](#API-methods)).

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
<a id="index"></a>

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
### table of content (42)

* [Wsimple.__init__()](#init)
* [Wsimple.refresh_token()](#refreshtoken)

* [Wsimple.get_account()](#getaccount)
* [Wsimple.get_historical_account_data()](#gethistoricalaccountdata)
* [Wsimple.get_me()](#getme)
* [Wsimple.get_person()](#getperson)
* [Wsimple.get_bank_accounts()](#getbankaccounts)
* [Wsimple.get_positions()](#getpositions)

* [Wsimple.get_orders()](#getorders)
* [Wsimple.buymarketorder()](#buymarketorder)
* [Wsimple.sellmarketorder()](#sellmarketorder)
* [Wsimple.buylimitorder()](#buylimitorder)
* [Wsimple.selllimitorder()](#selllimitorder)
* [Wsimple.delete_order()](#deleteorder)

* [Wsimple.find_securities()](#findsecurities)
* [Wsimple.find_securities_by_id()](#findsecuritiesbyid)
* [Wsimple.find_securities_by_id_historical()](#findsecuritiesbyidhistorical)

* [Wsimple.get_activities()](#getactivities)
* [Wsimple.get_activities_bookmark()](#getactivitiesbookmark)

* [Wsimple.make_deposit()](#makedeposit)
* [Wsimple.get_deposit()](#getdeposit)
* [Wsimple.list_deposits()](#listdeposits)
* [Wsimple.delete_deposit()](#deletedeposit)

* [Wsimple.get_all_markets()](#getallmarkets)
* [Wsimple.get_market_hours()](#getmarkethours)

* [Wsimple.get_watchlist()](#getwatchlist)
* [Wsimple.delete_watchlist()](#deletewatchlist)
* [Wsimple.add_watchlist()](#addwatchlist)

* [Wsimple.get_exchange_rate()](#getexchangerate)

* [Wsimple.usd_to_cad()](#usdtocad)
* [Wsimple.cad_to_usd()](#cadtousd)
* [Wsimple.get_total_value()](#gettotalvalue)
* [Wsimple.settings()](#settings)
* [Wsimple.dashboard()](#dashboard)

* [Wsimple.public_find_securities_by_ticker()](#publicfindsecuritiesbyticker)
* [Wsimple.public_find_securities_by_ticker_historical()](#publicfindsecuritiesbytickerhistorical)
* [Wsimple.public_top_traded()](#publictoptraded)
* [Wsimple.public_find_securities_news()](#publicfindsecuritiesnews)
* [Wsimple.summary_status()](#publicsummarystatus)
* [Wsimple.current_status()](#publiccurrentstatus)
* [Wsimple.previous_status()](#publicpreviousstatus)
* [Wsimple.auth()](#auth)

<a id="init"></a>

### function init(email, password):

Initializes and sets Access and Refresh tokens. The LOGIN endpoint.    
initializes a new session for the given email and password set. If.     
the login is successful, access and refresh tokens are returned in.   
the headers. The access token is the key for invoking all other endpoints.  

[Back to top—>](#index)

<a id="refreshtoken"></a>

### function refresh_token():
Generates and applies a new set of access and refresh tokens.  

[Back to top—>](#index)

<a id="getaccount"></a>

### function get_account():
Grabs account info of this WealthSimple Trade account.   

[Back to top—>](#index)

<a id="gethistoricalaccountdata"></a>   

### function get_historical_account_data(time: str):
The HISTORY_ACCOUNT endpoint provides historical snapshots of the.   
WealthSimple account for a specified timeframe.  
1.Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] autoset 1d.    
2.Where ACCOUNT is the account id received from /account/list: autoset to first accounts_id.     

[Back to top—>](#index)

<a id="getorders"></a>

### function get_orders():
Get all current and past orders.    

[Back to top—>](#index)

<a id="buymarketorder"></a>

### function buymarketorder(security_id: str, limit_price: int = 1, quantity: int = 1):
Places a market buy order for a security. Works.    

[Back to top—>](#index)

<a id="sellmarketorder"></a>  

### function sellmarketorder(security_id: str, quantity: int = 1):
Places a market sell order for a security. Works.   

[Back to top—>](#index)

<a id="buylimitorder"></a>

### function buylimitorder(security_id, limit_price, account_id=None, quantity=1):
Places a limit buy order for a security.    
NotImplementedError  

[Back to top—>](#index)

<a id="selllimitorder"></a>

### function selllimitorder(security_id, limit_price, account_id=None, quantity=1):
Places a limit sell order for a security.  
NotImplementedError  

[Back to top—>](#index)

<a id="deleteorder"></a>

### function delete_order(order: str):
Cancels a specific order by its id.    
Where ORDER is order_id from place order.    

[Back to top—>](#index)

<a id="findsecurities"></a>  

### function find_securities(ticker: str):
Grabs information about the security resembled by the ticker.    
1.Where TICKER is the ticker of the company, API will fuzzy.     
match this argument and therefore multiple results can appear.   

[Back to top—>](#index)

<a id="findsecuritiesbyid"></a>

### function find_securities_by_id(sec_id: str) -> dict:
Grabs information about the security resembled by the security id.      

[Back to top—>](#index)

<a id="findsecuritiesbyidhistorical"></a>

### function find_securities_by_id_historical(sec_id: str, time: str):
Grabs information about the security resembled by the security id in a a specified timeframe.   
1.Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] autoset 1d.   

[Back to top—>](#index)

<a id="getpositions"></a>

### function get_positions():
Get all current position held by this WealthSimple Trade account.    

[Back to top—>](#index)

<a id="getactivities"></a>    

### function get_activities():
Provides the most recent 20 activities (deposits, dividends, orders, etc).   
on this WealthSimple Trade account.  
?type ->> deposit, dividend, sell, buy, withdrawal  
?limit ->> less than 100.    
?bookmark ->> where bookmark is return by each GET that can be used for the subsequent.    
^> pages in following calls.    
?account-id ->> ??????.    

[Back to top—>](#index)

<a id="getactivitiesbookmark"></a>   

### function get_activities_bookmark(bookmark):
Provides the last 20 activities (deposits, dividends, orders, etc) on the WealthSimple Trade.   
account based on the url query bookmark.   
?bookmark ->> [long string of alphanumeric characters from the response of [Wsimple.get_activities()](#getactivities) ].   

[Back to top—>](#index)

<a id="getme"></a>

### function get_me():
Get Basic info of this WealthSimple Trade account.    

[Back to top—>](#index)

<a id="getperson"></a> 

### function get_person():
Get more Advanced-Personal info of this WealthSimple Trade account.    

[Back to top—>](#index)

<a id="getbankaccounts"></a>  

### function get_bank_accounts():
Get all linked bank accounts under the WealthSimple Trade account.  

[Back to top—>](#index)

<a id="makedeposit"></a>  

### function make_deposit():
make a deposit under this WealthSimple Trade account.  
1.Where amount is the amount to deposit.  
2.Where currency is the currency need to be transferred(Only CAD): autoset to "CAD"  
3.Where bank_account_id is id of bank account where the money is going to be deposited to  
(can be found in [get_bank_accounts function](#getbankaccounts)).  
if bank_account_id is not passed then it will pick the first result.  
4.Where account_id is id of the account that is depositing the money (can be found in [get_account function](#getaccount)).  
if account_id is not passed then it will pick the first result.  
 
[Back to top—>](#index)

<a id="getdeposit"></a>  

### function get_deposit():
Get specific deposit under this WealthSimple Trade account.  
1.Where funds_transfer_id is the id of the transfer and is in the result of [make_deposit function](#makedeposit)  
but can be also found in [list_deposits function](#listdeposits)  
 
[Back to top—>](#index)

<a id="listdeposits"></a>  

### function list_deposits():
Get all deposits under this WealthSimple Trade account.
 
[Back to top—>](#index)

<a id="deletedeposit"></a>  

### function delete_deposit():
Delete a specific deposit under this WealthSimple Trade account.
 
[Back to top—>](#index)

<a id="getallmarkets"></a>

### function get_all_markets():
Get all market data-hours including the hours. includes every exchange on Wealthsimple Trade.   
and has the opening and closing time amongst other data.  

[Back to top—>](#index)

<a id="getmarkethours"></a>

### function get_market_hours(exchange):
Get all data about a specific exchange.  
1.Where EXCHANGE is the ticker of the company, can be only.     
("TSX","CSE","NYSE","BATS","FINRA","OTCBB","TSX-V","NASDAQ","OTC MARKETS","AEQUITAS NEO EXCHANGE")

[Back to top—>](#index)

<a id="getwatchlist"></a>

### function get_watchlist():
Get all securities under the watchlist in this WealthSimple Trade account.      

[Back to top—>](#index)

<a id="deletewatchlist"></a>

### function delete_watchlist(sec_id):
Delete a security from watchlist under this WealthSimple Trade account.  
1.Where SEC_ID is the security id for the security you want to delete.  

[Back to top—>](#index)

<a id="addwatchlist"></a> 

### function add_watchlist(sec_id):
Add security under this WealthSimple Trade account.    
1.Where SEC_ID is the security id for the security you want to add.  

[Back to top—>](#index)

<a id="getexchangerate"></a>  

### function get_exchange_rate(self):
Current WealthSimple Trade USD/CAD exchange rates.  

[Back to top—>](#index)

<a id="usdtocad"></a>

### def usd_to_cad(self, amount):
use [Wsimple.get_exchange_rate()](#getexchangerate) to exchange to change usd to cad.   
**not working correctly**

[Back to top—>](#index) 

<a id="cadtousd"></a>

### def get_sell_usd(self, amount: float):
use [Wsimple.get_exchange_rate()](#getexchangerate) to exchange to change cad to usd.     

[Back to top—>](#index)

<a id="gettotalvalue"></a>

### def get_total_value(self):
Get the total account value of this wealthsimple account in cad.   

[Back to top—>](#index)

<a id="settings"></a>

### def settings(self):
Get settings needed for /settings route.   

[Back to top—>](#index)

<a id="dashboard"></a>

### def dashboard(self):
Get dashboard needed for /home route.   

[Back to top—>](#index)

<a id="publicfindsecuritiesbyticker"></a>

### def public_find_securities_by_ticker(ticker):  
staticmethod: get a company historical data by the ticker.    
1.Where TICKER is the ticker of the company you want to search for.    
Ex. AMZN, APPL, GOOGL, SPY. May not work on smaller companies, ETF.    
?May not work on smaller companies or ETF.    

[Back to top—>](#index)

<a id="publicfindsecuritiesbytickerhistorical"></a>

### def public_find_securities_by_ticker_historical(ticker, time):  
staticmethod: get a company historical data based on time and by the actual ticker.    
1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.  
2.Where TIME is ("1d", "1w", "1m", "3m", "1y"): DOES NOT INCLUDE ("all").   
?May not work on smaller companies or ETF.    


[Back to top—>](#index)

<a id="publictoptraded"></a>

### def public_top_traded(offset=0, limit=5):  
staticmethod: get top traded companies on wealthsimple trade.  
1.Where OFFSET is the displacement between the selected offset and the beginning.   
2.Where LIMIT is the amount of response you want from the request.  

[Back to top—>](#index)

<a id="publicfindsecuritiesnews"></a>

### def public_find_securities_news(ticker):  
staticmethod: get public news based on ticker name.    
1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.   
?May not work on smaller companies or ETF.   

[Back to top—>](#index)

<a id="publicsummarystatus"></a>
  
### def summary_status():  
staticmethod: get current summary status/incidents of wealthsimple trade.   
the summary contains data for the following systems [    
Login and Account Access, Quotes iOS app Order execution,  
Security Search, Order submission, Apps, Android App   
Order status, Trading, Market Data, Order Cancellation,   
Linking bank accounts, Deposits and Withdrawals,   
Account Values, Account Opening  
] 
the data is in JSON format in body/content, JSON is large.  
  
[Back to top—>](#index)

<a id="publiccurrentstatus"></a>

### def current_status():
staticmethod: get current status/incidents of wealthsimple trade.    
?the data is in json format in body/content, json could be large.  

[Back to top—>](#index)

<a id="publicpreviousstatus"></a> 

### def previous_status():
staticmethod: get all previous history status/incidents of wealthsimple trade.   
?the data is in json format in body/content, json is large.  

[Back to top—>](#index)

<a id="auth"></a> 

### def auth(email, password):  
staticmethod: checks if the given email and password are correct.    

[Back to top—>](#index)

## Disclaimer
  #### **DO NOT LEVERAGE THIS IN ATTEMPT TO DISRUPT ORDERLY MARKET FUNCTIONS**.
  This software is provided so you can use Wealthsimple trade on your computer duh, but you should understand that you have a responsibility to not engage in illegal trading behaviours that can disrupt orderly market functions. This means that you should not flood the website with orders in a fast manner. You might even get banned or locked out by WealthSimple Trade.

  You would be abusing this tool if you are leveraging it to carry out tactics that would provide you illegitimate personal gains. For example, [Spoofing](https://en.wikipedia.org/wiki/Spoofing_(finance)) is a forbidden tactic that has demonstrable negative effects on the operation of the markets.

  Remember when using this website you are still in agreement with Wealthsimple Trade and Crypto terms of service and they reserve the right to terminate anyone

  My recommendation is to be very conservative about how many orders you place within a small timeframe. I have no idea what the maximum amount of orders is by any timeframe, but if you have a gut feeling that it is too much, then it is too much.

  Users of [wstrade-api](https://github.com/ahmedsakr/wstrade-api) have observed that trades in excess of 7 per hour are rejected by the WealthSimple Trade servers. You can use this observation as a baseline of how many trades you can perform on an hourly basis.

  #### **USE AT YOUR OWN RISK**.
  Even though this software is 1000% secure due to everyone running an independent and secluded webserver and that no data is being sent out. But I still must say that this software is not built by or affiliated in way with Wealthsimple Trade or the company Wealthsimple. The use of this software is done at your own discretion and risk and with the agreement that you will be solely responsible for any damage to your computer system or loss of data that results from such activities. By using this software you solely responsible for any damages to you or your Wealthsimple account, and that I will not be liable for any damages that you may suffer connection with downloading, installing, using, modifying or distributing this software.

  to reiterate
  >I take NO responsibility and/or liability for how you choose to use the software. By using the software, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again, ALL software here is for PERSONAL and ONLY PERSONAL use.
