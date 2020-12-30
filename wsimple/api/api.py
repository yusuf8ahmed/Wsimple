"""
Name: Yusuf Ahmed  
Project Name: Wsimple   
File Name: api/api.py   
**File: Main access point to API** 
"""

#!/usr/bin/env python3
# standard library
import json
from loguru import logger
from typing import Optional, Union
# custom error
from .errors import LoginError
from .errors import InvalidAccessTokenError, InvalidRefreshTokenError
from .errors import WSOTPUser, WSOTPError, WSOTPLoginError, TSXStopLimitPriceError
# third party
import requests
             
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
    iscanadiansecurity = lambda _, x: x in ["TSX","TSX-V"]
    
    def __init__(self, 
                 email, 
                 password, 
                 otp_number: int = 0,
                 otp_mode: bool = False,
                 public_mode: bool = False,     
                 oauth_mode: bool = False,              
                 verbose_mode: bool = False, 
                 tokens: Optional[list] = None):
        """
        Wsimple._\_\_init_\_\_() initializes the Wsimple class and logs the user in using 
        the provided email and password. Alternatively, ***access_mode*** can be set 
        to True then and users can access the functions prefixed with public without using 
        a Wealthsimple Trade account.
        """
        #"create_account": not 1
        self.public_mode = public_mode
        self.verbose = verbose_mode
        self.oauth_mode = oauth_mode
        self.email = email
        if self.public_mode:
            pass
        elif self.oauth_mode:
            self.tokens = tokens
        else:
            payload = {"email":email, "password":password, "timeoutMs": 2e4}
            if otp_mode: payload["otp"] = otp_number
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
    def otp_login(cls,
                  email,
                  password,
                  otp_number,
                  verbose=False):
        """
        constructor: login with a otp code:
        """
        wsimple = cls(email, password, otp_mode=True, otp_number=int(otp_number))
        return wsimple 
   
    @classmethod
    def oauth_login(cls, token_dict, verbose=False):
        """
        constructor: login with a predefined list of tokens:
        """
        wsimple = cls("", "", oauth_mode=True, tokens=token_dict, verbose_mode=verbose)
        return wsimple
                         
    @classmethod
    def public(cls, verbose=False):
        """
        constructor: Use Wsimple.public functions without an wealthsimple account:
        """
        wsimple = cls("", "", public_mode=True, verbose_mode=verbose)
        return wsimple
 
    #! account related functions
    def get_account(self, tokens, id: str):
        """
        Grab a specific accounts information by id 
        """
        logger.debug("get_account call")
        r = requests.get(
            url="{}account/{}".format(self.base_url, id),
            headers=tokens[0]
        )
        logger.debug(f"get_account {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def get_accounts(self, tokens):
        """
        Grabs all accounts information
        """
        logger.debug("get_accounts call")
        r = requests.get(
            url="{}account/list".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_account {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json() 
           
    def get_trade_account_id(self, tokens):
        """ 
        If any function 'account_id' param is empty, it will use 
        this function to get the first trading id  """
        accounts = self.get_accounts(tokens)["results"]
        for account in accounts:
            if account["account_type"] == "ca_non_registered":
                return account["id"]

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
            logger.debug(f"get_account_ids ^^^")
            return account_ids  
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
        
    def get_historical_portfolio_data(self,
                                      tokens,
                                      time: str = "1d",
                                      account_id: Optional[str] = None
                                      ):
        """
        Grabs historical portfolio information for your Wealthsimple Trade account for a specified timeframe.  
        Where ***time*** is one of [1d, 1w, 1m, 3m, 1y, all]: autoset to 1d.  
        """
        logger.debug("get_historical_portfolio_data call")
        if account_id == None:
            account_id = self.get_trade_account_id(tokens)
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
            raise InvalidAccessTokenError
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
            raise InvalidAccessTokenError
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
            raise InvalidAccessTokenError
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

    def _send_order(self, tokens, payload: dict):
        """ send order to wealthsimple servers """
        logger.debug("create_order")
        r = requests.post("{}orders".format(self.base_url),
                    headers=tokens[0],
                    json=payload)
        logger.debug(f"create_order {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
        
    def market_buy_order(self,
                         tokens,
                         security_id: str,
                         quantity: int = 1,
                         account_id: Optional[str] = None,
                         ):
        """
        Places a market buy order for a security.  
        """
        try:
            logger.debug("buy_market_order")
            if account_id is None:
                account_id = self.get_trade_account_id(tokens)
            return self._send_order(tokens, {
                "security_id": security_id,
                "limit_price": 1,
                "quantity": quantity,
                "order_type": "buy_quantity",
                "order_sub_type": "market",
                "time_in_force": "day",
                "account_id": account_id
            })
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def limit_buy_order(self,
                        tokens,
                        security_id: str,
                        limit_price,
                        quantity: int = 1,
                        time_in_force: str = "day",
                        account_id: Optional[str] = None
                        ):
        """
        Places a limit buy order for a security.    
        """
        try:
            logger.debug("buy_limit_order")
            if account_id is None:
                account_id = self.get_trade_account_id(tokens)
            return self._send_order(tokens, {
                "security_id": security_id,
                "account_id": account_id,
                "limit_price": limit_price,
                "quantity": quantity,
                "order_type": "buy_quantity",
                "order_sub_type": "limit",
                "time_in_force": time_in_force,
            })
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def stop_limit_buy_order(self,
                             tokens,
                             security_id: str,
                             stop_price,
                             limit_price,
                             quantity: int = 1,
                             time_in_force: str = "day",
                             account_id: Optional[str] = None
                            ):
        """
        Places a stop limit buy order for a security. 
        """
        try:
            if account_id is None:
                account_id = self.get_trade_account_id(tokens)
            security = self.find_securities_by_id(tokens, security_id)
            exchange = security["stock"]["primary_exchange"]    
            if (self.iscanadiansecurity(exchange) and (stop_price != limit_price)):
                raise TSXStopLimitPriceError    
            return self._send_order(tokens, {
                "security_id": security_id,
                "account_id": account_id,
                "stop_price": stop_price,
                "limit_price": limit_price,
                "quantity": quantity,
                "order_type": "buy_quantity",
                "order_sub_type": "stop_limit",
                "time_in_force": time_in_force,
            })
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def market_sell_order(self,
                          tokens,
                          security_id: str,
                          quantity: int = 1,
                          account_id: Optional[str] = None
                          ):
        """
        Places a market sell order for a security.
        """
        try:
            logger.debug("sell_market_order")
            if account_id is None:
                account_id = self.get_trade_account_id(tokens)
            return self._send_order(tokens, {
                "security_id": security_id,
                "market_value": 1,
                "quantity": quantity,
                "order_type": "sell_quantity",
                "order_sub_type": "market",
                "time_in_force": "day",
                "account_id": account_id,
            })
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def limit_sell_order(self,
                         tokens,
                         security_id: str,
                         limit_price,
                         quantity: int = 1,
                         time_in_force: str = "day",
                         account_id: Optional[str] = None
                         ):
        """
        Places a limit sell order for a security.  
        """
        try:
            logger.debug("sell_limit_order")
            if account_id is None:
                account_id = self.get_trade_account_id(tokens)
            return self._send_order(tokens, {
                "security_id": security_id,
                "limit_price": limit_price,
                "quantity": quantity,
                "order_type": "sell_quantity",
                "order_sub_type": "limit",
                "time_in_force": time_in_force,
                "account_id": account_id
            })
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def stop_limit_sell_order(self,
                              tokens,
                              security_id: str,
                              stop_price,
                              limit_price,
                              quantity: int = 1,
                              time_in_force: str = "day",
                              account_id: Optional[str] = None,
                              ):
        """
        Places a limit sell order for a security.
        """
        try:
            if account_id is None:
                account_id = self.get_trade_account_id(tokens)
            security = self.find_securities_by_id(tokens, security_id)
            exchange = security["stock"]["primary_exchange"]    
            if (self.iscanadiansecurity(exchange) and (stop_price != limit_price)):
                raise TSXStopLimitPriceError   
            return self._send_order(tokens, {
                "security_id": security_id,
                "stop_price": stop_price,
                "limit_price": limit_price,
                "quantity": quantity,
                "order_type": "sell_quantity",
                "order_sub_type": "stop_limit",
                "time_in_force": time_in_force,
                "account_id": account_id
            })        
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

    def pending_orders(self, tokens):
        """
        Grabs all pending orders under your Wealthsimple Trade account.
        """
        try:
            orders = self.get_orders(tokens)['results']
            result = []
            for order in orders:
                if order['status'] == 'submitted':
                    result.append(order)
            return result
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError
    
    def cancelled_orders(self, tokens):
        """
        Grabs all cancelled orders under your Wealthsimple Trade account.
        """
        try:
            orders = self.get_orders(tokens)['results']
            result = []
            for order in orders:
                if order['status'] == 'cancelled':
                    result.append(order)
            return result
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def filled_orders(self, tokens):
        """
        Grabs all filled orders under your Wealthsimple Trade account.
        """
        try:
            orders = self.get_orders(tokens)['results']
            result = []
            for order in orders:
                if order['status'] == 'posted':
                    result.append(order)
            return result
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    def cancel_pending_orders(self, tokens):
        """ cancel all pending order """
        try:
            pending = self.pending_orders(tokens)
            result = []
            for orders in pending:
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

    def find_securities_by_id(self, tokens, sec_id: str):
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
                                         time: str = "1d",
                                         mic: str = "XNAS"):
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
    def get_activities(self, 
                       tokens, 
                       limit: int = 20,
                       type: Union[str, list] = "all",
                       sec_id: Optional[str] = None,
                       account_id: Optional[str] = None,
                       ):
        """
        Grabs the 20 most recent activities on under your Wealthsimple Trade account.    
        Where ***type*** is the activities type you want can be 
        [ 'buy','sell','deposit','withdrawal',
          'dividend','institutional_transfer', 'internal_transfer',
          'refund','referral_bonus', 'affiliate'
        ] autoset to "all".  
        Where ***limit*** is the limitation of the response has to be less than 100: autoset 20.         
        """
        if account_id is None:
            account_id = self.get_trade_account_id(tokens)
        params = {"account_ids":account_id, "limit":limit}      
        if not type == "all":
            params["type"] = type
        if not sec_id is None:
            params["security_id"] = sec_id
        logger.debug("get_activities")
        r = requests.get(
            url="{}account/activities".format(self.base_url),
            params=params,
            headers=tokens[0]
        ) 
        logger.debug(f"get_activities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_activities_bookmark(self, tokens, bookmark: str):
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
                        amount: Union[int, float],
                        bank_account_id: Optional[str] = None,
                        account_id: Optional[str] = None):
        """
        Make a withdrawal under your Wealthsimple Trade account.  
        Where ***amount*** is the amount to withdraw.  
        Where ***bank_account_id*** is id of bank account where the money is going to be withdrawn from (get_bank_accounts function)  
        Where ***account_id*** is id of the account that is withdrawing the money.  
        """
        logger.debug("make_withdrawal")
        if bank_account_id == None:
            bank_account_id = self.get_bank_accounts(tokens)["results"][0]["id"]
        if account_id == None:
            account_id = self.get_trade_account_id(tokens)
        person = self.get_me(tokens)
        payload = {
            "bank_account_id": str(bank_account_id),
            "account_id": str(account_id),
            "client_id": str(person["id"]),
            "amount": float(amount),
            "currency": "CAD"
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
                     amount: Union[int, float],
                     bank_account_id: Optional[str] = None, 
                     account_id: Optional[str] = None):
        """
        Make a deposit under your Wealthsimple Trade account. 
        Where ***amount*** is the amount to deposit    
        Where ***bank_account_id*** is id of bank account.  
        Where ***account_id*** is id of the account.  
        """
        logger.debug("make_deposits")
        if bank_account_id == None:
            bank_account_id = self.get_bank_accounts(tokens)["results"][0]["id"]
        if account_id == None:
            account_id = self.get_trade_account_id(tokens)
        person = self.get_me(tokens)
        payload = {
            "client_id": str(person["id"]),
            "bank_account_id": str(bank_account_id),
            "account_id": str(account_id),
            "amount": float(amount),
            "currency": "CAD"
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

    def add_watchlist(self, tokens, sec_id: str):
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

    def delete_watchlist(self, tokens, sec_id: str):
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
    def get_top_losers_securities(self,
                                  tokens,
                                  offset: int = 0,
                                  limit: int = 20):
        """
        Grab a list of top losers securities under Wealthsimple trade today.
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
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

    def get_top_gainers_securities(self,
                                   tokens,
                                   offset: int = 0,
                                   limit: int = 20):
        """
        Grab a list of top gainers securities under Wealthsimple trade today.
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
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
    
    def get_most_active_securities(self,
                                   tokens,
                                   limit: int = 20):
        """
        Grab a list of most active securities under Wealthsimple trade today.  
        Where ***limit*** is the amount of response you want from the request.  
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
    
    def get_most_watched_securities(self,
                                    tokens,
                                    offset: int = 0,
                                    limit: int = 20):
        """
        Grabs all most watched securities under Wealthsimple trade today.
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
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
    
    def get_securities_in_groups(self, 
                                 tokens,
                                 group_id: str,
                                 offset: int = 0,
                                 limit: int = 20,
                                 filter_type: str = None):
        """
        Grabs all securities groups under Wealthsimple trade. 
        Where ***filter_type*** - "most_watched" ? 
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
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
    
    def get_all_securities_groups(self, 
                                  tokens,
                                  offset: int = 0,
                                  limit: int = 25,
                                  order: str = "desc"):
        """
        Grabs all security groups under Wealthsimple trade  
        Where ***offset*** is >= 0: autoset to 0  
        Where ***limit*** is the limitation of the response, (1 <= limit < 99): autoset to 25  
        Where ***sort_order*** is order of the results and can be ["asc", "desc"]: autoset to "desc"  
        """
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
     
    #! global alerts
    def get_alerts(self, tokens):
        """
        Grab all global alerts
        """
        logger.debug("get_alerts")
        result = {}
        r_user = requests.get(
            url='{}global-alerts/user'.format(self.base_url),
            headers=tokens[0]
        )
        r_all = requests.get(
            url='{}global-alerts'.format(self.base_url),
            headers=tokens[0]
        ) 
        result["user"] = r_user.json()["results"]
        result["all"] = r_all.json()["results"]
        logger.debug(f"get_alerts user:{r_user.status_code} all:{r_all.status_code}")
        if (r_user.status_code == 401 or r_all.status_code == 401) :
            raise InvalidAccessTokenError
        else:
            return result
     
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
        currently no wrapper functions.
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
    def get_tax_documents(self, 
                          tokens, 
                          account_id: Optional[str] = None):
        """
        Grab tax documents of your Wealthsimple account
        """
        logger.debug("get_tax_documents")
        if account_id is None:
            account_id = self.get_trade_account_id(tokens)
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
            result = []
            for data in monthly_statements_data:
                inner_dict = {}
                inner_dict["created_at"] = data["created_at"]
                inner_dict["updated_at"] = data["updated_at"]
                inner_dict["period"] = data["period"]
                inner_dict["id"] = data["id"]
                inner_dict["url"] = self.get_monthly_statements_url(tokens, data["id"])["url"]
                result.append(inner_dict)
            logger.debug(f"get_all_monthly_statements ^^^")    
            return result
                        
        except InvalidAccessTokenError:
            raise InvalidAccessTokenError

    #! websocket_ticket
    def get_websocket_ticket(self, tokens):
        """
        Grabs a websocket ticket, need to connect to the wealthsimple websocket 
        url for accessing websocket is:
        "wss://trade-service.wealthsimple.com/websocket?ticket={}&version=2".format(ticket) 
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
        account_id = self.get_trade_account_id(tokens)
        logger.debug("test endpoint")
        r = requests.get(
            url="{}crypto-waitlist".format(self.base_url),
            params={"user-id": "user-80b4076b-6a6a-4b3c-84a9-43d44f302da4"},
            headers=tokens[0]
            )  
        print(f"{r.status_code} {r.url}")
        print(r.headers)
        print(r.content)
        # print(r.json())
        return r.json()

    def settings(self, tokens):
        """
        Get settings data needed for settings page.
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

    def stock(self,
              tokens,
              sec_id: str,
              time: str = "1m"):
        """
        Get security data needed for stock search pages.
        """
        logger.debug("starting stock {}".format(sec_id))
        try:
            sparkline = self.find_securities_by_id_historical(tokens, sec_id, time)
            security_info = self.find_securities_by_id(tokens, sec_id)
            news = self.public_find_securities_news(security_info["stock"]["symbol"])
            position = self.get_positions(tokens)
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
        Get groups need for search page
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
        Get dashboard page needed for home page.    
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
        !May not work on smaller companies or ETFs. 
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
    def public_top_traded(offset: int = 0, limit: int = 5):
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
        Apps, iOS app, Android App  
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