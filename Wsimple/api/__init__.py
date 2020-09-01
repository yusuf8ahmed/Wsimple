from .__main__ import Wsimple
from .errors import LoginError, InvalidAccessToken

("""
class Wsimple:
    function __init__(email, password):
        #* initializes and gets Access and Refresh tokens
        "
        The LOGIN endpoint intializes a new session for the given email and
        password set. If the login is successful, access and refresh tokens
        are returned in the headers. The access token is the key for invoking
        all other end points.
        "    
    function refresh_token():
        #* Generates a new set of access and refresh tokens.
         
    function get_account():
        #* Grabs account info of this WealthSimple Trade account.
    
    function get_historical_account_data(time: str):
        #* The HISTORY_ACCOUNT endpoint provides historical snapshots of the
        #* WealthSimple account for a specified timeframe.
        #* 1: Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] auto set 1d
        #* 2: Where ACCOUNT is the account id received from /account/list Ex. rrsp-123_abc auto set to frist accounts id
    
    function get_orders():
        #* Get all current and past orders.
    
    function _place_order(self, security_id: str, order_type: str='buy_quantity',
                    sub_type: str='market',limit_price: float=1,quantity: int = 1):
        #* Places an order for a security.

    function buymarketorder(security_id: str, limit_price: int = 1, quantity: int = 1):
        #* Places an market buy order for a security. Works
    
    function sellmarketorder(security_id: str, quantity: int =1):
        #* Places an market sell order for a security. Works

    function buylimitorder(self, security_id, limit_price,
                      account_id=None, quantity=1):
        #* NotImplementedError()

    function selllimitorder(self, security_id, limit_price,
                       account_id=None, quantity=1):
        #* NotImplementedError()

    function delete_order(order_id: str):
        #* Cancels a specific order by its id.
        #1: Where ORDER is order_id from place order
        
    function find_securities(ticker: str):
        #* Grabs information about the security resembled by the ticker
        #1: Where TICKER is the ticker of the company, wealthsimple will fuzzy 
        # match this argument and therefore multiple results can appear.

    function find_securities_by_id(self, sec_id: str) -> dict:
        #* Grabs information about the security resembled by the security id
    
    function find_securities_by_id_historical(self, sec_id: str, time: str):
        #* Grabs information about the security resembled by the security id in a a specified timeframe.
        
    function get_positions():
        #* Get all current securities held by this WealthSimple Trade account. 
        
    function get_activities():
        #* Provides the most recent 20 activities (deposits, dividends, orders, etc)
        #* on this WealthSimple Trade account.
        #?: ?type ->> ?type=deposit, ?type=dividend
        #?: ?limit ->> < 100
        #?: ?bookmark ->> where bookmark is return by each GET that can be used for the subsequent
        #?: ^> pages in following calls.
        #?: ?account-id ->> ??????
    
    function get_activities_bookmark(self, bookmark):
        #* Provides the most recent 20 activities (deposits, dividends, orders, etc)
        #* on the WealthSimple Trade account. used url query bookmark
    
    function get_me():
        #*  Get Basic info of this WealthSimple Trade account.
    
    function get_person():
        #*  Get more Advanced/Personal info of this WealthSimple Trade account.
    
    function get_bank_accounts():
        #*  Get All linked bank accounts under the WealthSimple Trade account
    
    function get_deposits():
        #*  Get All deposits under the WealthSimple Trade account
    
    #? get, add, delete securities on watchlist functions
    def get_watchlist(self):
        #* Get watchlist under this WealthSimple Trade account
          
    def delete_watchlist(self, sec_id):
        #* Delete security from watchlist under this WealthSimple Trade account 
           
    def add_watchlist(self, sec_id):
        #* Add security  under this WealthSimple Trade account
                   
    def get_exchange_rate(self):
        #* Current WealthSimple Trade USD/CAD exchange rates
    
    #? not api endpoint related
    def test_endpoint(self):
        #* test random endpoints

    def usd_to_cad(self, amount):
        #* use wealthsimple forex exchange to change usd to cad
        #not working correctly
    
    def get_sell_usd(self, amount: float):
        #* use wealthsimple forex exchange to change cad to usd
        #not working correctly

    def get_total_value(self):
        #* Get total account value of this wealthsimple account in cad 

    def dashboard(self):
        #* Get dashboard need for route "/home"
    
    @staticmethod
    def auth(email, password):
        #* checks if the given email and password is correct 
""")