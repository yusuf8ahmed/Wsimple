from .__main__ import Wsimple
from .errors import LoginError, InvalidAccessToken

("""
class Wsimple:
    function __init__(email, password):
    Initializes and sets Access and Refresh tokens. The LOGIN endpoint.    
    initializes a new session for the given email and password set. If.     
    the login is successful, access and refresh tokens are returned in.   
    the headers. The access token is the key for invoking all other endpoints.  
 
    function refresh_token():
    Generates and applies a new set of access and refresh tokens.  
    
    function get_account():
    Grabs account info of this WealthSimple Trade account.  
    
    function get_historical_account_data(time: str):
    The HISTORY_ACCOUNT endpoint provides historical snapshots of the.   
    WealthSimple account for a specified timeframe.  
    1.Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] autoset 1d.    
    2.Where ACCOUNT is the account id received from /account/list: autoset to first accounts_id.     
    
    function get_orders():
    Get all current and past orders.   
    
    function _place_order(self, security_id: str, order_type: str='buy_quantity',
                    sub_type: str='market',limit_price: float=1,quantity: int = 1):
        #* Places an order for a security.

    function buymarketorder(security_id: str, limit_price: int = 1, quantity: int = 1):
    Places a market buy order for a security. Works.  
    
    function sellmarketorder(security_id: str, quantity: int =1):
    Places a market sell order for a security. Works. 

    function buylimitorder(self, security_id, limit_price, account_id=None, quantity=1):
    Places a limit buy order for a security.    
    NotImplementedError     

    function selllimitorder(self, security_id, limit_price, account_id=None, quantity=1):
    Places a limit sell order for a security.  
    NotImplementedError  

    function delete_order(order_id: str):
    Cancels a specific order by its id.    
    1.Where ORDER is order_id from place order.    
        
    function find_securities(ticker: str):
    Grabs information about the security resembled by the ticker.    
    1.Where TICKER is the ticker of the company, API will fuzzy.     
    match this argument and therefore multiple results can appear. 

    function find_securities_by_id(self, sec_id: str) -> dict:
    Grabs information about the security resembled by the security id.  
    
    function find_securities_by_id_historical(self, sec_id: str, time: str):
    Grabs information about the security resembled by the security id in a a specified timeframe.   
    1.Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] autoset 1d.   
    ?mic=XNAS: (XNAS: "US", XNYS: "US", XTSE: "CA", XTSX: "CA", BATS: "US", NEOE: "CA").  
        
    function get_positions():
    Get all current position held by this WealthSimple Trade account.  
        
    function get_activities():
    Provides the most recent 20 activities (deposits, dividends, orders, etc).   
    on this WealthSimple Trade account.  
    ?type ->> ?type=deposit, ?type=dividend.    
    ?limit ->> less than 100.    
    ?bookmark ->> where bookmark is return by each GET that can be used for the subsequent.    
    ^> pages in following calls.    
    ?account-id ->> ??????. 
    
    function get_activities_bookmark(self, bookmark):
    Provides the last 20 activities (deposits, dividends, orders, etc) on the WealthSimple Trade.   
    account based on the url query bookmark.   
    ?bookmark ->> [long string of alphanumeric characters from the response of [Wsimple.get_activities()](#getactivities) ].   
    
    function get_me():
    Get Basic info of this WealthSimple Trade account. 
    
    function get_person():
    Get more Advanced-Personal info of this WealthSimple Trade account.    
    
    function get_bank_accounts():
    Get all linked bank accounts under the WealthSimple Trade account.   
    
    function get_deposits():
    Get all deposits under the WealthSimple Trade account.    
        
    function get_all_markets():
    Get all market data-hours including the hours. includes every exchange on Wealthsimple Trade.   
    and has the opening and closing time amongst other data.  

    function get_market_hours(exchange):
    Get all data about a specific exchange.  
    1.Where EXCHANGE is the ticker of the company, can be only.     
    ("TSX","CSE","NYSE","BATS","FINRA","OTCBB","TSX-V","NASDAQ","OTC MARKETS","AEQUITAS NEO EXCHANGE")
    
    function get_watchlist(self):
    Get all securities under the watchlist in this WealthSimple Trade account.     
          
    function delete_watchlist(self, sec_id):
    Delete a security from watchlist under this WealthSimple Trade account.  
    1.Where SEC_ID is the security id for the security you want to delete.  
           
    function add_watchlist(self, sec_id):
    Add security under this WealthSimple Trade account.    
    1.Where SEC_ID is the security id for the security you want to add.            
                   
    function get_exchange_rate(self):
    Current WealthSimple Trade USD/CAD exchange rates. 
    
    function test_endpoint(self):
    test endpoints.  

    function usd_to_cad(self, amount):
    use [Wsimple.get_exchange_rate()](#getexchangerate) to exchange to change usd to cad.   
    **not working correctly**
    
    function cad_to_usd(self, amount: float):
    use [Wsimple.get_exchange_rate()](#getexchangerate) to exchange to change cad to usd. 

    function get_total_value(self):
    Get the total account value of this wealthsimple account in cad.  

    function settings(self):
    Get settings needed for /settings route.

    function dashboard(self):
    Get dashboard needed for /home route.

    function public_find_securities_by_ticker(ticker):  
    staticmethod: get a company historical data by the ticker.    
    1.Where TICKER is the ticker of the company you want to search for.    
    Ex. AMZN, APPL, GOOGL, SPY. May not work on smaller companies, ETF.    
    ?May not work on smaller companies or ETF.    

    function public_find_securities_by_ticker_historical(ticker, time):  
    staticmethod: get a company historical data based on time and by the actual ticker.    
    1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.  
    2.Where TIME is ("1d", "1w", "1m", "3m", "1y"): DOES NOT INCLUDE ("all").   
    ?May not work on smaller companies or ETF.    

    function public_top_traded(offset=0, limit=5):  
    staticmethod: get top traded companies on wealthsimple trade.  
    1.Where OFFSET is the displacement between the selected offset and the beginning.   
    2.Where LIMIT is the amount of response you want from the request.  

    function public_find_securities_news(ticker):  
    staticmethod: get public news based on ticker name.    
    1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.   
    ?May not work on smaller companies or ETF.   
  
    function summary_status():  
    staticmethod: get current summary status/incidents of wealthsimple trade.   
    the summary contains data for the following systems [    
    Login and Account Access, Quotes iOS app Order execution,  
    Security Search, Order submission, Apps, Android App   
    Order status, Trading, Market Data, Order Cancellation,   
    Linking bank accounts, Deposits and Withdrawals,   
    Account Values, Account Opening  
    ] 
    the data is in JSON format in body/content, JSON is large.  
    
    function current_status():
    staticmethod: get current status/incidents of wealthsimple trade.    
    ?the data is in json format in body/content, json could be large.  

    function previous_status():
    staticmethod: get all previous history status/incidents of wealthsimple trade.   
    ?the data is in json format in body/content, json is large.  
    
    function auth(email, password):
    staticmethod: checks if the given email and password are correct. 
""")