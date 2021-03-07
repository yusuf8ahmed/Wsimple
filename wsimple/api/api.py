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
from .endpoints import Endpoints
from .requestor import requestor
# third party
from box import Box
import requests
             
class Wsimple:
    """Wsimple is the main access class to the wealthsimple trade api."""
    BASE_URL = Endpoints.BASE.value
    BASE_PUBLIC_URL = Endpoints.BASE_PUBLIC.value
    BASE_STATUS_URL = Endpoints.BASE_STATUS.value 
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
        'ca_tfsa':'tfsa',
        'ca_non_registered': 'personal',
        'ca_rrsp':'rrsp',
        'ca_non_registered_crypto':'crypto'
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
            if "x-wealthsimple-otp-required" in r.headers: 
                #! otp needed code
                logger.info("OTP code needed")
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
                    self.access_expires = int(r.headers['X-Access-Token-Expires'])
                    print(int(r.headers['X-Access-Token-Expires']))
                    self.tokens = [
                        {'Authorization': self._access_token},
                        {"refresh_token": self._refresh_token}
                        ]
                    self.data = r.json()
                    del r
                else:
                    if otp_mode:
                        raise WSOTPLoginError
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
    def get_accounts(self, tokens):
        """
        Grabs all accounts information
        """
        return requestor(
            Endpoints.GET_ACCOUNT_LIST,
            args={"base": self.BASE_URL},
            headers=tokens[0]
        )    
        
    def get_account(self, tokens, account_id: Optional[str]=None):
        """
        Grab a specific accounts information by id: 
        !Wealthsimple Servers will default to trade account if account_id = None
        """   
        params = {}    
        if account_id != None:
            params["account_ids"] = account_id   
        return requestor(
            Endpoints.GET_ACCOUNT,
            args={"base": self.BASE_URL},
            params=params,
            headers=tokens[0]
        )
    
    def accounts(self, tokens, block_deleted=True):
        """
        Wrapper: Grabs all account ids under your Wealthsimple account. 
        """
        try:
            logger.debug("accounts call")
            accounts = self.get_accounts(tokens)["results"]
            res = {}
            for account in accounts:
                k = self.friendly_account_name[account["account_type"]]
                if block_deleted: 
                    if account['deleted_at'] == None:
                        res[k] = account["id"]
                else:
                    res[k] = account["id"]
            logger.debug(f"accounts ^^^")
            return Box(res)
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
        !account_id is required. 
        """
        if account_id == None:
            account_id = self.accounts(tokens).personal
        return requestor(
            Endpoints.GET_ACCOUNT_HISTORY,
            args={"base": self.BASE_URL, "time": time},
            headers=tokens[0],
            params={"account_id": account_id},
        )

    def get_me(self, tokens):
        """
        Grabs basic information about your Wealthsimple Trade account.
        """
        return requestor(
                Endpoints.GET_ME,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def get_person(self, tokens):
        """
        Grabs Advanced/information about your Wealthsimple Trade account. 
        """
        return requestor(
                Endpoints.GET_PERSON,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def get_bank_accounts(self, tokens):
        """
        Grabs all bank accounts under your Wealthsimple Trade account. 
        """
        return requestor(
                Endpoints.GET_BANK_ACCOUNTS,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def get_positions(self, tokens,
                      sec_id: Optional[str] = None,
                      account_id: Optional[str] = None):
        """
        Grabs your current Wealthsimple Trade positions.    
        """      
        param = {
            "account_id": account_id,
            "security_id": sec_id
        }        
        return requestor(
                Endpoints.GET_POSITONS,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                params=param)

    #! order functions
    def get_orders(self, tokens):
        """
        Grabs all current and past orders.
        """    
        return requestor(
                Endpoints.GET_ORDERS,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def _send_order(self, tokens, payload: dict):
        """ send order to wealthsimple servers """
        return requestor(
                Endpoints.SEND_ORDER,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                json=payload)
        
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
        return requestor(
                Endpoints.CANCEL_ORDER,
                args = {"base": self.BASE_URL, "order_id": order_id},
                headers=tokens[0])

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
            return {"result": result}
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
        return requestor(
                Endpoints.FIND_SECURITIES,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                params={"query": ticker})

    def find_securities_by_id(self, tokens, sec_id: str):
        """
        Grabs information about the security resembled by the security id.  
        Where ***ticker*** is the ticker of the company. security_id
        """
        return requestor(
                Endpoints.FIND_SECURITIES_BY_ID,
                args = {"base": self.BASE_URL, "security_id": sec_id },
                headers=tokens[0])

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
        return requestor(
                Endpoints.FIND_SECURITIES_HISTORY,
                args = {"base": self.BASE_URL, "time": time, "security_id": sec_id },
                headers=tokens[0],
                params={"mic":mic})

    #! activities functions
    def get_activities(self, 
                       tokens, 
                       limit: int = 20,
                       type: Union[str, list] = "all",
                       sec_id: Optional[str] = None,
                       account_ids: Union[str, list] = None,
                       ):
        """
        Grabs the 20 most recent activities on under your Wealthsimple Trade account.    
        Where ***type*** is the activities type you want can be 
        [ 'buy','sell','deposit','withdrawal',
          'dividend','institutional_transfer', 'internal_transfer',
          'refund','referral_bonus', 'affiliate'
        ] autoset to "all".  
        Where ***limit*** is the limitation of the response has to be less than 100: autoset 20.
        !Wealthsimple Servers will default to trade account if account_id = None         
        """
        params = {"limit":limit}   
        if not account_ids is None:
            params["account_ids"] = account_ids
        if not type == "all":
            params["type"] = type
        if not sec_id is None:
            params["security_id"] = sec_id   
        return requestor(
                Endpoints.GET_ACTIVITES,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                params=params)

    def get_activities_bookmark(self, tokens, bookmark: str):
        """
        Provides the last 20 activities on the Wealthsimple Trade based on the bookmark.   
        Where ***bookmark*** is the bookmark id.   
        """
        params = {"bookmark": bookmark}
        return requestor(
                Endpoints.GET_ACTIVITES,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                params=params)

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
            account_id = self.accounts(tokens).personal
        person = self.get_me(tokens)
        payload = {
            "bank_account_id": str(bank_account_id),
            "account_id": str(account_id),
            "client_id": str(person["id"]),
            "amount": float(amount),
            "currency": "CAD"
        }
        return requestor(
                Endpoints.MAKE_WITHDRAWALS,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                data=payload)

    def get_withdrawal(self, tokens, funds_transfer_id: str):
        """
        Get specific withdrawal under yout Wealthsimple Trade account.
        Where ***funds_transfer_id*** is the id of the withdrawal
        """
        return requestor(
                Endpoints.GET_WITHDRAWAL_BY_ID,
                args={ "base": self.BASE_URL,"funds_transfer_id": funds_transfer_id},
                headers=tokens[0])

    def list_withdrawals(self, tokens):
        """
        Get all withdrawals under your Wealthsimple Trade account.
        """
        return requestor(
                Endpoints.LIST_WITHDRAWALS,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def delete_withdrawal(self, tokens, funds_transfer_id: str):
        """
        Delete a specific withdrawal your Wealthsimple Trade account.
        """
        return requestor(
                Endpoints.DELETE_WITHDRAWAL_BY_ID,
                args = {"base": self.BASE_URL, "funds_transfer_id": funds_transfer_id},
                headers=tokens[0])

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
        return requestor(
                Endpoints.MAKE_DEPOSITS,
                args = {"base": self.BASE_URL},
                headers=tokens[0],
                data=payload)

    def get_deposit(self, tokens, funds_transfer_id: str):
        """
        Get specific deposit under this Wealthsimple Trade account.  
        Where ***funds_transfer_id*** is the id of the deposit  
        """
        return requestor(
                Endpoints.GET_DEPOSIT_BY_ID,
                args = {"base": self.BASE_URL, "funds_transfer_id": funds_transfer_id},
                headers=tokens[0])

    def list_deposits(self, tokens):
        """
        Get all deposits under your Wealthsimple Trade account.
        """
        return requestor(
                Endpoints.LIST_DEPOSITS,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def delete_deposit(self, tokens, funds_transfer_id: str):
        """
        Delete a specific deposit under your Wealthsimple Trade account.
        """
        return requestor(
                Endpoints.DELETE_DEPOSIT_BY_ID,
                args = {"base": self.BASE_URL, "funds_transfer_id": funds_transfer_id},
                headers=tokens[0])

    #! market related functions
    def get_all_markets(self, tokens):
        """
        Grabs all market data including opening and closing hours 
        """
        return requestor(
                Endpoints.GET_ALL_MARKETS,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

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
        return requestor(
                Endpoints.GET_WATCHLIST,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    def add_watchlist(self, tokens, sec_id: str):
        """
        Add security under this Wealthsimple Trade account.    
        Where ***sec_id*** is the security id for the security you want to add.            
        """
        return requestor(
                Endpoints.ADD_TO_WATCHLIST,
                args = {"base": self.BASE_URL, "security_id": sec_id},
                headers=tokens[0])

    def delete_watchlist(self, tokens, sec_id: str):
        """
        Delete a watchlisted securities in your Wealthsimple Trade account.  
        Where ***sec_id*** is the security id for the security you want to delete. 
        """
        return requestor(
                Endpoints.DELETE_FROM_WATCHLIST,
                args = {"base": self.BASE_URL, "security_id": sec_id},
                headers=tokens[0])

    #! exchange functions
    def get_exchange_rate(self, tokens):
        """
        Current Wealthsimple Trade forex USD/CAD exchange rates. 
        """
        return requestor(
                Endpoints.GET_EXCHANGE_RATE,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

    #! fact-sheet functions
    def get_fact_sheets(self, tokens):
        """
        Get all fact-sheets that you have access to under your Wealthsimple account
        """
        return requestor(
                Endpoints.GET_FACT_SHEET,
                args = {"base": self.BASE_URL},
                headers=tokens[0])

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
        return requestor(
            Endpoints.GET_TOP_MARKET_MOVERS,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            params={"type":"losers","limit":limit,"offset":offset})  

    def get_top_gainers_securities(self,
                                   tokens,
                                   offset: int = 0,
                                   limit: int = 20):
        """
        Grab a list of top gainers securities under Wealthsimple trade today.
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
        """
        return requestor(
            Endpoints.GET_TOP_MARKET_MOVERS,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            params={"type":"gainers", "limit":limit, "offset":offset})   
    
    def get_most_active_securities(self,
                                   tokens,
                                   limit: int = 20):
        """
        Grab a list of most active securities under Wealthsimple trade today.  
        Where ***limit*** is the amount of response you want from the request.  
        """
        return requestor(
            Endpoints.GET_TOP_MARKET_MOVERS,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            params={"type":"most_active", "limit":limit})      
    
    def get_most_watched_securities(self,
                                    tokens,
                                    offset: int = 0,
                                    limit: int = 20):
        """
        Grabs all most watched securities under Wealthsimple trade today.
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
        """
        return requestor(
            Endpoints.GET_MOST_WATCHED,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            params={"limit":limit,"offset":offset})  
    
    def get_featured_security_groups(self, tokens):
        """
        Grabs all featured security groups under Wealthsimple trade today
        """
        return requestor(
            Endpoints.GET_FEATURED,
            args={"base": self.BASE_URL},
            headers=tokens[0])
    
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
        return requestor(
            Endpoints.GET_SECURITIES_IN_GROUPS,
            args={"base": self.BASE_URL, "group_id": group_id},
            headers=tokens[0],
            params={"limit":limit,"offset":offset,"filter_type":filter_type})
    
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
        return requestor(
            Endpoints.GET_ALL_GROUPS,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            params={"offset":offset, "limit":limit, "sort_order":order})
        
    #! mobile dashboard functions
    def get_mobile_dashboard(self, tokens):
        """
        Get all info in the mobile dashboard
        """
        return requestor(
            Endpoints.GET_MOBILE_DASHBOARD,
            args={"base": self.BASE_URL},
            headers=tokens[0])
     
    #! global alerts
    def get_global_alerts(self, tokens):
        """
        Grab all global alerts
        """
        return requestor(
            Endpoints.GET_GLOBAL_ALERTS,
            args={"base": self.BASE_URL},
            headers=tokens[0]) 
        
    def get_user_alerts(self, tokens):
        """
        Grab all global alerts
        """
        return requestor(
            Endpoints.GET_USER_ALERTS,
            args={"base": self.BASE_URL},
            headers=tokens[0]) 
        
    #! internal transfers 
    def get_supported_internal_transfers(self, tokens):
        """
        Grabs a list of all support internal transfers
        ! NOT WORKING
        """
        return requestor(
            Endpoints.GET_SUPPORTED_INTERNAL_TRANSFERS,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            response_list=True)
     
    def create_internal_transfers(self, tokens, payload):
        """
        create a internal transfer request  
        currently no wrapper functions.
        """
        return requestor(
            Endpoints.CREATE_INTERNAL_TRANSFER,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            data=payload)   
    
    #! tax-documents
    def get_tax_documents(self, 
                          tokens):
        """
        Grab tax documents of your Wealthsimple account
        """  
        return requestor(
            Endpoints.GET_TAX_DOCUMENTS,
            args={"base": self.BASE_URL},
            headers=tokens[0],
            response_list=True
            )
     
    #! monthly-statements
    def get_monthly_statements(self, tokens):
        """
        Grabs all monthly statements under your Wealthsimple account
        """
        return requestor(
            Endpoints.GET_MONTHLY_STATEMENTS,
            args={"base": self.BASE_URL},
            headers=tokens[0])
    
    def get_monthly_statements_url(self, tokens, pdf_statement_id):
        """
        Grabs a url to a pdf of your statement.  
        Where ***pdf_statement_id*** is the id of the month you want to get.  
        """
        return requestor(
            Endpoints.GET_URL_MONTHLY_STATEMENTS,
            args={"base": self.BASE_URL, "pdf_statement_id": pdf_statement_id},
            headers=tokens[0])

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
    def get_websocket_uri(self, tokens):
        """
        returns websocket url to a wealthsimple websockets 
        "wss://trade-service.wealthsimple.com/websocket?ticket={{TICKET}}&version=2"
        """
        res = requestor(
            Endpoints.GET_WEBSOCKET_URI,
            args={"base": self.BASE_URL},
            headers=tokens[0])
        return "wss://trade-service.wealthsimple.com/websocket?ticket={}&version=2".format(res.ticket)   

    #! functions after this point are not core to the API
    def test_endpoint(self, tokens, data):
        """
        function for testing new endpoints
        """
        # account_id = self.accounts(tokens).personal
        # base_url = self.BASE_URL
        # name = "kepa"
        # k = requests.get(
        #     url="{}documents/new".format(base_url),
        #     params={"filename": name},
        #     headers=tokens[0]
        #     )  
        # print(f"{k.status_code} {k.url}")
        # print(k.headers)
        # print(k.json())
        # r = requests.put(
        #     url="{}".format(k.json()["upload_url"]),
        #     headers={
        #     'Content-type': 'application/json'
        #     },
        #     data=data
        # )
        # print(f"{r.status_code} {r.url}")
        # print(r.headers)
        # print(r.content)
        # f = requests.post(
        #     url="{}documents".format(base_url),
        #     data={"s3_key": k.json()["s3_key"],
        #             "document_type": "notes",
        #             "resource_type": 'Client'},
        #     headers=tokens[0]
        #     )  
        # print(f"{f.status_code} {f.url}")
        # print(f.headers)
        # print(f.json())

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
    def public_find_securities_by_ticker(self, ticker):
        """
        Grabs information about the security resembled by the ticker.  
        Where ***ticker*** is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.
        !May not work on smaller companies or ETFs. 
        """
        return requestor(
            Endpoints.PUBLIC_GET_SECURITIES_BY_TICKER,
            args={"base": self.BASE_PUBLIC_URL, "ticker": ticker})   

    def public_find_securities_by_ticker_historical(self, ticker, time):
        """
        Get a company historical data based on a time.    
        Where ***ticker*** is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.  
        Where ***time*** is ("1d", "1w", "1m", "3m", "1y"): DOES NOT INCLUDE ("all").   
        !May not work on smaller companies or ETFs.  
        """
        return requestor(
            Endpoints.PUBLIC_GET_SECURITIES_HISTORICAL,
            args={"base": self.BASE_PUBLIC_URL, "ticker": ticker, "time": time})   

    def public_top_traded(self, offset: int = 0, limit: int = 5):
        """
        Get top traded companies on Wealthsimple trade.  
        Where ***offset*** is the displacement between the selected offset and the beginning.   
        Where ***limit*** is the amount of response you want from the request.  
        """
        return requestor(
            Endpoints.PUBLIC_GET_TOP_TRADED,
            args={"base": self.BASE_PUBLIC_URL},
            params={"offset":offset, "limit":limit})   

    def public_find_securities_news(self, ticker):
        """
        Get public news based on the ticker.    
        Where ***ticker*** is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.   
        !May not work on smaller companies or ETF. 
        """
        return requestor(
            Endpoints.PUBLIC_GET_SECURITIES_NEWS,
            args={"base": self.BASE_PUBLIC_URL, "ticker": ticker})   

    #! public prefix functions: wealthsimple operational status
    def summary_status(self):
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
        return requestor(
            Endpoints.GET_SUMMARY_STATUS,
            args={"base": self.BASE_STATUS_URL},
            request_status=True
            )   

    def current_status(self):
        """
        Get current status/incidents of wealthsimple trade.    
        the data is in body(content), data could be large. 
        """
        return requestor(
            Endpoints.GET_CURRENT_STATUS,
            args={"base": self.BASE_STATUS_URL},
            request_status=True
            )   

    def historical_status(self):
        """
        Get all previous history status/incidents of wealthsimple trade.   
        the data is in body(content), data could be large. 
        """
        return requestor(
            Endpoints.GET_HISTORICAL_STATUS,
            args={"base": self.BASE_STATUS_URL},
            request_status=True
            )    