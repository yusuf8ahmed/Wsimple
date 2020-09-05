#!/usr/bin/env python3
# standard library
import json
import pprint
# custom error
from .errors import LoginError, InvalidAccessToken
# third party
import requests

class Wsimple:
    # class assumes first id in account/list is for trading
    base_url = "https://trade-service.wealthsimple.com/"
    
    def __init__(self, email, password):
        """
        The LOGIN endpoint intializes a new session for the given email and
        password set. If the login is successful, access and refresh tokens
        are returned in the headers. The access token is the key for invoking
        all other end points.
        """
        payload = dict(email=email, password=password)
        r = requests.post(
            url="{}auth/login".format(self.base_url),
            data=payload
        )
        del password
        if r.status_code == 200:
            self._access_token = r.headers['X-Access-Token']
            self._refresh_token = r.headers['X-Refresh-Token']
            self._header = {'Authorization': self._access_token}
            del r
        else:
            print(r.status_code, r.content)
            raise LoginError()
            
    def refresh_token(self):
        """
        Generates a new set of access and refresh tokens.
        """
        payload = dict(refresh_token=str(self._refresh_token))
        r = requests.post(
            url="{}auth/refresh".format(self.base_url),
            data=payload,
        )
        self._access_token = r.headers['X-Access-Token']
        self._refresh_token = r.headers['X-Refresh-Token']
        self._header = {'Authorization': self._access_token}
        return r.text
         
    def get_account(self):
        """
        Grabs account info of this WealthSimple Trade account.
        """
        r = requests.get(
            url="{}account/list".format(self.base_url),
            headers=self._header
        )
        return r.json()
    
    def get_historical_account_data(self, time: str = "1d"):
        """
        The HISTORY_ACCOUNT endpoint provides historical snapshots of the
        WealthSimple account for a specified timeframe.
        """
        #1: Where TIME is one of [1d, 1w, 1m, 3m, 1y, all]
        #2: Where ACCOUNT is the account id received from /account/list Ex. rrsp-123_abc
        account = self.get_account()
        r = requests.get(
            url="{}account/history/{}?account_id={}".format(
                self.base_url, time, account["results"][0]["id"] ),
            headers=self._header
        )
        return r.json()    
    
    def get_orders(self):
        """
        Get all current and past orders.
        """
        r = requests.get(
            url="{}orders".format(self.base_url),
            headers=self._header
        )
        return r.json()
    
    def _place_order(self,
                    security_id: str,
                    order_type: str  = 'buy_quantity',
                    sub_type: str = 'market',
                    limit_price: float = 1,
                    quantity: int = 1):
        """
        Places an order for a security.
        """
        account_id = self.get_account()["results"][0]["id"]
        if order_type == "sell_quantity" and sub_type == "market":
            order_dict = {
                "account_id": account_id,
                "quantity": quantity,
                "security_id": security_id,
                "order_type": order_type,
                "order_sub_type": sub_type,
                "time_in_force": "day",
            }
        else:
            order_dict = {
                "account_id": account_id,
                "quantity": quantity,
                "security_id": security_id,
                "order_type": order_type,
                "order_sub_type": sub_type,
                "time_in_force": "day",
                "limit_price": limit_price
            }
        r = requests.post("{}orders".format(self.base_url),
                       headers=self._header,
                       json=order_dict)
        return r.json()
      
    def delete_order(self, order_id: str):
        """
        Cancels a specific order by its id.
        """
        #1: Where ORDER is order_id from place order
        r = requests.delete(
            "{}/orders/{}".format(self.base_url, order_id)
            )   
        return r.json() 
      
    def buymarketorder(self, security_id: str, limit_price: int = 1, quantity: int = 1):
        """
        Places an market buy order for a security. Works
        """
        res = self._place_order(security_id, 'buy_quantity',
                               'market', limit_price, quantity)
        return res
    
    def sellmarketorder(self, security_id: str, quantity: int =1):
        """
        Places an market sell order for a security. Works
        """
        res = self._place_order(security_id, 'sell_quantity',
                               'market', quantity=quantity)
        return res  
     
    def buylimitorder(self,
                      security_id,
                      limit_price,
                      account_id=None,
                      quantity=1):
        return NotImplementedError()

    def selllimitorder(self,
                       limit_price,
                       security_id,
                       account_id=None,
                       quantity=1):
        return NotImplementedError()

    def find_securities(self, ticker: str):
        """
        Grabs information about the security resembled by the ticker
        """
        #1: Where TICKER is the ticker of the company, wealthsimple will fuzzy match this argument 
        # and therefore multiple results can appear.
        r = requests.get(
            url="{}securities?query={}".format(self.base_url, ticker),
            headers=self._header
        )
        return r.json()
    
    def find_securities_by_id(self, sec_id: str) -> dict:
        r = requests.get(
            url="{}securities/{}".format(self.base_url, sec_id),
            headers=self._header
        )
        return r.json()
    
    def find_securities_by_id_historical(self, sec_id: str, time: str):
        """
        Get historical data of securites by id 
        #mic=XNAS
        XNAS: "US", XNYS: "US", XTSE: "CA", XTSX: "CA", BATS: "US", NEOE: "CA"
        """
        r = requests.get(
            url="{}securities/{}/historical_quotes/{}?mic=XNAS".format(self.base_url, sec_id, time),
            headers=self._header
        )
        return r.json()
    
    def get_positions(self):
        """
        Get all current securities held by this WealthSimple Trade account. 
        """
        r = requests.get(
            url="{}account/positions".format(self.base_url),
            headers=self._header
        )
        return r.json() 
        
    def get_activities(self):
        """
        Provides the most recent 20 activities (deposits, dividends, orders, etc)
        on the WealthSimple Trade account.
        #?type=deposit
        #?type=dividend
        """
        r = requests.get(
            url="{}account/activities".format(self.base_url),
            headers=self._header
        )
        return r.json() 
    
    def get_activities_bookmark(self, bookmark):
        """
        Provides the most recent 20 activities (deposits, dividends, orders, etc)
        on the WealthSimple Trade account.
        """
        r = requests.get(
            url="{}account/activities?bookmark={}".format(self.base_url, bookmark),
            headers=self._header
        )
        return r.json() 
    
    def get_me(self):
        """
        Get Basic info of this WealthSimple Trade account.
        """
        r = requests.get(
            url="{}me".format(self.base_url),
            headers=self._header
        )
        return r.json()     
    
    def get_person(self):
        """
        Get more Advanced/Personal info of this WealthSimple Trade account.
        """
        r = requests.get(
            url="{}person".format(self.base_url),
            headers=self._header
        )
        return r.json() 
    
    def get_bank_accounts(self):
        """
        All linked bank accounts under the WealthSimple Trade account
        """
        r = requests.get(
            url="{}bank-accounts".format(self.base_url),
            headers=self._header
        )
        return r.json()
    
    def get_deposits(self):
        """
        All deposits under the WealthSimple Trade account
        """
        r = requests.get(
            url="{}deposits".format(self.base_url),
            headers=self._header
        )
        return r.json()   
    
    # get, add, delete securities on watchlist functions
    def get_watchlist(self):
        """
        Get watchlist under this WealthSimple Trade account
        """
        r = requests.get(
            url="{}watchlist".format(self.base_url),
            headers=self._header
        )
        return r.json()   
  
    def delete_watchlist(self, sec_id):
        r = requests.delete(
            url="{}watchlist/{}".format(self.base_url, sec_id),
            headers=self._header
        )
        return r.json()   
           
    def add_watchlist(self, sec_id):
        r = requests.put(
            url="{}watchlist/{}".format(self.base_url, sec_id),
            headers=self._header
        )
        return r.json()  
            
    # exchange functions 
    def get_exchange_rate(self):
        """
        Current WealthSimple Trade USD/CAD exchange rates
        """
        r = requests.get(
            url="{}forex".format(self.base_url),
            headers=self._header
        )
        return r.json() 
    
    #! functions after this point are not core to the API
    def test_endpoint(self):
        """
        test endpoints
        """
        r = requests.get(
            url="{}top_traded".format(self.base_url),
            headers=self._header
        )
        print(r.status_code)
        return r.json()

    def usd_to_cad(self, amount):
        #not working correctly
        forex = self.get_exchange_rate()['USD']
        buy_rate = forex['buy_rate']
        return round(amount * buy_rate, 3)
    
    def get_sell_usd(self, amount: float):
        #not working correctly
        forex = self.get_exchange_rate()['USD']
        sell_rate = float(forex['sell_rate'])
        price = round(float(amount * sell_rate), 2)
        return price
 
    def get_total_value(self):
        account = self.get_account()["results"][0]
        account_positions = self.get_positions()['results']
        security_value = {}

        for security in account_positions:
            ticker = security["stock"]["symbol"]
            currency = security["quote"]["currency"]
            if currency == "CAD":
                amount = round(float(security["quote"]["amount"]) * security["quantity"], 3) 
            elif currency == "USD":
                # change usd to cad
                amount = round(self.usd_to_cad(float(security["quote"]["amount"])) * security["quantity"], 3)
            else:
                amount = 0
            security_value[ticker] = amount
            
        return {
            "amount": round(sum(security_value.values()) + account['buying_power']['amount'], 2),
            "currency": "CAD"
        }
        
    def get_settings(self):
        me = self.get_me()
        person = self.get_person()
        bank_account = self.get_deposits()
        exchange_rate = self.get_exchange_rate()  
        ws_current_operational_status = self.current_status()    
        return {
            'me': me,
            'person': person,
            'bank_account': bank_account,
            'exchange_rate': exchange_rate,
            'ws_current_operational_status': ws_current_operational_status  
        }
    
    def dashboard(self):
        account = self.get_account()["results"][0]
        total_value = self.get_total_value()
        watchlist = self.get_watchlist()
        positions = self.get_positions()
        account_value_graph = self.get_historical_account_data("1d")
        previous_amount = account_value_graph["previous_close_net_liquidation_value"]['amount']
        account_change = format(total_value['amount'] - previous_amount, '.2f')
        account_change_percentage = format(((total_value['amount'] - previous_amount) / previous_amount)*100, '.2f')
        return  {
                    'available_to_trade':{
                        'amount': account['buying_power']['amount'],
                        'currency': account['buying_power']['currency']
                        },
                    'account_value':{
                        'amount': total_value['amount'],
                        'currency': total_value['currency']
                        },
                    'net_deposits':{
                        'amount': account['net_deposits']['amount'],
                        'currency': account['net_deposits']['currency']
                        },
                    'available_to_withdraw':{
                        'amount': account['available_to_withdraw']['amount'],
                        'currency': account['available_to_withdraw']['currency']
                    },
                    'account_change':{
                        'amount': account_change,
                        'percentage': account_change_percentage
                    },
                    'account_value_graph': { 'table': account_value_graph },
                    'account_positions': { 'table': positions },
                    'account_watchlist': { 'table': watchlist }
                }
        
    #? public functions (can be used without login in)
    @staticmethod
    def public_find_securities_by_ticker(ticker):
        #"https://trade-service.wealthsimple.com/public/securities/" + e
        return NotImplementedError()
    
    @staticmethod
    def public_find_securities_by_ticker_historical(ticker, time):
        #https://trade-service.wealthsimple.com/public/securities/{AAPL}/historical_quotes/{1d}
        return NotImplementedError()
    
    @staticmethod
    def public_top_traded(offset=0, limit=5):
        #"https://trade-service.wealthsimple.com/public/securities/top_traded?offset="+e+"&limit="+t
        r = requests.get(
            url="""https://trade-service.wealthsimple.com/public/securities/top_traded?offset={}&limit={}""".format(offset, limit)
        )
        return r.json()
    
    @staticmethod
    def public_find_securities_news(ticker):
        r = requests.get(
            url="https://trade-service.wealthsimple.com/public/securities/{}/news".format(ticker)
        )
        return r.json()
    
    #? wealthsimple operational status also public
    @staticmethod    
    def summary_status():
        #https://status.wealthsimple.com/api/v2/summary.json
        # summary contains data for
        # [ Login and Account Access, Quotes iOS app Order execution
        # Security Search, Order submission, Apps, Android App
        # Order status, Trading, Market Data, Order Cancellation,
        # Linking bank accounts, Deposits and Withdrawals,
        # Account Values, Account Opening ]
        #json in context
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/status.json"
        )
        return json.loads(r.content)
    
    @staticmethod    
    def current_status():
        # https://status.wealthsimple.com/api/v2/status.json
        # current status
        # json in context
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/status.json"
        )
        return json.loads(r.content)
    
    @staticmethod    
    def previous_status():
        #https://status.wealthsimple.com/api/v2/incidents.json
        #previous status (very large json)
        #json in context
        return NotImplementedError()
    
    #? auth for testing
    @staticmethod
    def auth(email, password):
        """
        The LOGIN endpoint intializes a new session for the given email and
        password set. If the login is successful, access and refresh tokens
        are returned in the headers. The access token is the key for invoking
        all other end points.
        """
        payload = dict(email=email, password=password)
        r = requests.post(
            url="https://trade-service.wealthsimple.com/auth/login",
            data=payload
        )
        del password
        if r.status_code == 200:
            return "OK", r.status_code, r.text
        else:
            return "ERROR", r.status_code, r.text