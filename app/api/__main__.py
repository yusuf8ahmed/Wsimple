#!/usr/bin/env python3
# standard library
import sys
import json
import pprint
import datetime
from loguru import logger
from typing import Union, Optional
# custom error
from .errors import LoginError, InvalidAccessTokenError
# third party
import requests

class Wsimple:
    # class assumes first id in account/list is for trading
    base_url = "https://trade-service.wealthsimple.com/"
    exh_to_mic = {
        "TSX": "XTSE",
        "CSE": "XCNQ",        
        "NYSE": "XNYS",
        "BATS": "BATS",
        "FINRA": "FINR",        
        "OTCBB": "XOTC",                
        "TSX-V": "XTSX",        
        "NASDAQ": "XNAS",
        "OTC MARKETS": "OTCM",
        "AEQUITAS NEO EXCHANGE": "NEOE"
    }
    
    def __init__(self, email, password, verbose=False, access_mode=False, tokens=""):
        """
        Initializes and sets Access and Refresh tokens. The LOGIN endpoint.    
        initializes a new session for the given email and password set. If.     
        the login is successful, access and refresh tokens are returned in.   
        the headers. The access token is the key for invoking all other endpoints.
        """
        self.logger = logger
        self.logger.add("logfiles/file_{time}.log",  rotation="24:00")
        self.logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="DEBUG")
        self.access_mode = access_mode
        self.verbose = verbose   
        if self.access_mode:
            pass
        else:
            payload = dict(email=email, password=password)
            r = requests.post(
                url="{}auth/login".format(self.base_url),
                data=payload
            )
            del password
            if r.status_code == 200:
                self._access_token = r.headers['X-Access-Token']
                self._refresh_token = r.headers['X-Refresh-Token']
                self.tokens = [{'Authorization': self._access_token}, {"refresh_token": self._refresh_token}]
                del r
            else:
                raise LoginError()
    
    @classmethod
    def access(cls, verbose=False):
        """
        access api by using tokens
        """
        wsimple = cls("", "", verbose=verbose, access_mode=True)
        return wsimple
            
    def refresh_token(self, tokens):
        """
        Generates and applies a new set of access and refresh tokens.  
        """
        try:
            r = requests.post(
                url="{}auth/refresh".format(self.base_url),
                data=tokens[1],
            )
            self._access_token = r.headers['X-Access-Token']
            self._refresh_token = r.headers['X-Refresh-Token']
            return [{'Authorization': self._access_token}, {"refresh_token": self._refresh_token}]
        except BaseException as e:
            self.logger.error(e)
     
    #! account related functions     
    def get_account(self, tokens):
        """
        Grabs account info of this WealthSimple Trade account. 
        """
        r = requests.get(
            url="{}account/list".format(self.base_url),
            headers=tokens[0]
        )         
        if r.status_code == 401:
            print("get account info InvalidAccessTokenError")
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_historical_account_data(self, tokens, time: str = "1d"):
        """
        The HISTORY_ACCOUNT endpoint provides historical snapshots of the.   
        WealthSimple account for a specified timeframe.  
        1.Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] autoset 1d.    
        2.Where ACCOUNT is the account id received from /account/list: autoset to first accounts_id.  
        """
        try:
            logger.debug("get historical account data")
            account = self.get_account(tokens)["results"][0]["id"]
            r = requests.get(
                url="{}account/history/{}?account_id={}".format(self.base_url, time, account),
                headers=tokens[0]
            )
            logger.debug(f"get historical account data status code {r.status_code}")
            if r.status_code == 401:
                raise InvalidAccessTokenError
            else:
                return r.json()    
        except BaseException as e:
            logger.error(e)
   
    def get_me(self, tokens):
        """
        Get Basic info of this WealthSimple Trade account.
        """
        try: 
            logger.debug("get me info")
            r = requests.get(
                url="{}me".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError
            else:
                return r.json()                                    
        except BaseException as e:
            logger.error(e)   
    
    def get_person(self, tokens):
        """
        Get more Advanced-Personal info of this WealthSimple Trade account. 
        """
        try: 
            logger.debug("get person info")
            r = requests.get(
                url="{}person".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()
            return r.json()                                   
        except BaseException as e:
            logger.error(e) 
    
    def get_bank_accounts(self, tokens):
        """
        Get all linked bank accounts under the WealthSimple Trade account.
        """
        try: 
            logger.debug("get bank accounts")
            r = requests.get(
                url="{}bank-accounts".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                                  
        except BaseException as e:
            logger.error(e) 
       
    def get_positions(self, tokens):
        """
        Get all current position held by this WealthSimple Trade account. 
        """
        try: 
            logger.debug("get positions")
            r = requests.get(
                url="{}account/positions".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                       
        except BaseException as e:
            logger.error(e)
  
    #! order functions   
    def get_orders(self, tokens):
        """
        Get all current and past orders.
        """
        try:
            logger.debug("get orders")
            r = requests.get(
                url="{}orders".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()
        except BaseException as e:
            logger.error(e)
    
    def _place_order(self,
                     tokens: str,
                     security_id: str,
                     account_id: str,
                     order_type: str = 'buy_quantity',
                     sub_type: str = 'market',
                     limit_price: float = 1,
                     quantity: int = 1,
                     gtc: bool = False):
        """
        Places an order for a security.
        """
        try:
            assert (order_type == 'sell_quantity' or 'buy_quantity')
            assert (sub_type == 'market' or sub_type == 'limit')
            if gtc:
                time_in_force = 'until_cancel'
            else:
                time_in_force = 'day'
            if order_type == "sell_quantity" and sub_type == "market":
                order_dict = {
                    "account_id": account_id,
                    "quantity": quantity,
                    "security_id": security_id,
                    "order_type": order_type,
                    "order_sub_type": sub_type,
                    "time_in_force": time_in_force,
                }
            else:
                order_dict = {
                    "account_id": account_id,
                    "quantity": quantity,
                    "security_id": security_id,
                    "order_type": order_type,
                    "order_sub_type": sub_type,
                    "time_in_force": time_in_force,
                    "limit_price": limit_price
                }
            r = requests.post("{}orders".format(self.base_url),
                        headers=tokens[0],
                        json=order_dict)
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()
        except BaseException as e:
            logger.error(e)

    def buy_market_order(self,
                         tokens,
                         security_id: str,
                         account_id: Optional[str] = None,
                         limit_price: int = 1,
                         quantity: int = 1):
        """
        Places a market buy order for a security. Works.  
        """
        try:
            logger.debug("buy market order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"] 
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type = 'buy_quantity',
                                    sub_type = 'market',
                                    limit_price = limit_price,
                                    quantity = quantity
                                    )
            return res                 
        except BaseException as e:
            logger.error(e)

    def sell_market_order(self,
                          tokens,
                          security_id: str,
                          account_id: Optional[str] = None,
                          quantity: int = 1):
        """
        Places a market sell order for a security. Works.
        """
        try: 
            logger.debug("sell market order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"] 
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type = 'sell_quantity',
                                    sub_type = 'market',
                                    quantity = quantity)
            return res               
        except BaseException as e:
            logger.error(e)

    def buy_limit_order(self, 
                        tokens, 
                        security_id, 
                        limit_price, 
                        account_id: Optional[str] = None,
                        quantity = 1, 
                        gtc = False):
        """
        Places a limit buy order for a security.    
        """
        try: 
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"] 
            logger.debug("buy limit order")
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type = 'buy_quantity',
                                    sub_type = 'limit',
                                    limit_price = limit_price,
                                    quantity = quantity,
                                    gtc = gtc)
            return res          
        except BaseException as e:
            logger.error(e)

    def sell_limit_order(self,
                         tokens,
                         limit_price,
                         security_id, 
                         account_id: Optional[str] = None,
                         quantity = 1,
                         gtc = False):
        """
        Places a limit sell order for a security.  
        """
        try: 
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"] 
            logger.debug("sell limit order")
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type = 'sell_quantity',
                                    sub_type = 'limit',
                                    limit_price = limit_price,
                                    quantity = quantity,
                                    gtc = gtc)
            return res 
            return NotImplementedError()            
        except BaseException as e:
            logger.error(e)
    
    def delete_order(self, tokens, order: str):
        """
        Cancels a specific order by its id.    
        1.Where ORDER is order_id from place order. 
        """
        try: 
            logger.debug("delete order")
            r = requests.delete(
                "{}/orders/{}".format(self.base_url, order),
                headers=tokens[0]
                )   
            return r.json()                        
        except BaseException as e:
            logger.error(e)

    #! find securitites functions
    def find_securities(self, tokens, ticker: str):
        """
        Grabs information about the security resembled by the ticker.    
        1.Where TICKER is the ticker of the company, API will fuzzy.     
        match this argument and therefore multiple results can appear. 
        """
        try: 
            logger.debug("find securities")
            r = requests.get(
                url="{}securities?query={}".format(self.base_url, ticker),
                headers=tokens[0]
            )
            print(r.status_code)
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                   
        except BaseException as e:
            logger.error(e)
    
    def find_securities_by_id(self, tokens, sec_id: str = "1d") -> dict:
        """
        Grabs information about the security resembled by the security id.
        """
        try: 
            logger.debug("find securities by id")
            r = requests.get(
                url="{}securities/{}".format(self.base_url, sec_id),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                       
        except BaseException as e:
            logger.error(e)
    
    def find_securities_by_id_historical(self, tokens, sec_id: str, time: str, mic: str = "XNAS"):
        """
        Grabs information about the security resembled by the security id in a a specified timeframe.   
        1.Where TIME is one of [1d, 1w, 1m, 3m, 1y, all] autoset 1d.   
        ?mic=XNAS: (XNAS: "US", XNYS: "US", XTSE: "CA", XTSX: "CA", BATS: "US", NEOE: "CA").   
        """
        try: 
            logger.debug("find securities by id historical")
            r = requests.get(
                url="{}securities/{}/historical_quotes/{}?mic={}".format(self.base_url, sec_id, time, mic),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                      
        except BaseException as e:
            logger.error(e)   
   
    #! activities functions      
    def get_activities(self, tokens):
        """
        Provides the most recent 20 activities (deposits, dividends, orders, etc).   
        on this WealthSimple Trade account.  
        ?type ->> ?type=deposit, ?type=dividend.    
        ?limit ->> less than 100.    
        ?bookmark ->> where bookmark is return by each GET that can be used for the subsequent.    
        ^> pages in following calls.    
        ?account-id ->> ??????. 
        """
        try: 
            logger.debug("get activities")
            r = requests.get(
                url="{}account/activities".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                     
        except BaseException as e:
            logger.error(e)
    
    def get_activities_bookmark(self, tokens, bookmark):
        """
        Provides the last 20 activities (deposits, dividends, orders, etc) on the WealthSimple Trade.   
        account based on the url query bookmark.   
        ?bookmark ->> [long string of alphanumeric characters from the response of [Wsimple.get_activities()](#getactivities) ].   
        """
        try: 
            logger.debug("get activities bookmark")
            r = requests.get(
                url="{}account/activities?bookmark={}".format(self.base_url, bookmark),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                                   
        except BaseException as e:
            logger.error(e)
 
    #! withdrawal functions (Not ADDED)
    def make_withdrawal(self, tokens, amount: int, currency: str = "CAD", bank_account_id: str = None, account_id: str = None):
        """
        make a withdrawal under this WealthSimple Trade account.
        1.Where amount is the amount to withdraw
        2.Where currency is the currency need to be withdrawn(only CAD): autoset to "CAD"
        3.Where bank_account_id is id of bank account where the money is going to be withdrawn from (can be found in get_bank_accounts function)
        if bank_account_id is not passed then it will pick the first result.
        4.Where account_id is id of the account that is withdrawing the money (can be found in get_account function).
        if account_id is not passed then it will pick the first result.
        """
        if bank_account_id == None:
            bank_account_id = self.get_bank_accounts()["results"][0]["id"] 
        if account_id == None:
            account_id = self.get_account()["results"][0]["id"]
        person = self.get_person()
        payload = {
            "bank_account_id": str(bank_account_id),
            "account_id": str(account_id),
            "client_id": str(person["id"]),
            "withdrawal_type": "full",
            "withdrawal_reason": "other",
            "withdrawal_reason_details": "other",
            "amount": float(amount),
            "currency": str(currency)
        }
        r = requests.post(
            url='{}withdrawals'.format(self.base_url),
            headers=tokens[0],
            data=payload
        )
        if r.status_code == 401:
            raise InvalidAccessTokenError()        
        return r.json()
     
    def get_withdrawal(self, tokens, funds_transfer_id: str):
        """
        Get specific withdrawal under this WealthSimple Trade account.
        1.Where funds_transfer_id is the id of the transfer and is in the result of make_withdrawal function
        but can be also found in list_withdrawals function
        """
        try: 
            logger.debug("get withdrawal")
            r = requests.get(
                url="{}withdrawals/{}".format(self.base_url, funds_transfer_id),
                headers=tokens[0]
            )
            return r.json()                                  
        except BaseException as e:
            logger.error(e) 
             
    def list_withdrawals(self, tokens):
        """
        Get all withdrawals under this WealthSimple Trade account.
        """
        try: 
            logger.debug("list withdrawals")
            r = requests.get(
                url="{}withdrawals".format(self.base_url),
                headers=tokens[0]
            )
            return r.json()                                  
        except BaseException as e:
            logger.error(e)  
    
    def delete_withdrawal(self, tokens, funds_transfer_id: str):
        """
        Delete a specific withdrawals under this WealthSimple Trade account.
        """
        try: 
            logger.debug("delete withdrawal")
            r = requests.delete(
                url="{}withdrawals/{}".format(self.base_url, funds_transfer_id),
                headers=tokens[0]
            )
            return r.json()                                  
        except BaseException as e:
            logger.error(e)     
 
    #! deposits functions
    def make_deposit(self, tokens, amount: int, currency: str = "CAD", bank_account_id: str = None, account_id: str = None):
        """
        make a deposit under this WealthSimple Trade account.
        1.Where amount is the amount to deposit
        2.Where currency is the currency need to be transferred(Only CAD): autoset to "CAD"
        3.Where bank_account_id is id of bank account where the money is going to be deposited to (can be found in get_bank_accounts function)
        if bank_account_id is not passed then it will pick the first result.
        4.Where account_id is id of the account that is depositing the money (can be found in get_account function).
        if account_id is not passed then it will pick the first result.
        """
        logger.debug("make deposits")
        if bank_account_id == None:
            bank_account_id = self.get_bank_accounts()["results"][0]["id"] 
        if account_id == None:
            account_id = self.get_account()["results"][0]["id"]
        person = self.get_person()
        payload = {
            "client_id": str(person["id"]),
            "bank_account_id": str(bank_account_id),
            "account_id": str(account_id),
            "amount": float(amount),
            "currency": str(currency)
        }
        r = requests.post(
            url='{}deposits'.format(self.base_url),
            headers=tokens[0],
            data=payload
        )
        return r.json()
     
    def get_deposit(self, tokens, funds_transfer_id: str):
        """
        Get specific deposit under this WealthSimple Trade account.
        1.Where funds_transfer_id is the id of the transfer and is in the result of make_deposit function
        but can be also found in list_deposits function
        """
        try: 
            logger.debug("get deposits")
            r = requests.get(
                url="{}deposits/{}".format(self.base_url, funds_transfer_id),
                headers=tokens[0]
            )
            return r.json()                                  
        except BaseException as e:
            logger.error(e) 
             
    def list_deposits(self, tokens):
        """
        Get all deposits under this WealthSimple Trade account.
        """
        try: 
            logger.debug("list deposits")
            r = requests.get(
                url="{}deposits".format(self.base_url),
                headers=tokens[0]
            )
            return r.json()                                  
        except BaseException as e:
            logger.error(e)  
    
    def delete_deposit(self, tokens, funds_transfer_id: str):
        """
        Delete a specific deposit under this WealthSimple Trade account.
        """
        try: 
            logger.debug("delete deposits")
            r = requests.delete(
                url="{}deposits/{}".format(self.base_url, funds_transfer_id),
                headers=tokens[0]
            )
            return r.json()                                  
        except BaseException as e:
            logger.error(e)     
    
    #! market related functions
    def get_all_markets(self, tokens):
        """
        Get all market data-hours including the hours. includes every exchange on Wealthsimple Trade.   
        and has the opening and closing time amongst other data.  
        """
        try: 
            logger.debug("get all market")
            r = requests.get(
                url='{}markets'.format(self.base_url),
                headers=tokens[0]
            )            
            return r.json()                                  
        except BaseException as e:
            logger.error(e)  
            
    def get_market_hours(self, tokens, exchange: str):
        """
        Get all data about a specific exchange.  
        1.Where EXCHANGE is the ticker of the company, can be only.     
        ("TSX","CSE","NYSE","BATS","FINRA","OTCBB","TSX-V","NASDAQ","OTC MARKETS","AEQUITAS NEO EXCHANGE")
        """
        try: 
            exchanges = list(self.exh_to_mic.keys())
            if exchange in exchanges:
                all_markets = self.get_all_markets(tokens)['results'] 
                for market in all_markets:
                    if market["exchange_name"] == exchange:
                        return market 
            else:
                return {}              
        except BaseException as e:
            logger.error(e) 
        
    #! watchlist functions
    def get_watchlist(self, tokens):
        """
        Get all securities under the watchlist in this WealthSimple Trade account. 
        """
        try: 
            logger.debug("get watchlist")
            r = requests.get(
                url="{}watchlist".format(self.base_url),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()
            return r.json()                                  
        except BaseException as e:
            logger.error(e)  
  
    def add_watchlist(self, tokens, sec_id):
        """
        Add security under this WealthSimple Trade account.    
        1.Where SEC_ID is the security id for the security you want to add.            
        """
        try: 
            logger.debug("add_watchlist")
            r = requests.put(
                url="{}watchlist/{}".format(self.base_url, sec_id),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                                 
        except BaseException as e:
            logger.error(e)   
             
    def delete_watchlist(self, tokens, sec_id):
        """
        Delete a security from watchlist under this WealthSimple Trade account.  
        1.Where SEC_ID is the security id for the security you want to delete.  
        """
        try: 
            logger.debug("delete watchlist")
            r = requests.delete(
                url="{}watchlist/{}".format(self.base_url, sec_id),
                headers=tokens[0]
            )
            if r.status_code == 401:
                raise InvalidAccessTokenError()            
            return r.json()                                 
        except BaseException as e:
            logger.error(e) 
                       
    #! exchange functions 
    def get_exchange_rate(self, tokens):
        """
        Current WealthSimple Trade USD/CAD exchange rates. 
        """
        try: 
            logger.debug("get exchange rate")
            r = requests.get(
                url="{}forex".format(self.base_url),
                headers=tokens[0]
            )
            return r.json()                               
        except BaseException as e:
            logger.error(e) 
    
    #! fact-sheet functions
    def get_fact_sheets(self, tokens):
        """
        Get all fact-sheet you have access to on this Wealthsimple account
        It shows ETFs fact sheets.
        """
        try: 
            logger.debug("get_fact_sheets")
            r = requests.get(
                url='{}fact-sheets'.format(self.base_url),
                headers=tokens[0]
            )
            return r.json()                               
        except BaseException as e:
            logger.error(e) 
    
    #! functions after this point are not core to the API
    def test_endpoint(self, tokens):
        logger.debug("test endpoint")
        r = requests.get(
            url='{}'.format(self.base_url),
            headers=tokens[0]
        )
        print(r.status_code)
        print(r.content)
        print(r.json())
        return r.json()

    def usd_to_cad(self, tokens, amount: Union[float, int]) -> float:
        """
        use Wsimple.get_exchange_rate() to exchange to change usd to cad.   
        **not working correctly**
        """
        logger.debug("usd to cad")
        forex = self.get_exchange_rate(tokens)['USD']
        buy_rate = forex['buy_rate']
        return round(amount * buy_rate, 3)
    
    def cad_to_usd(self, tokens, amount: Union[float, int]) -> float:
        """
        use Wsimple.get_exchange_rate() to exchange to change cad to usd. 
        """
        logger.debug("cad to usd")
        forex = self.get_exchange_rate(tokens)['USD']
        sell_rate = forex['sell_rate']
        return round(amount * sell_rate, 2)
 
    def get_total_value(self, tokens):
        """
        Get the total account value of this wealthsimple account in cad. 
        """
        logger.debug("get total value")
        account = self.get_account(tokens)["results"][0]
        account_positions = self.get_positions(tokens)['results']
        security_value = {}

        for security in account_positions:
            ticker = security["stock"]["symbol"]
            currency = security["quote"]["currency"]
            if currency == "CAD":
                amount = round(float(security["quote"]["amount"]) * security["quantity"], 3) 
            elif currency == "USD":
                amount = round(self.usd_to_cad(tokens, float(security["quote"]["amount"])) * security["quantity"], 3)
            else:
                amount = 0
            security_value[ticker] = amount
            
        return {
            "amount": round(sum(security_value.values()) + account['buying_power']['amount'], 2),
            "currency": "CAD"
        }
        
    def settings(self, tokens):
        """
        Get settings needed for /settings route.
        """
        logger.debug("settings")
        me = self.get_me(tokens)
        person = self.get_person(tokens)
        bank_account = self.get_deposits(tokens)
        exchange_rate = self.get_exchange_rate(tokens)  
        ws_current_operational_status = self.current_status()    
        return {
            'me': me,
            'person': person,
            'bank_account': bank_account,
            'exchange_rate': exchange_rate,
            'ws_current_operational_status': ws_current_operational_status  
        }
    
    def dashboard(self, tokens):
        """
        Get dashboard needed for /home route.
        """
        try:
            account = self.get_account(tokens)
            account = account["results"][0]
            total_value = self.get_total_value(tokens)
            watchlist = self.get_watchlist(tokens)
            positions = self.get_positions(tokens)
            account_value_graph = self.get_historical_account_data(tokens)
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
                        'account_value_graph': {
                            'table': account_value_graph 
                            },
                        'account_positions': { 
                            'table': positions 
                            },
                        'account_watchlist': { 
                            'table': watchlist 
                            }
                    }
        except InvalidAccessTokenError:
            print("dashboard InvalidAccessTokenError")
            raise InvalidAccessTokenError
        
    #! all functions after here are public and (can be used without logging in).
    @staticmethod
    def public_find_securities_by_ticker(ticker):
        """
        staticmethod: get a company historical data by the ticker.    
        1.Where TICKER is the ticker of the company you want to search for.    
        Ex. AMZN, APPL, GOOGL, SPY. May not work on smaller companies, ETF.    
        ?May not work on smaller companies or ETF.  
        """
        try:
            r = requests.get(
                url="https://trade-service.wealthsimple.com/public/securities/{}".format(ticker)
            )
            # or json.loads(r.content) 
            return r.json()                 
        except BaseException as e:
            print(e) 
        
    @staticmethod
    def public_find_securities_by_ticker_historical(ticker, time):
        """
        staticmethod: get a company historical data based on time and by the actual ticker.    
        1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.  
        2.Where TIME is ("1d", "1w", "1m", "3m", "1y"): DOES NOT INCLUDE ("all").   
        ?May not work on smaller companies or ETF.  
        """
        try: 
            r = requests.get(
                url="https://trade-service.wealthsimple.com/public/securities/{}/historical_quotes/{}".format(ticker, time)
            )
            # json.loads(r.content) 
            return r.json()                       
        except BaseException as e:
            print(e) 
    
    @staticmethod
    def public_top_traded(offset=0, limit=5):
        """
        staticmethod: get top traded companies on wealthsimple trade.  
        1.Where OFFSET is the displacement between the selected offset and the beginning.   
        2.Where LIMIT is the amount of response you want from the request.  
        """
        try: 
            r = requests.get(
                url="""https://trade-service.wealthsimple.com/public/securities/top_traded?offset={}&limit={}""".format(offset, limit)
            )
            return r.json()                             
        except BaseException as e:
            print(e) 
    
    @staticmethod
    def public_find_securities_news(ticker):
        """
        staticmethod: get public news based on ticker name.    
        1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.   
        ?May not work on smaller companies or ETF. 
        """
        try: 
            r = requests.get(
                url="https://trade-service.wealthsimple.com/public/securities/{}/news".format(ticker)
            )
            return r.json()                            
        except BaseException as e:
            print(e)
    
    #! wealthsimple operational status api still public.
    @staticmethod    
    def summary_status():
        """
        staticmethod: get current summary status/incidents of wealthsimple trade.   
        the summary contains data for the following systems [    
        Login and Account Access, Quotes iOS app Order execution,  
        Security Search, Order submission, Apps, Android App   
        Order status, Trading, Market Data, Order Cancellation,   
        Linking bank accounts, Deposits and Withdrawals,   
        Account Values, Account Opening  
        ] 
        the data is in JSON format in body/content, JSON is large.  
        """
        try: 
            r = requests.get(
                url="https://status.wealthsimple.com/api/v2/summary.json"
            )
            return json.loads(r.content)                        
        except BaseException as e:
            print(e)
    
    @staticmethod    
    def current_status():
        """
        staticmethod: get current status/incidents of wealthsimple trade.    
        ?the data is in json format in body/content, json could be large. 
        """
        try: 
            r = requests.get(
                url="https://status.wealthsimple.com/api/v2/status.json"
            )
            return json.loads(r.content)                                   
        except BaseException as e:
            print(e)
    
    @staticmethod    
    def previous_status():
        """
        staticmethod: get all previous history status/incidents of wealthsimple trade.   
        ?the data is in json format in body/content, json is large.  
        """
        try: 
            r = requests.get(
                url="https://status.wealthsimple.com/api/v2/incidents.json"
            )
            return json.loads(r.content)                                   
        except BaseException as e:
            print(e)
    
    @staticmethod
    def auth(email, password):
        """
        staticmethod: checks if the given email and password are correct. 
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