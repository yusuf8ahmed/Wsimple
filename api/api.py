"""
Name: Chromazmoves  
Project Name: Wsimple   
File Name: Wsimple/api/api.py   
**File: Main access point to Wsimple API** 
"""

#!/usr/bin/env python3
# standard library
import sys
import json
import pprint
import datetime
from sys import platform
from loguru import logger
from typing import Union, Optional
# custom error
from .errors import LoginError, MethodInputError
from .errors import InvalidAccessTokenError, InvalidRefreshTokenError
from .errors import WSOTPUser, WSOTPError, WSOTPLoginError, TSXStopLimitPriceError
# third party
import requests

class Requestor:
    """Requestor class for Wsimple api as requests code is very repetitive 
    always stay.  
    """
    def get(url, funcname, **kwargs):
        """make a get request to a ***url***"""
        logger.debug("{}".format(funcname))
        r = requests.get(
            "".format(url), 
            kwargs
        )
        logger.debug("{} {}".format(funcname, r.status_code))
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r
    
    def post(url, funcname, **kwargs):
        """make a post request to a ***url***"""
        logger.debug("{}".format(funcname))
        r = requests.post(
            "".format(url), 
            kwargs
        )
        logger.debug("{} {}".format(funcname, r.status_code))
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r
    
    def delete(url, funcname, **kwargs):
        """make a delete request to a ***url***"""
        logger.debug("{}".format(funcname))
        r = requests.delete(
            "".format(url), 
            kwargs
        )
        logger.debug("{} {}".format(funcname, r.status_code))
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def put(url, funcname, **kwargs):
        """make a put request to a ***url***"""
        logger.debug("{}".format(funcname))
        r = requests.put(
            "".format(url), 
            kwargs
        )
        logger.debug("{} {}".format(funcname, r.status_code))
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
          
        
class Wsimple:
    """Wsimple is the main access class to the wealthsimple trade api."""
    base_url = "https://trade-service.wealthsimple.com/"
    time_ranges = [
        '1d',
        '1w',
        '1m',
        '3m',
        '1y',
        'all'
    ]
    email_notification = [ 
        'deposits',
        'withdrawals',
        'orders',
        'dividends',
        'referrals',
        'institutional_transfers',
        'news_and_announcements',
        'promos_and_tips'
    ]
    push_notification = [
        'deposits',
        'withdrawals',
        'orders',
        'dividends',
        'referrals',
        'institutional_transfers',
    ]  
    activities_types = [
        'all',
        'deposit',
        'withdrawal',        
        'buy',
        'sell',
        'dividend',
        'institutional_transfer',
        'internal_transfer',
        'refund',
        'referral_bonus',
        'affiliate',
    ]
    bank_logos = {
        "TD Canada Trust": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/td.png",
        "Royal Bank of Canada": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/rbc.png",
        "Tangerine Bank": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/tangerine.png",
        "CIBC": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/cibc.png",
        "Bank of Montreal": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/bmo.png",
        "Scotiabank": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/scotiabank.png",
        "Sun Life": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/sunlife.png",
        "Manulife": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/manulife.png",
        "Simplii Financial": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/simplii.png",
        "Great West Life": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/gwl.png",
        "Investors Group": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/investors-group.png",
        "Fidelity": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/fidelity.png",
        "National Bank of Canada": "https://s3.amazonaws.com/bank-verification-ui/institution-logos/nbcn.png"
    }
    exchanges = {
        "TSX",
        "CSE",
        "NYSE",
        "BATS",
        "FINRA",
        "OTCBB",
        "TSX-V",
        "NASDAQ",
        "OTC MARKETS",
        "AEQUITAS NEO EXCHANGE"
    }
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
    friendly_account_name = {
        'ca_tfsa':'TFSA',
        'ca_non_registered': 'Personal account',
        'ca_rrsp':'RRSP account',
        'ca_non_registered_crypto':'Crypto account'
    }
    name_security_group = { 
        'most_watched': {
            "title": 'Top 100 on Trade',
            "description": 'The most popular stocks on Wealthsimple Trade'
        },
        'most_active': {
            "title": 'Most active',
            "description": 'Most actively traded stocks and ETFs today'
        },
        'gainers': {
            "title": 'Top gainers',
            "description": 'Stocks and ETFs with the largest gains in stock price today'
        },
        'losers': {
            "title": 'Top losers',
            "description": 'Stocks and ETFs with the largest losses in stock price today'
        }
    }
    iscanadiansecurity = lambda x: x in ["TSX","TSX-V"]
    
    def __init__(self, 
                 email,
                 password, 
                 verbose_mode=False, 
                 access_mode=False, 
                 otp_mode=False,
                 otp_number=0, 
                 tokens=""):
        """
        Wsimple._\_\_init_\_\_() initializes the Wsimple class and logs the user in using 
        the provided email and password. Alternatively, ***access_mode*** can be set 
        to True then and users can access the functions prefixed with public without using 
        a Wealthsimple Trade account.
        """
        otp_status = None
        self.access_mode = access_mode
        self.verbose = verbose_mode
        if self.access_mode:
            pass
        else:
            #"create_account": not 1
            self.email = email
            payload = {"email":email, "password":password, "timeoutMs": 2e4}
            if otp_mode: 
                payload["otp"] = otp_number
            r = requests.post(
                url="{}auth/login".format(self.base_url),
                data=payload
            ) 
            del payload
            logger.debug(f"Login status code {r.status_code}")
            if "x-wealthsimple-otp" in r.headers: 
                #! one time password code login
                logger.info("One time password needed")
                try:
                    otp_headers = r.headers['x-wealthsimple-otp'].replace(" ", "").split(";")
                    method = otp_headers[1][7:] 
                    self._otp_info = {  
                                    "required": (otp_headers[0]),
                                    "method": otp_headers[1][7:]
                                }
                    if method == "sms":
                            self._otp_info["digits"] = otp_headers[2][7:]
                except:
                    raise WSOTPError
                finally:
                    raise WSOTPUser
            else:
                #! natural code login         
                if r.status_code == 200:
                    self._access_token = r.headers['X-Access-Token']
                    self._refresh_token = r.headers['X-Refresh-Token']
                    self.tokens = [
                        {'Authorization': self._access_token},
                        {"refresh_token": self._refresh_token}
                        ]
                    del r
                else:
                    if otp_mode: raise WSOTPLoginError
                    raise LoginError
      
    def refresh_token(self, tokens):
        """
        Generates and applies a new set of access and refresh tokens.  
        """
        r = requests.post(
            url="{}auth/refresh".format(self.base_url),
            data=tokens[1],
        )
        if r.status_code == 401:
            self.logger.error("dead refresh token")
            raise InvalidRefreshTokenError
        else:
            self.logger.debug(f"refresh token {r.status_code} code")
            self._access_token = r.headers['X-Access-Token']
            self._refresh_token = r.headers['X-Refresh-Token']
            self.tokens = [{'Authorization': self._access_token}, {"refresh_token": self._refresh_token}]
            return self.tokens
                         
    @classmethod
    def access(cls, verbose=False):
        """
        access functions prefixed with public
        """
        wsimple = cls("", "", verbose_mode=verbose, access_mode=True)
        return wsimple

    @classmethod
    def otp_login(cls, email, password, otp_number):
        """
        One time password(otp) login function:
        """
        wsimple = cls(email, password, otp_mode=True, otp_number=int(otp_number))
        return wsimple
        
    #! account related functions
    def get_account_ids(self, tokens):
        """
        Grabs all account ids under your your Wealthsimple Trade account. 
        """
        try:
            logger.debug("get_account_ids call")
            accounts = self.get_account(tokens)["results"]
            account_ids = []
            for account in accounts:
                account_ids.append(account["id"])
            logger.debug(f"get_account_ids XXX")
            return account_ids  
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def get_account(self, tokens):
        """
        Grabs all account information under your Wealthsimple Trade account. 
        """
        logger.debug("get_account call")
        r = requests.get(
            url="{}account/list".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_account {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_historical_portfolio_data(self, tokens, account_id: str = None, time: str = "1d"):
        """
        Grabs historical portfolio information for your Wealthsimple Trade account for a specified timeframe.  
        Where ***time*** is one of [1d, 1w, 1m, 3m, 1y, all]: autoset to 1d.  
        """
        logger.debug("get_historical_portfolio_data call")
        if account_id == None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        r = requests.get(
            url="{}account/history/{}".format(self.base_url, time),
            params={"account_id":account_id},
            headers=tokens[0]
        )
        logger.debug(f"get_historical_portfolio_data {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_me(self, tokens):
        """
        Grabs basic information about your Wealthsimple Trade account.
        """
        logger.debug("get_me call")
        r = requests.get(
            url="{}me".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_me {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_person(self, tokens):
        """
        Grabs Advanced/information about your Wealthsimple Trade account. 
        """
        logger.debug("get_person")
        r = requests.get(
            url="{}person".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_person {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError()
        else:
            return r.json()

    def get_bank_accounts(self, tokens):
        """
        Grabs all bank accounts under your Wealthsimple Trade account. 
        """
        logger.debug("get_bank_accounts")
        r = requests.get(
            url="{}bank-accounts".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_bank_accounts {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError()
        else:
            return r.json()

    def get_positions(self, tokens):
        """
        Grabs your current Wealthsimple Trade positions.    
        """
        logger.debug("get_positions")
        r = requests.get(
            url="{}account/positions".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_positions {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError()
        else:
            return r.json()

    #! order functions
    def get_orders(self, tokens):
        """
        Grabs all current and past orders.
        """
        logger.debug("get_orders")
        r = requests.get(
            url="{}orders".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_orders {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def _place_order(self,
                     tokens: str,
                     security_id: str,
                     account_id: str,
                     order_type: str,
                     sub_type: str,
                     stop_price = None,
                     quantity: int = 1,
                     limit_price: float = 1,
                     time_in_force: str = "day"):
        """
        Private function: places an order for a security.
        Where ***security_id*** is security id of the security that want to put an order on.
        Where ***account_id*** is you wealthsimple account id
        Where ***order_type*** is the major order type you want to make: ['sell_quantity' , 'buy_quantity']
        Where ***sub_type*** is the minor order type you want to attach to the major order type: ['market', 'limit', 'stop_limit']
        Where ***stop_price*** is the stop price used for "stop_limit" sub_type orders.
        Where ***quantity*** is the amount that you want to put in the order.
        Where ***limit_price*** is the limit price that you want to use in 'limit' and 'stop_limit' sub_type orders.
        Where ***time_in_force*** is when you
        
        """
        assert (order_type == 'sell_quantity' or order_type == 'buy_quantity')
        assert (sub_type == 'market' or sub_type == 'limit' or sub_type == 'stop_limit')
        # default time_in_force to 'day'
        if (order_type == "sell_quantity" and sub_type == "market"):
            # no limit_price: market sell
            order_dict = {
                "account_id": account_id,
                "quantity": quantity,
                "security_id": security_id,
                "order_type": order_type,
                "order_sub_type": sub_type,
                "time_in_force": time_in_force,
            }  
        elif(sub_type == "stop_limit"):
            # add stop_price: stop limit buy and sell
            order_dict = {
                "account_id": account_id,
                "quantity": quantity,
                "security_id": security_id,
                "order_type": order_type,
                "order_sub_type": sub_type,
                "time_in_force": time_in_force,
                "limit_price": limit_price,
                "stop_price": stop_price,
            }     
        else:
            # for market buy, limit buy and sell
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
            raise InvalidAccessTokenError
        else:
            return r.json()

    def create_order(self, tokens, payload):
        r = requests.post("{}orders".format(self.base_url),
                    headers=tokens[0],
                    json=payload)
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            print(r.status_code)
            print(r.content)
            print(json.loads(r.content))
            return r.json()
        
    def market_buy_order(self,
                         tokens,
                         security_id,
                         quantity,
                         limit_price=None,
                         account_id: Optional[str] = None,
                         ):
        """
        Places a market buy order for a security.  
        """
        try:
            logger.debug("buy_market_order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"]
            limit_price = self.find_securities_by_id(tokens, security_id)["quote"]["amount"]
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type='buy_quantity',
                                    sub_type='market',
                                    limit_price=limit_price,
                                    quantity=quantity
                                    )
            return res
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def limit_buy_order(self,
                        tokens,
                        security_id,
                        limit_price,
                        quantity,
                        account_id: Optional[str] = None,
                        gtc="day"):
        """
        Places a limit buy order for a security.    
        """
        try:
            logger.debug("buy_limit_order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"]
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type='buy_quantity',
                                    sub_type='limit',
                                    limit_price=limit_price,
                                    quantity=quantity,
                                    gtc=gtc)
            return res
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def stop_limit_buy_order(self,
                             tokens,
                             stop_price,
                             limit_price,
                             security_id,
                             quantity,
                             account_id: Optional[str] = None,
                             gtc="day"):
        """
        Places a stop limit buy order for a security.  
        """
        try:
            security = self.find_securities_by_id(security_id)
            exchange = security["stock"]["primary_exchange"]    
            if (self.iscanadiansecurity(exchange) and (stop_price != limit_price)):
                raise TSXStopLimitPriceError    
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type='buy_quantity',
                                    sub_type='stop_limit',
                                    limit_price=limit_price,
                                    quantity=quantity,
                                    gtc=gtc)
            return res       
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def market_sell_order(self,
                          tokens,
                          security_id: str,
                          account_id: Optional[str] = None,
                          quantity: int = 1):
        """
        Places a market sell order for a security.
        """
        try:
            logger.debug("sell_market_order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"]
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type='sell_quantity',
                                    sub_type='market',
                                    quantity=quantity)
            return res
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def limit_sell_order(self,
                         tokens,
                         limit_price,
                         security_id,
                         account_id: Optional[str] = None,
                         quantity=1,
                         gtc="day"):
        """
        Places a limit sell order for a security.  
        """
        try:
            logger.debug("sell_limit_order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"]
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type='sell_quantity',
                                    sub_type='limit',
                                    limit_price=limit_price,
                                    quantity=quantity,
                                    gtc=gtc)
            return res
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def stop_limit_sell_order(self,
                              tokens,
                              stop_price,
                              limit_price,
                              security_id,
                              account_id: Optional[str] = None,
                              quantity=1,
                              gtc="day"):
        """
        Places a limit sell order for a security.  
        """
        try:
            security = self.find_securities_by_id(security_id)
            exchange = security["stock"]["primary_exchange"]    
            if (self.iscanadiansecurity(exchange) and (stop_price != limit_price)):
                raise TSXStopLimitPriceError   
            res = self._place_order(tokens,
                                    account_id,
                                    security_id,
                                    order_type='sell_quantity',
                                    sub_type='stop_limit',
                                    limit_price=limit_price,
                                    quantity=quantity,
                                    gtc=gtc)
            return res       
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
    
    def cancel_order(self, tokens, order_id: str):
        """
        Cancels a order by its id.    
        Where ***order*** is order_id.   
        """
        logger.debug("cancel_order")
        r = requests.delete(
            "{}orders/{}".format(self.base_url, order_id),
            headers=tokens[0]
        )
        logger.debug(f"cancel_order {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def pending_orders(self, tokens, account_id=None):
        """
        Grabs all pending orders under your Wealthsimple Trade account.
        """
        if account_id is None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        orders = self.get_orders(tokens)['results']
        result = []
        for order in orders:
            if order['status'] == 'submitted':
                result.append(order)
        return result
    
    def cancelled_orders(self, tokens, account_id=None):
        """
        Grabs all cancelled orders under your Wealthsimple Trade account.
        """
        try:
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"]
            orders = self.get_orders(tokens)['results']
            result = []
            for order in orders:
                if order['status'] == 'cancelled':
                    result.append(order)
            return result
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def filled_orders(self, tokens, account_id=None):
        """
        Grabs all filled orders under your Wealthsimple Trade account.
        """
        if account_id is None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        orders = self.get_orders(tokens)['results']
        result = []
        for order in orders:
            if order['status'] == 'posted':
                result.append(order)
        return result

    def cancel_pending_orders(self, tokens):
        try:
            pending = self.pending_orders(tokens)
            result = []
            for orders in pending:
                print(orders["order_id"])
                result.append(self.cancel_order(tokens, orders["order_id"]))
            return result
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
        
    #! find securitites functions
    def find_securities(self, tokens, ticker: str):
        """
        Grabs information about the security resembled by the ticker.    
        Where ***ticker*** is the ticker of the company, API will fuzzy    
        match this argument and therefore multiple results can appear. 
        """
        logger.debug("find_securities")
        r = requests.get(
            url="{}securities".format(self.base_url),
            params={"query": ticker},
            headers=tokens[0]
        )
        logger.debug(f"find_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def find_securities_by_id(self, tokens, sec_id: str) -> dict:
        """
        Grabs information about the security resembled by the security id.  
        Where ***ticker*** is the ticker of the company. 
        """
        logger.debug("find_securities_by_id")
        r = requests.get(
            url="{}securities/{}".format(self.base_url, sec_id),
            headers=tokens[0]
        )
        logger.debug(f"find_securities_by_id {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def find_securities_by_id_historical(self, 
                                         tokens,
                                         sec_id: str,
                                         time: str="1d",
                                         mic: str="XNAS"):
        """
        Grabs historical information about the security by the security id in a specified timeframe.  
        Where ***time*** is the timeframe one of [1d, 1w, 1m, 3m, 1y, all]: autoset "1d".  
        Where ***mic*** is the Market Identifier Code for the exchange: autoset "XNAS"  
        """
        logger.debug("find_securities_by_id_historical")
        r = requests.get(
            url="{}securities/{}/historical_quotes/{}".format(self.base_url, sec_id, time),
            params={"mic":mic},
            headers=tokens[0]
        )
        logger.debug(f"find_securities_by_id_historical {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! activities functions
    def get_activities(self, tokens, account_id: Optional[str] = None, limit:int = 20, type:str = "all"):
        """
        Grabs the 20 most recent activities on under your Wealthsimple Trade account.    
        Where ***type*** is the activities type you want can be ["deposit", "withdrawal", "dividend", "buy", "sell"] autoset to all.  
        Where ***limit*** is the limitation of the response has to be less than 100: autoset 20.         
        """
        if not 1 < limit < 100:
            raise MethodInputError
        if type == "all":
            logger.debug("get_activities")
            r = requests.get(
                url="{}account/activities".format(self.base_url),
                params={"account-id":account_id, "limit":limit},
                headers=tokens[0]
            )
        else:
            logger.debug("get_activities")
            r = requests.get(
                url="{}account/activities".format(self.base_url),
                params={"account-id":account_id, "type":type, "limit":limit},
                headers=tokens[0]
            )  
        logger.debug(f"get_activities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_activities_bookmark(self, tokens, bookmark=None):
        """
        Provides the last 20 activities on the Wealthsimple Trade based on the bookmark.   
        Where ***bookmark*** is the bookmark id.   
        """
        logger.debug("get_activities_bookmark")
        r = requests.get(
            url="{}account/activities".format(self.base_url),
            params={"bookmark": bookmark},
            headers=tokens[0]
        )
        logger.debug(f"get_activities_bookmark {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! withdrawal functions
    def make_withdrawal(self,
                        tokens, 
                        amount: int,
                        currency: str = "CAD",
                        bank_account_id: str = None,
                        account_id: str = None):
        """
        Make a withdrawal under your Wealthsimple Trade account.  
        Where ***amount*** is the amount to withdraw.  
        Where ***currency*** is the currency need to be withdrawn(): autoset to "CAD"  
        Where ***bank_account_id*** is id of bank account where the money is going to be withdrawn from (get_bank_accounts function)  
        Where ***account_id*** is id of the account that is withdrawing the money (get_account function).  
        """
        logger.debug("make_withdrawal")
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
        logger.debug(f"make_withdrawal {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_withdrawal(self, tokens, funds_transfer_id: str):
        """
        Get specific withdrawal under yout Wealthsimple Trade account.
        Where ***funds_transfer_id*** is the id of the withdrawal
        """
        logger.debug("get_withdrawal")
        r = requests.get(
            url="{}withdrawals/{}".format(self.base_url, funds_transfer_id),
            headers=tokens[0]
        )
        logger.debug(f"get_withdrawal {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def list_withdrawals(self, tokens):
        """
        Get all withdrawals under your Wealthsimple Trade account.
        """
        logger.debug("list_withdrawals")
        r = requests.get(
            url="{}withdrawals".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"list_withdrawals {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def delete_withdrawal(self, tokens, funds_transfer_id: str):
        """
        Delete a specific withdrawal your Wealthsimple Trade account.
        """
        logger.debug("delete_withdrawal")
        r = requests.delete(
            url="{}withdrawals/{}".format(self.base_url, funds_transfer_id),
            headers=tokens[0]
        )
        logger.debug(f"delete_withdrawal {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! deposits functions
    def make_deposit(self, 
                     tokens, 
                     amount: int,
                     currency: str = "CAD", 
                     bank_account_id: str = None, 
                     account_id: str = None):
        """
        Make a deposit under your Wealthsimple Trade account. 
        Where ***amount*** is the amount to deposit  
        Where ***currency*** is the currency need to be transferred: autoset to "CAD"  
        Where ***bank_account_id*** is id of bank account.  
        Where ***account_id*** is id of the account.  
        """
        logger.debug("make_deposits")
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
        logger.debug(f"make_deposits {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_deposit(self, tokens, funds_transfer_id: str):
        """
        Get specific deposit under this Wealthsimple Trade account.  
        Where ***funds_transfer_id*** is the id of the deposit  
        """
        logger.debug("get_deposits")
        r = requests.get(
            url="{}deposits/{}".format(self.base_url, funds_transfer_id),
            headers=tokens[0]
        )
        logger.debug(f"get_deposits {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def list_deposits(self, tokens):
        """
        Get all deposits under your Wealthsimple Trade account.
        """
        logger.debug("list_deposits")
        r = requests.get(
            url="{}deposits".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"list_deposits {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def delete_deposit(self, tokens, funds_transfer_id: str):
        """
        Delete a specific deposit under your Wealthsimple Trade account.
        """
        logger.debug("delete_deposits")
        r = requests.delete(
            url="{}deposits/{}".format(self.base_url, funds_transfer_id),
            headers=tokens[0]
        )
        logger.debug(f"delete_deposits {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! market related functions
    def get_all_markets(self, tokens):
        """
        Grabs all market data including opening and closing hours 
        """
        logger.debug("get_all_markets")
        r = requests.get(
            url='{}markets'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_all_markets {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_market_hours(self, tokens, exchange: str):
        """
        Get all market data about a specific exchange.  
        Where ***exchange*** is the exchange name.
        """
        try:
            logger.debug("get_market_hours")
            exchanges = list(self.exh_to_mic.keys())
            if exchange in exchanges:
                all_markets = self.get_all_markets(tokens)['results']
                for market in all_markets:
                    if market["exchange_name"] == exchange:
                        return market
            else:
                return {}
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    #! watchlist functions
    def get_watchlist(self, tokens):
        """
        Get all watchlisted securities under your Wealthsimple trade account. 
        """
        logger.debug("get_watchlist")
        r = requests.get(
            url="{}watchlist".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_watchlist {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def add_watchlist(self, tokens, sec_id):
        """
        Add security under this Wealthsimple Trade account.    
        Where ***sec_id*** is the security id for the security you want to add.            
        """
        logger.debug("add_watchlist")
        r = requests.put(
            url="{}watchlist/{}".format(self.base_url, sec_id),
            headers=tokens[0]
        )
        logger.debug(f"add_watchlist {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def delete_watchlist(self, tokens, sec_id):
        """
        Delete a watchlisted securities in your Wealthsimple Trade account.  
        Where ***sec_id*** is the security id for the security you want to delete. 
        """
        logger.debug("delete_watchlist")
        r = requests.delete(
            url="{}watchlist/{}".format(self.base_url, sec_id),
            headers=tokens[0]
        )
        logger.debug(f"delete_watchlist {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! exchange functions
    def get_exchange_rate(self, tokens):
        """
        Current Wealthsimple Trade forex USD/CAD exchange rates. 
        """
        logger.debug("get_exchange_rate")
        r = requests.get(
            url="{}forex".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_exchange_rate {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! fact-sheet functions
    def get_fact_sheets(self, tokens):
        """
        Get all fact-sheets that you have access to under your Wealthsimple account
        """
        logger.debug("get_fact_sheets")
        r = requests.get(
            url='{}fact-sheets'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_fact_sheets {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    #! securities groups functions
    def get_top_losers_securities(self, tokens, offset=0, limit=20):
        """
        Grab a list of top losers securities under Wealthsimple trade today
        """
        logger.debug("get_top_losers_securities")
        r = requests.get(
            url='{}securities/top_market_movers'.format(self.base_url),
            params={"type":"losers","limit":limit,"offset":offset},
            headers=tokens[0]
        )
        logger.debug(f"get_top_losers_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json() 

    def get_top_gainers_securities(self, tokens, offset=0, limit=20):
        """
        Grab a list of top gainers securities under Wealthsimple trade today
        """
        logger.debug("get_top_gainers_securities")
        r = requests.get(
            url='{}securities/top_market_movers'.format(self.base_url),
            params={"type":"gainers","limit":limit,"offset":offset},
            headers=tokens[0]
        )
        logger.debug(f"get_top_gainers_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()  
    
    def get_most_active_securities(self, tokens, limit=20):
        """
        Grab a list of most active securities under Wealthsimple trade today
        """
        logger.debug("get_most_active_securities")
        r = requests.get(
            url='{}securities/top_market_movers'.format(self.base_url),
            params={"type":"most_active","limit":limit},
            headers=tokens[0]
        )
        logger.debug(f"get_most_active_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()      
    
    def get_most_watched_securities(self, tokens, offset=0, limit=20):
        """
        Grabs all most watched securities under Wealthsimple trade today
        """
        logger.debug("get_most_watched_securities")
        r = requests.get(
            url='{}securities/most_watched'.format(self.base_url),
            params={"limit":limit,"offset":offset},
            headers=tokens[0]
        )
        logger.debug(f"get_most_watched_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()    
    
    def get_featured_security_groups(self, tokens):
        """
        Grabs all featured security groups under Wealthsimple trade today
        """
        logger.debug("get_featured_security_groups")
        r = requests.get(
            url='{}security-groups/featured'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_featured_security_groups {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def get_securities_in_groups(self, tokens, group_id, offset=0, limit=20, filter_type=None):
        """
        Grabs all securities groups under Wealthsimple trade
        """
        logger.debug("get_securities_in_groups")
        r = requests.get(
            url='{}security-groups/{}/securities'.format(self.base_url, group_id),
            params={"limit":limit,"offset":offset,"filter_type":filter_type},
            headers=tokens[0]
        )        
        logger.debug(f"get_securities_in_groups {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def get_all_securities_groups(self, tokens, offset=0, limit=25, order="desc"):
        """
        Grabs all security groups under Wealthsimple trade  
        Where ***offset*** is >= 0: autoset to 0  
        Where ***limit*** is the limitation of the response, (1 <= limit < 99): autoset to 25  
        Where ***sort_order*** is order of the results and can be ["asc", "desc"]: autoset to "desc"  
        """
        # if not (1 <= limit < 99):
        #     raise MethodInputError(f"limit argument(int): must between 1 and 100 not {limit} {type(limit)}")
        # elif not offset >= 0:
        #     raise MethodInputError(f"offset argument(int): must be greater than or equal to 0 not {offset} {type(offset)}")
        # elif order not in ["asc", "desc"]:
        #     raise MethodInputError(f"order argument(str): must be either 'asc' or 'desc' not {order} {type(order)}")
        logger.debug("get_all_securities_groups")
        r = requests.get(
            url="{}security-groups".format(self.base_url),
            params={"offset":offset, "limit":limit, "sort_order":order},
            headers=tokens[0]
        )
        logger.debug(f"get_all_securities_groups {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            print(r.status_code)
            return r.json()
        
    #! mobile dashboard functions
    def get_mobile_dashboard(self, tokens):
        """
        Get all info in the mobile dashboard
        """
        logger.debug("get_mobile_dashboard")
        r = requests.get(
            url='{}mobile-dashboard'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_mobile_dashboard {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
     
    #! notification controls
    def get_disabled_notifications(self, token):
        """
        Grab all disabled notifications
        """
        logger.debug("get_disabled_notifications")
        r = requests.get(
            url='{}mute-notifications'.format(self.base_url),
            headers=token[0]
        )
        logger.debug(f"get_disabled_notifications {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def _notification(self, token, type, platform, enable=True):
        logger.debug(f"get_disabled_notifications {type} {platform} {enable}")
        if platform not in ["push", "email"]:
            raise MethodInputError("""
            platform given in incorrect use either 'push' (for mobile notifications) or 'email' (for email notifications)
            """)
        if enable: 
            # enable notification here: delete req
            r = requests.delete(
                url='{}mute-notifications/{}/{}'.format(self.base_url, type, platform),
                headers=token[0]
            )
            logger.debug(f"get_disabled_notifications {r.status_code}") 
        else:
            # disable notification here: put req
            r = requests.put(
                url='{}mute-notifications/{}/{}'.format(self.base_url, type, platform),
                headers=token[0]
            )
            logger.debug(f"get_disabled_notifications {r.status_code}")            
 
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json() 
    
    def enable_mobile_notification(self, token, type):
        """
        enable a specific type of notification for mobile
        """
        try:
            if type not in self.push_notification:
                raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.push_notification for allow notification type on moblie)""")
            notif = self._notification(token, type, "push")
            return notif            
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
 
    def enable_email_notification(self, token, type):
        """
        enable a specific type of notification for email
        """
        try:
            if type not in self.email_notification:
                raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.email_notification for allow notification type on email)""")
            notif = self._notification(token, type, "email")
            return notif           
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
    
    def disable_moblie_notification(self, token, type):
        """
        disable a specific type of notification for moblie
        """
        try:
            if type not in self.push_notification:
                raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.push_notification for allow notification type on moblie)""")
            notif = self._notification(token, type, "push", enable=False)
            return notif        
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
 
    def disable_email_notification(self, token, type):
        """
        disable a specific type of notification for email
        """
        try:
            if type not in self.email_notification:
                raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.email_notification for allow notification type on email)""")
            notif = self._notification(token, type, "email", enable=False)
            return notif       
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    #! global alerts
    def get_global_alerts(self, tokens):
        """
        Grab all global alerts
        """
        logger.debug("get_global_alerts")
        r = requests.get(
            url='{}global-alerts'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_global_alerts {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
     
    #! internal transfers 
    def get_supported_internal_transfers(self, tokens):
        """
        Grabs a list of all support interal transfers
        """
        logger.debug("get_supported_internal_transfers")
        r = requests.get(
            url='{}supported-internal-transfers'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_supported_internal_transfers {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
     
    def create_internal_transfers(self, tokens, payload):
        """
        create a internal transfer request
        currently no wrapper code
        """
        logger.debug("create_internal_transfers")
        r = requests.post(
            url='{}internal_transfers'.format(self.base_url),
            headers=tokens[0],
            data=payload
        )
        logger.debug(f"create_internal_transfers {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()    
    
    #! tax-documents
    def get_tax_documents(self, tokens, account_id=None):
        """
        Grab tax documents of your Wealthsimple account
        """
        logger.debug("get_tax_documents")
        if account_id == None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        r = requests.get(
            url='{}tax-documents'.format(self.base_url),
            param={"account_id", account_id},
            headers=tokens[0]
        )
        logger.debug(f"get_tax_documents {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
     
    #! monthly-statements
    def get_monthly_statements(self, tokens):
        """
        Grabs all monthly statements under your Wealthsimple account
        """
        logger.debug("get_monthly_statements")
        r = requests.get(
            url='{}monthly-statements'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_monthly_statements {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def get_monthly_statements_url(self, tokens, pdf_statement_id):
        """
        Grabs a url to a pdf of your statement.  
        Where ***pdf_statement_id*** is the id of the month you want to get.  
        """
        logger.debug("get_monthly_statements")
        r = requests.get(
            url='{}monthly-statements/{}'.format(self.base_url, pdf_statement_id),
            headers=tokens[0]
        )
        logger.debug(f"get_monthly_statements {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_monthly_statements_cleaned(self, tokens):
        """
        Grabs all monthly statements under your Wealthsimple account.  
        Is diffrent from ***get_monthly_statements*** as it clean the response data.   
        """
        try:
            logger.debug("get_all_monthly_statements")
            monthly_statements_data = self.get_monthly_statements(tokens)["results"]
            return_res = []
            for data in monthly_statements_data:
                inner_dict = {}
                inner_dict["created_at"] = data["created_at"]
                inner_dict["updated_at"] = data["updated_at"]
                inner_dict["period"] = data["period"]
                inner_dict["id"] = data["id"]
                inner_dict["url"] = self.get_monthly_statements_url(tokens, data["id"])
                return_res.append(inner_dict)
            logger.debug(f"get_all_monthly_statements done!!")            
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    #! websocket_ticket
    def get_websocket_ticket(self, tokens):
        """
        Grabs a websocket ticket, need to connect to the wealthsimple websocket 
        """
        logger.debug("get_websocket_ticket")
        r = requests.post(
            url='{}websocket-ticket'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_websocket_ticket {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()  

    #! functions after this point are not core to the API
    def test_endpoint(self, tokens):
        """
        function for testing new endpoints
        """
        logger.debug("test endpoint")
        order_dict =  {
            "account_id": str(self.get_account(tokens)["results"][0]["id"]),
            "security_id": "sec-s-76a7155242e8477880cbb43269235cb6",
            "limit_price": int(),
            "quantity": 1,
            "order_type": "buy_quantity",
            "order_sub_type": "market",
            "time_in_force": "day"
        }
        r = requests.post("{}orders".format(self.base_url),
                    headers=tokens[0],
                    json=order_dict)
        print(f"{r.status_code} {r.url}")
        print(r.headers)
        print(r.content)
        # print(r.json())
        return r.json()

    def settings(self, tokens):
        """
        Get settings needed for /settings route.
        """
        logger.debug("starting settings")
        try:
            me = self.get_me(tokens)
            person = self.get_person(tokens)
            bank_account = self.get_bank_accounts(tokens)
            exchange_rate = self.get_exchange_rate(tokens)
            ws_current_operational_status = self.current_status()
            return {
                'me': me,
                'person': person,
                'bank_account': bank_account,
                'exchange_rate': exchange_rate,
                'ws_current_operational_status': ws_current_operational_status
            }
        except InvalidAccessTokenError:
            logger.debug("settings InvalidAccessTokenError")
            raise InvalidAccessTokenError

    def stock(self, tokens, sec_id, time="1d"):
        """
        Get dashboard needed for /stock/<sec_id> route.
        """
        logger.debug("starting stock {}".format(sec_id))
        try:
            sparkline = self.find_securities_by_id_historical(tokens, sec_id, time)
            security_info = self.find_securities_by_id(tokens, sec_id)
            news = self.public_find_securities_news(security_info["stock"]["symbol"])
            position = self.get_account(tokens)
            return {
                "sparkline": sparkline,
                "security_info": security_info,
                "position": position,
                "news": news 
            }
        except InvalidAccessTokenError:
            logger.error("stock InvalidAccessTokenError")
            raise InvalidAccessTokenError
        
    def search_page(self, tokens):
        """
        Get security groups need for /search route
        """
        try:
            featured_security_groups = self.get_featured_security_groups(tokens)
            get_top_losers_securities = self.get_top_losers_securities(tokens, limit=5)
            get_top_gainers_securities = self.get_top_gainers_securities(tokens, limit=5)
            get_most_active_securities = self.get_most_active_securities(tokens, limit=5)
            get_most_watched_securities = self.get_most_watched_securities(tokens, limit=5)
            return {
                "featured_security_groups": featured_security_groups,
                "most_watched": get_most_watched_securities,
                "most_active": get_most_active_securities,
                "top_gainers": get_top_gainers_securities,
                "top_losers": get_top_losers_securities,
            }
        except InvalidAccessTokenError:
            logger.error("search_page InvalidAccessTokenError")
            raise InvalidAccessTokenError

    def dashboard(self, tokens):
        """
        Get dashboard needed for /home route.  
        v1: 2+ seconds - 11 calls     
        v2: 1-2 seconds - 5 calls   
        v3: 1-2 seconds - 4 calls   
        v4: 0-1 seconds - 2 calls    
        """
        logger.debug("calling dashboard")
        try:
            mobile_dashboard = self.get_mobile_dashboard(tokens)
            account_data = self.get_historical_portfolio_data(tokens)
            
            account = mobile_dashboard["accounts"][0]
            watchlist = mobile_dashboard["watchlist"]
            positions = mobile_dashboard["positions"]
            previous_amount = account_data["previous_close_net_liquidation_value"]['amount']
            total_value = account_data["results"][-1]["value"]
            account_value_graph = account_data["results"]
            account_change = round(total_value['amount'] - previous_amount, 2)
            account_change_percentage = round((account_change / previous_amount)*100, 2)
            return {
                'available_to_trade': {
                    'amount': account['buying_power']['amount'],
                    'currency': account['buying_power']['currency']
                },
                'account_value': {
                    'amount': total_value['amount'],
                    'currency': total_value['currency']
                },
                'net_deposits': {
                    'amount': account['net_deposits']['amount'],
                    'currency': account['net_deposits']['currency']
                },
                'available_to_withdraw': {
                    'amount': account['available_to_withdraw']['amount'],
                    'currency': account['available_to_withdraw']['currency']
                },
                'account_change': {
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
            logger.error("dashboard InvalidAccessTokenError")
            raise InvalidAccessTokenError

    #! public prefix functions
    @staticmethod
    def public_find_securities_by_ticker(ticker):
        """
        Grabs information about the security resembled by the ticker.  
        Where ***ticker*** is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/{}".format(base_url_public, ticker)
        )
        return r.json()

    @staticmethod
    def public_find_securities_by_ticker_historical(ticker, time):
        """
        Get a company historical data based on a time.    
        Where ***ticker*** is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.  
        Where ***time*** is ("1d", "1w", "1m", "3m", "1y"): DOES NOT INCLUDE ("all").   
        !May not work on smaller companies or ETFs.  
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/{}/historical_quotes/{}".format(
                base_url_public, ticker, time)
        )
        return r.json()

    @staticmethod
    def public_top_traded(offset=0, limit=5):
        """
        Get top traded companies on Wealthsimple trade.  
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/top_traded".format(base_url_public),
            params={"offset": offset,"limit":limit}
        )
        return r.json()

    @staticmethod
    def public_find_securities_news(ticker):
        """
        Get public news based on the ticker.    
        Where ***ticker*** is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.   
        !May not work on smaller companies or ETF. 
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/{}/news".format(base_url_public, ticker)
        )
        return r.json()

    #! public prefix functions: wealthsimple operational status
    @staticmethod
    def summary_status():
        """
        Get current summary status/incidents of Wealthsimple trade.     
        This function returns data on these systems:  
        Login and Account Access, Deposits and Withdrawals,   
        Security Search, Order execution, Order submission,   
        Order Cancellation, Linking bank accounts,   
        Quotes, Order status, Trading, Market Data,  
        Account Values, Account Opening,   
        Apps, 
        iOS app, Android App  
        the data is in the body(content), data is large.  
        """
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/summary.json"
        )
        return json.loads(r.content)

    @staticmethod
    def current_status():
        """
        Get current status/incidents of wealthsimple trade.    
        the data is in body(content), data could be large. 
        """
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/status.json"
        )
        return json.loads(r.content)

    @staticmethod
    def historical_status():
        """
        Get all previous history status/incidents of wealthsimple trade.   
        the data is in body(content), data could be large. 
        """
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/incidents.json"
        )
        return json.loads(r.content)
