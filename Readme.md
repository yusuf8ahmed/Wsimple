<p align="center">
  <a>
    <img src="app/static/media/logo64.svg">
    <br>
    <img src="https://forthebadge.com/images/badges/does-not-contain-treenuts.svg">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg">
    <img src="https://forthebadge.com/images/badges/uses-badges.svg">
    <img src="https://forthebadge.com/images/badges/designed-in-etch-a-sketch.svg">
    <img src="https://forthebadge.com/images/badges/ages-18.svg">
    <img src="https://forthebadge.com/images/badges/thats-how-they-get-you.svg">
  </a>
</p>

### What is the Wsimple project?
Welcome! This project is a web interface and API for Wealthsimple Trade. The main goal this project is to give a simple yet robust interface for Wealthsimple Trade users and also give the ability to allow developers to create projects while hooking straight into their Wealthsimple Trade account. Click [Here](#index) for API wrapper documentation. 

Please read the [disclamer](#disclamer), and due to the nature of this project and goodwill, specific endpoints aren't available as.

## Getting Started

  ### Project Status
  <p style="color:red;font-size:35px;margin:0px;">
  Pre-alpha v1.0
  </p>

  This project is in the pre-alpha stage. if you find any bugs please submit an
  [issue](https://github.com/yusuf8ahmed/Wsimple/issues/new).

  ### Prerequisites
  * python and pip is required to use/download wsimple
  * to download pip and python goto ["Download Python"](https://realpython.com/installing-python/)
    * for windows click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-windows)
    * for macos click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-macos)

  ### Installation
  ```bash
  # Production
  pip install wsimple
  # Testing
  git clone https://github.com/yusuf8ahmed/Wsimple.git
  ```
  #### start webserver
  ```bash
  # Production
  wsimple start
  # Testing
  gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 8 app:app
  ```

<a id="index"></a> 

## API

### Usage
  ```python
  from Wsimple import Wsimple

  ws = Wsimple("john.doe@gmail.com", "johndoepass")
  # Wsimple("gmail", "password")
  tokens = ws.tokens
  # holds authentication information

  print(ws.find_securities(tokens, "GOOG")) 
  # return a list of securities that include GOOG and GOOGL

  ws.make_deposit(tokens, amount=2000)
  # create deposit order for 2000 CAD into your account

  ws.get_market_hours(tokens, exchange="NYSE")
  # return opening and closing of the exchange NYSE 

  ws.current_status()
  # this method is in the misc section therefore doesn't need tokens
  # get current operation status of Wealthsimple Trade Systems
  ```
## API Methods
### Table of Contents

<details>
<summary>General</summary>
<br>

* [init()](#init)
* [access()](#access)
* [refresh_token()](#refreshtoken)
</details>

<details>
<summary>Account info</summary>
<br>

* [get_account()](#getaccount)
* [get_historical_account_data()](#gethistoricalportfoliodata)
* [get_me()](#getme)
* [get_person()](#getperson)
* [get_bank_accounts()](#getbankaccounts)
* [get_positions()](#getpositions)
</details>

<details>
<summary>Order</summary>
<br>

  * [get_orders()](#getorders)
  * [buy_market_order()](#buymarketorder)
  * [sell_market_order()](#sellmarketorder)
  * [buy_limit_order()](#buylimitorder)
  * [sell_limit_order()](#selllimitorder)
  * [delete_order()](#deleteorder)
</details>

<details>
<summary>Find securities</summary>
<br>

* [find_securities()](#findsecurities)
* [find_securities_by_id()](#findsecuritiesbyid)
* [find_securities_by_id_historical()](#findsecuritiesbyidhistorical)
</details>

<details>
<summary>Activities</summary>
<br>

* [get_activities()](#getactivities)
* [get_activities_bookmark()](#getactivitiesbookmark)
</details>

<details>
<summary>Withdrawal</summary>
<br>

* [make_withdrawal()](#makewithdrawal)
* [get_withdrawal()](#getwithdrawal)
* [list_withdrawals()](#listwithdrawals)
* [delete_withdrawal()](#deletewithdrawal)
</details>

<details>
<summary>Deposits</summary>
<br>

* [make_deposit()](#makedeposit)
* [get_deposit()](#getdeposit)
* [list_deposits()](#listdeposits)
* [delete_deposit()](#deletedeposit)
</details>

<details>
<summary>Market related</summary>
<br>

* [get_all_markets()](#getallmarkets)
* [get_market_hours()](#getmarkethours)
</details>

<details>
<summary>Watchlist</summary>
<br>

* [get_watchlist()](#getwatchlist)
* [add_watchlist()](#addwatchlist)
* [delete_watchlist()](#deletewatchlist)
</details>

<details>
<summary>Securities groups</summary>
<br>

* [get_all_securities_groups()](#getallsecuritiesgroups)
</details>

<details>
<summary>Exchange</summary>
<br>

* [get_exchange_rate()](#getexchangerate)
</details>

<details>
<summary>Fact-sheet</summary>
<br>

* [get_fact_sheets()](#getfactsheets)
</details>

<details>
<summary>Securities groups</summary>
<br>

* [get_all_securities_groups()](#getallsecuritiesgroups) 
</details>

<details>
<summary>Functions for flask app</summary>
<br>

* [settings()](#settings)
* [stock()](#stock)
* [dashboard()](#dashboard)
</details>

<details>
<summary>Miscellaneous</summary>
<br>

* [find_securities_by_ticker()](#miscfindsecuritiesbyticker)
* [find_securities_by_ticker_historical()](#miscfindsecuritiesbytickerhistorical)
* [top_traded()](#misctoptraded)
* [find_securities_news()](#miscfindsecuritiesnews)
</details>

<details>
<summary>Misc: Wealthsimple Trade operational status</summary>
<br>

* [summary_status()](#miscsummarystatus)
* [current_status()](#misccurrentstatus)
* [historical_status()](#mischistoricalstatus)
</details>

<a id="init"></a>

## Documentation



<div id="general">

### init(email, password, verbose, access_mode, tokens):

This function initializes and logs the user in using the provided *email* and 
*password*. Alternatively, *access_mode* can be set to True then, 
users can access misc functions without using a Wealthsimple Trade account.
If the login is successful, access and refresh tokens are returned in the 
header. The access token is the key for invoking all endpoints 
that are not considered misc.  

<a id="access"></a>

### access(verbose):
access misc functions without logging in

### function refresh_token(tokens):
generates and returns a new set of access and refresh tokens. 

[Back to top—>](#index)

</div>

<div id="account_functions">

  <a id="getaccount"></a>

  ### function get_account(tokens):
  Grabs account info for your Wealthsimple Trade account.   

  <a id="gethistoricalportfoliodata"></a>   

  ### function get_historical_portfolio_data(tokens, account, time):
  Grabs historical portfolio info for your Wealthsimple Trade account for a specified timeframe. 
  Where *time* is one of [1d, 1w, 1m, 3m, 1y, all]: defaults to 1d.    
  Where *account* is the account_id received from [get_account()](#getaccount): defaults to first accounts_id.     

  <a id="getme"></a>

  ### function get_me(tokens):
  Grabs basic information about your Wealthsimple Trade account.    

  <a id="getperson"></a> 

  ### function get_person(tokens):
  Grabs personal information about your Wealthsimple Trade account. 

  <a id="getbankaccounts"></a>  

  ### function get_bank_accounts(tokens):
  Grabs all bank accounts under your Wealthsimple Trade account. 

  <a id="getpositions"></a>

  ### function get_positions(tokens):
  Grabs all securities held by your Wealthsimple Trade account.    

  [Back to top—>](#index)
</div>

<div id="order_functions">

  <a id="getorders"></a>

  ### function get_orders(tokens):
  Grabs all orders under your Wealthsimple Trade account.   

  <a id="buymarketorder"></a>

  ### function market_buy_order(tokens, security_id, account_id, limit_price, quantity):
  Places a market buy order under your Wealthsimple Trade account.  

  <a id="sellmarketorder"></a>  

  ### function market_sell_order(tokens, security_id, account_id, quantity):
  Places a market sell order under your Wealthsimple Trade account. 

  <a id="buylimitorder"></a>

  ### limit_buy_order(tokens, security_id, limit_price, account_id,quantity, gtc):
  Places a limit buy order under your Wealthsimple Trade account.  

  <a id="selllimitorder"></a>

  ### limit_sell_order(tokens, limit_price, security_id, account_id, quantity, gtc):
  Places a limit sell order under your Wealthsimple Trade account. 
 
  <a id="stoplimitbuyorder"></a> 

  ### stop_limit_buy_order(tokens, stop, limit_price, security_id, account_id, quantity, gtc):
  Places a stop limit buy order under your Wealthsimple Trade account: NotImplementedError

  <a id="stoplimitsellorder"></a>

  ### stop_limit_sell_order(tokens, stop, limit_price, security_id, account_id, quantity, gtc):
  Places a stop limit sell order under your Wealthsimple Trade account: NotImplementedError

  <a id="deleteorder"></a>

  ### delete_order(tokens, order)
  Cancels a order by its id.    
  Where *order* is order_id from the return of the above functions.    

  [Back to top—>](#index)

</div>

<div id="securities_functions">

  <a id="findsecurities"></a>

  ### find_securities(tokens, ticker):
  Grabs information about the security resembled by the ticker.    
  Where *ticket* is the ticker of the company, API will fuzzy.     
  match this argument and therefore multiple results can appear.   

  <a id="findsecuritiesbyid"></a>

  ### find_securities_by_id(tokens, sec_id):
  Grabs information about the security by the security id. 
  Where *sec_id* is the internal security id of the security    

  <a id="findsecuritiesbyidhistorical"></a>

  ### find_securities_by_id_historical(tokens, sec_id, time):
  Grabs historical information about the security by the security id in a specified timeframe.
  Where *sec_id* is the internal security id of the security    
  Where *time_ is the timeframe one of [1d, 1w, 1m, 3m, 1y, all] defaults to "1d".
  Where *mic* is the Market Identifier Code for the exchange defaults to "XNAS" 

  [Back to top—>](#index)

</div>

<div id="activities_functions">

  <a id="getactivities"></a>    

  ### get_activities(tokens, account_id, limit, type):
  Provides the most recent 20 activities (deposits, dividends, orders, etc).   
  on this WealthSimple Trade account.  
  Where type is the activites type you want can be ["deposit", "withdrawal", "dividend", "buy", "sell"] defaults to "all"
  Where limit is the limitation of the response has to be less than 100 defaults to 20.       
  Where account_id is the id of your Wealthsimple Trade account.

  <a id="getactivitiesbookmark"></a>   

  ### get_activities_bookmark(tokens, bookmark):
  Provides the last 20 activities on the WealthSimple Trade based on the bookmark.   
  Where bookmark is the string that is that is in the response of [get_activities()](#getactivities). 

  [Back to top—>](#index)

</div>

<div id="withdrawals_functions">

  <a id="makewithdrawal"></a>  

  ### make_withdrawal(tokens, amount, currency, bank_account_id, account_id):
  make a withdrawal under your Wealthsimple Trade account.
  Where *amount* is the amount to withdraw
  Where *currency* is the currency need to be withdrawn(only CAD): defaults to "CAD"
  Where *bank_account_id* is id of bank account where the money is going to be withdrawn from (can be found in get_bank_accounts function)
  if bank_account_id is not passed then it will pick the first result.
  Where *account_id* is id of the account that is withdrawing the money (can be found in get_account function).
  if account_id is not passed then it will pick the first result.

  <a id="getwithdrawal"></a>  

  ### get_withdrawal(tokens, funds_transfer_id):
  Get specific withdrawal under this Wealthsimple Trade account.
  Where funds_transfer_id is the id of the transfer and is in the result of [make_withdrawal()](#makewithdrawal) function
  but can be also found in [list_withdrawals()](#listwithdrawals) function  

  <a id="listwithdrawals"></a>  

  ### list_withdrawals(tokens):
  Get all withdrawals under your Wealthsimple Trade account.

  <a id="deletewithdrawal"></a>  

  ### delete_withdrawal(tokens, funds_transfer_id):
  Delete a specific withdrawal your Wealthsimple Trade account.
  
  [Back to top—>](#index)

</div>

<div id="deposit_functions">

  <a id="makedeposit"></a>  

  ### make_deposit(tokens, amount, currency, bank_account_id, account_id):
  make a deposit under your Wealthsimple Trade account.
  Where *amount* is the amount to deposit
  Where *currency* is the currency need to be transferred(Only CAD): defaults to "CAD"
  Where *bank_account_id* is id of bank account where the money is going to be deposited to
  (can be found in [get_bank_accounts()](#getbankaccounts))
  if bank_account_id is not passed then it will pick the first result.
  Where *account_id* is id of the account that is depositing the money (can be found in [get_account()](#getaccount)).
  if account_id is not passed then it will pick the first result.

  <a id="getdeposit"></a>  

  ### get_deposit(tokens, funds_transfer_id):
  Get specific deposit under this WealthSimple Trade account.
  Where *funds_transfer_id* is the id of the transfer and is in the result
  of make_deposit function but can be also found in list_deposits function

  <a id="listdeposits"></a>  

  ### list_deposits(tokens):
  Get all deposits under your WealthSimple Trade account.

  <a id="deletedeposit"></a>  

  ### delete_deposit(tokens, funds_transfer_id):
  Delete a specific deposit under your WealthSimple Trade account.
  
  [Back to top—>](#index)

</div>

<div id="market_functions">

  <a id="getallmarkets"></a>

  ### get_all_markets(tokens):
  Get all market data-hours including the hours. includes every exchange on Wealthsimple Trade.   
  and has the opening and closing time amongst other data.  

  <a id="getmarkethours"></a>

  ### get_market_hours(tokens, exchange):
  Get all data about a specific exchange.  
  Where *exchange* is the ticker of the company, can be only.     
  ("TSX","CSE","NYSE","BATS","FINRA","OTCBB","TSX-V","NASDAQ","OTC MARKETS","AEQUITAS NEO EXCHANGE")

  [Back to top—>](#index)

</div>

<div id="watchlist_functions">

  <a id="getwatchlist"></a>

  ### get_watchlist(tokens):
  Get all watchlisted securities in your Wealthsimple Trade account.     

  <a id="addwatchlist"></a> 

  ### add_watchlist(tokens, sec_id):
  Add security to watchlist under your Wealthsimple Trade account.    
  Where  *sec_id* is the security id for the security you want to add.  

  <a id="deletewatchlist"></a>

  ### delete_watchlist(tokens, sec_id):
  Delete a watchlisted securities in your WealthSimple Trade account.  
  Where *sec_id* is the security id for the security you want to delete.  

  [Back to top—>](#index)

</div>

<div id="exchange_rate_functions">

  <a id="getexchangerate"></a>  

  ### get_exchange_rate(tokens):
  Current WealthSimple Trade USD/CAD exchange rates.  

  [Back to top—>](#index)

</div>

<div id="fact_sheet_functions">

  <a id="getfactsheets"></a>  

  ### get_fact_sheets(tokens):
  Get all fact sheets under your Wealthsimple trade account

  [Back to top—>](#index)

</div>

<div id="securities_groups_functions">

  <a id="getallsecuritiesgroups"></a>  

  ### get_all_securities_groups(tokens, offset, limit, sort_order):
  Grabs all security groups under Wealthsimple trade
  Where *offset* is >= 0 and defaults to 0
  Where *limit* is the limitation of the response, has to be greater than 1
  and less than 250 and defaults to 25
  Where *sort_order* is order of the results and can be ["asc", "desc"] defaults to "desc"

  [Back to top—>](#index)

</div>

<div id="not_core_functions">

  <a id="settings"></a>

  ### settings(tokens):
  Get settings needed for /settings route.   

  <a id="stock"></a>

  ### stock(tokens, sec_id, time):
  Get stock info needed for /stock/(sec_id) route.   

  <a id="dashboard"></a>

  ### dashboard(tokens):
  Get dashboard needed for /home route.   

  [Back to top—>](#index)

### Miscellaneous Functions (No login or tokens needed)

<div id="misc_functions">

  <a id="miscfindsecuritiesbyticker"></a>

  ### find_securities_by_ticker(ticker):  
  staticmethod: get a company historical data by the ticker.    
  Where *ticker* is the ticker of the company/ETF ["AMZN", "APPL", "GOOGL", "SPY"].   
  May not work on smaller companies, ETFs.    

  <a id="miscfindsecuritiesbytickerhistorical"></a>

  ### find_securities_by_ticker_historical(ticker, time):  
  staticmethod: get a company historical data based on time and by the actual ticker.    
  Where *ticker* is the ticker of the company or ETF. ["AMZN", "APPL", "GOOGL", "SPY"]. 
  Where *time* is ("1d", "1w", "1m", "3m", "1y") 
  May not work on smaller companies or ETF.    

  <a id="misctoptraded"></a>

  ### top_traded(offset, limit):  
  staticmethod: get top traded companies on Wealthsimple trade.  
  Where *OFFSET* is the index of where the response will begin. defaults to 0 
  Where *LIMIT* is the limit response. defaults to 5

  <a id="miscfindsecuritiesnews"></a>

  ### find_securities_news(ticker):  
  staticmethod: get news based on ticker name.    
  Where *ticker* is the ticker of the company or ETF. ["AMZN", "APPL", "GOOGL", "SPY"].   
  May not work on smaller companies or ETF. 

  [Back to top—>](#index)

  <a id="miscsummarystatus"></a>
    
  ### summary_status():  
  staticmethod: get current operation status/incidents of Wealthsimple trade Systems.   
  the summary contains data for the following Wealthsimple Trade Systems [  
  Login and Account Access,  
  Account Values,  
  Account Opening,   
  Deposits and Withdrawals,     
  Linking bank accounts,  
  Trading, Order execution, Order submission, Order status, Order Cancellation,     
  Market Data, Quotes, Security Search,    
  Apps, Android App, iOS app]   
  the response is very large. 
    
  <a id="misccurrentstatus"></a>

  ### current_status():
  staticmethod: get current status/incidents of Wealthsimple trade.    
  the response could be very large. 

  <a id="mischistoricalstatus"></a> 

  ### historical_status():
  staticmethod: get all historical status/incidents of wealthsimple trade.   
  the response is very large.

  [Back to top—>](#index)

</div>
</div>

<a id="disclamer"></a> 

## Disclaimer 
  #### **DO NOT LEVERAGE THIS IN ATTEMPT TO DISRUPT ORDERLY MARKET FUNCTIONS**.
  This software is provided so you can use Wealthsimple trade on your computer. This software is not built or maintained by Wealthsimple Trade or the company Wealthsimple. Remember your responsibility to not engage in illegal or unethical trading behaviours that can disrupt orderly market functions. Flooding the website/api with orders in a short timeframe may result in getting banned or locked out by Wealthsimple Trade.

  Remember when using this website/api you are still under Wealthsimple Trade services and they reserve the right to terminate anyone.

  Users of [wstrade-api](https://github.com/ahmedsakr/wstrade-api) have observed that trades in excess of 7 per hour are rejected by the WealthSimple Trade servers. You can use this observation as a baseline of how many trades you can perform on an hourly basis.

  This product was built with security in mind. This software was made to run personal and local webserver and to assure no data/credentials is being sent out. 
  
  The use of this software is done at your own discretion and risk and with the agreement that you will be solely responsible for any damages. By using this software you agree that you are solely responsible for any damages incurred to you or your account, and that I will not be liable for any damages that you may suffer in connection with downloading, installing, using, modifying or distributing this software.

  Parts of this disclaimer are adapted from [wstrade-api](https://github.com/ahmedsakr/wstrade-api)
