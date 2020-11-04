"""
Project Name: Wsimple
 Copyright (c) 2020 Chromazmoves
 Released under the Tos of Wealthsimple Trade and Wsimple
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
from .errors import WSOTPUser, WSOTPError
# third party
import requests

class Wsimple:
    """ Wsimple is the main access class to the wealthsimple trade api """
    
    # class assumes first id in account/list is for trading
    # 73 methods and 5 attributes
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
    def __init__(self, 
                 email,
                 password, 
                 verbose_mode=False, 
                 access_mode=False, 
                 otp_mode=False,
                 otp_number=0, 
                 tokens=""):
        """
        This function initializes and logs the user in using the provided 
        email and password. Alternatively, access_mode can be set to True then, 
        users can access misc functions without using a Wealthsimple Trade account.
        If the login is successful, access and refresh tokens are returned in the 
        header. The access token is the key for invoking all endpoints 
        that are not considered misc.  
        """
        otp_status = None
        self.logger = logger # self.logger.add("logfiles/file_{time}.log",  rotation="1 day")
        self.logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="DEBUG")
        self.access_mode = access_mode
        self.verbose = verbose_mode
        if self.access_mode:
            # set function argument tokens to self.tokens
            pass
        else:
            #"create_account": not 1
            payload = {"email":email, "password":password, "timeoutMs": 2e4}
            if otp_mode:
                payload["otp"] = otp_number
            r = requests.post(
                url="{}auth/login".format(self.base_url),
                data=payload
            ) 
            del payload
            print(f"Login status code {r.status_code}")
            if "x-wealthsimple-otp" in r.headers:
                #! one time password code login
                print("Need to Login with one time password")
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
                    raise LoginError
                         
    @classmethod
    def access(cls, verbose=False):
        """
        access misc functions without logging in
        """
        wsimple = cls("", "", verbose_mode=verbose, access_mode=True)
        return wsimple

    @classmethod
    def otp_login(cls, email, password, otp_number):
        #as i don't want to hold email or password, the email and password will have to be sent again
        wsimple = cls(email, password, otp_mode=True, otp_number=otp_number)
        return wsimple
        
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

    #! account related functions
    def get_account_ids(self, tokens):
        """
        Grabs account ids of this WealthSimple Trade account. 
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
        Grabs account info of this WealthSimple Trade account. 
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

    def get_historical_portfolio_data(self, tokens, account: str = None, time: str = "1d"):
        """
        Grabs historical portfolio info for your Wealthsimple Trade account for a specified timeframe. 
        Where __time__ is one of [1d, 1w, 1m, 3m, 1y, all]: autoset 1d.    
        Where __account__ is the account_id received from [get_account](#getaccount): autoset to first accounts_id.    
        """
        logger.debug("get_historical_portfolio_data call")
        if account == None:
            account = self.get_account(tokens)["results"][0]["id"]
        r = requests.get(
            url="{}account/history/{}?account_id={}".format(
                self.base_url, time, account),
            headers=tokens[0]
        )
        logger.debug(f"get_historical_portfolio_data {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_me(self, tokens):
        """
        Grabs Basic information about your Wealthsimple Trade account.
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
        Grabs Advanced/Personal information about your Wealthsimple Trade account. 
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
        Grabs all bank accounts under to your Wealthsimple Trade account. 
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

    def delete_bank_accounts(self, tokens, bank_account_id):
        """
        Grabs all bank accounts under to your Wealthsimple Trade account. 
        """
        logger.debug("delete_bank_accounts")
        r = requests.delete(
            url="{}bank-accounts/{}".format(self.base_url, bank_account_id),
            headers=tokens[0]
        )
        logger.debug(f"delete_bank_accounts {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError()
        else:
            return r.json()

    def get_positions(self, tokens):
        """
        Grabs all securities held by your WealthSimple Trade account.    
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
        Get all current and past orders.
        """
        logger.debug("get_orders")
        r = requests.get(
            url="{}orders".format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_orders {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError()
        else:
            return r.json()

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
        assert (order_type == 'sell_quantity' or order_type == 'buy_quantity')
        assert (sub_type == 'market' or sub_type == 'limit' or sub_type == 'stop_limit')
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
            raise InvalidAccessTokenError
        else:
            return r.json()

    def market_buy_order(self,
                         tokens,
                         security_id: str,
                         account_id: Optional[str] = None,
                         limit_price: int = 1,
                         quantity: int = 1):
        """
        Places a market buy order for a security. Works.  
        """
        try:
            logger.debug("buy_market_order")
            if account_id is None:
                account_id = self.get_account(tokens)["results"][0]["id"]
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

    def market_sell_order(self,
                          tokens,
                          security_id: str,
                          account_id: Optional[str] = None,
                          quantity: int = 1):
        """
        Places a market sell order for a security. Works.
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

    def limit_buy_order(self,
                        tokens,
                        security_id,
                        limit_price,
                        account_id: Optional[str] = None,
                        quantity=1,
                        gtc=False):
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

    def limit_sell_order(self,
                         tokens,
                         limit_price,
                         security_id,
                         account_id: Optional[str] = None,
                         quantity=1,
                         gtc=False):
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

    def stop_limit_buy_order(self,
                             tokens,
                             stop,
                             limit_price,
                             security_id,
                             account_id: Optional[str] = None,
                             quantity=1,
                             gtc=False):
        """
        Places a limit sell order for a security.  
        """
        raise NotImplementedError
    
    def stop_limit_sell_order(self,
                              tokens,
                              stop,
                              limit_price,
                              security_id,
                              account_id: Optional[str] = None,
                              quantity=1,
                              gtc=False):
        """
        Places a limit sell order for a security.  
        """
        raise NotImplementedError
    
    def delete_order(self, tokens, order: str):
        """
        Cancels a order by its id.    
        Where __order__ is order_id from the return of the above functions.   
        """
        logger.debug("delete_order")
        r = requests.delete(
            "{}/orders/{}".format(self.base_url, order),
            headers=tokens[0]
        )
        logger.debug(f"delete_order {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def pending_orders(self, tokens, account_id=None):
        if account_id is None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        orders = self.get_orders(tokens)['results']
        result = []
        for order in orders:
            if order['filled_at'] is None and order['status'] != 'cancelled':
                result.append(order)
        return result
    
    def cancelled_orders(self, tokens, account_id=None):
        if account_id is None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        orders = self.get_orders(tokens)['results']
        result = []
        for order in orders:
            if order['status'] == 'cancelled':
                result.append(order)
        return result

    def filled_orders(self, tokens, account_id=None):
        if account_id is None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        orders = self.get_orders(tokens)['results']
        result = []
        for order in orders:
            if order['status'] == 'posted':
                result.append(order)
        return result

    #! find securitites functions
    def find_securities(self, tokens, ticker: str):
        """
        Grabs information about the security resembled by the ticker.    
        1.Where ticke is the ticker of the company, API will fuzzy.     
        match this argument and therefore multiple results can appear. 
        """
        logger.debug("find_securities")
        r = requests.get(
            url="{}securities?query={}".format(self.base_url, ticker),
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

    def find_securities_by_id_historical(self, tokens, sec_id: str, time: str = "1d", mic: str = "XNAS"):
        """
        Grabs historical information about the security by the security id in a specified timeframe.
        Where __sec_id__ is the internal security id of the security    
        Where __time_ is the timeframe one of [1d, 1w, 1m, 3m, 1y, all] autoset "1d".
        Where __mic__ is the Market Identifier Code for the exchange autoset "XNAS"
        """
        logger.debug("find_securities_by_id_historical")
        r = requests.get(
            url="{}securities/{}/historical_quotes/{}?mic={}".format(
                self.base_url, sec_id, time, mic),
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
        Provides the most recent 20 activitieson this Wealthsimple Trade account.  
        Where type is the activites type you want can be ["deposit", "withdrawal", "dividend", "buy", "sell"] autoset to "all"
        Where limit is the limitation of the response has to be less than 100 autoset 20.       
        Where account_id is the id of your Wealthsimple Trade account.
        """
        if not 1 < limit < 100:
            raise MethodInputError
        if account_id == None:
            account_id = self.get_account(tokens)["results"][0]["id"]
        if type == "all":
            logger.debug("get_activities")
            r = requests.get(
                url="{}account/activities?account-id={}".format(self.base_url, account_id),
                headers=tokens[0]
            )
        else:
            logger.debug("get_activities")
            r = requests.get(
                url="{}account/activities?type={}&account-id={}".format(self.base_url, type, account_id),
                headers=tokens[0]
            )
        logger.debug(f"get_activities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()

    def get_activities_bookmark(self, tokens, bookmark):
        """
        Provides the last 20 activities on the Wealthsimple Trade based on the bookmark.   
        Where bookmark is the string that is that is in the response of [get_activities()](#getactivities).   
        """
        logger.debug("get_activities_bookmark")
        r = requests.get(
            url="{}account/activities?bookmark={}".format(
                self.base_url, bookmark),
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
        make a withdrawal under your Wealthsimple Trade account.
        Where __amount__ is the amount to withdraw
        Where __currency__ is the currency need to be withdrawn(only CAD): autoset to "CAD"
        Where __bank_account_id__ is id of bank account where the money is going to be withdrawn from (can be found in get_bank_accounts function)
        if bank_account_id is not passed then it will pick the first result.
        Where __account_id__ is id of the account that is withdrawing the money (can be found in get_account function).
        if account_id is not passed then it will pick the first result.
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
        Get specific withdrawal under this Wealthsimple Trade account.
        Where __funds_transfer_id__ is the id of the transfer and is in the result of
        make_withdrawal function but can be also found in list_withdrawals function
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
                     amount: int, currency: str = "CAD", 
                     bank_account_id: str = None, 
                     account_id: str = None):
        """
        make a deposit under your Wealthsimple Trade account.
        Where __amount__ is the amount to deposit
        Where __currency__ is the currency need to be transferred(Only CAD): autoset to "CAD"
        Where __bank_account_id__ is id of bank account where the money is going to be deposited to (can be found in get_bank_accounts function)
        if bank_account_id is not passed then it will pick the first result.
        Where __account_id__ is id of the account that is depositing the money (can be found in get_account function).
        if account_id is not passed then it will pick the first result.
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
        Get specific deposit under this WealthSimple Trade account.
        Where funds_transfer_id is the id of the transfer and is in the result of 
        make_deposit function but can be also found in list_deposits function
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
        Get all deposits under your WealthSimple Trade account.
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
        Delete a specific deposit under your WealthSimple Trade account.
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
        Get all market data-hours including the hours. includes every exchange on Wealthsimple Trade.   
        and has the opening and closing time amongst other data.  
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
        Get all data about a specific exchange.  
        Where __exchange__ is the ticker of the company, can be only.     
        {"TSX","CSE","NYSE","BATS","FINRA","OTCBB","TSX-V","NASDAQ","OTC MARKETS","AEQUITAS NEO EXCHANGE"}
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
        Get all watchlisted securities in your Wealthsimple trade account. 
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
        Add security under this WealthSimple Trade account.    
        Where __sec_id__ is the security id for the security you want to add.            
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
        Delete a watchlisted securities in your WealthSimple Trade account.  
        Where __sec_id__ is the security id for the security you want to delete. 
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
        Current WealthSimple Trade USD/CAD exchange rates. 
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
        Get all fact-sheet you have access to on this Wealthsimple account
        It shows ETFs fact sheets.
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
    def get_top_losers_securities(self, tokens, offset=0,limit=20):
        """
        Grab a list of top losers securities under Wealthsimple trade today
        """
        logger.debug("get_top_losers_securities")
        r = requests.get(
            url='{}securities/top_market_movers?type=losers&limit={}'.format(self.base_url, limit),
            headers=tokens[0]
        )
        logger.debug(f"get_top_losers_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json() 

    def get_top_gainers_securities(self, tokens, offset=0,limit=20):
        """
        Grab a list of top gainers securities under Wealthsimple trade today
        """
        logger.debug("get_top_gainers_securities")
        r = requests.get(
            url='{}securities/top_market_movers?type=gainers&limit={}'.format(self.base_url,limit),
            headers=tokens[0]
        )
        logger.debug(f"get_top_gainers_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()  
    
    def get_most_active_securities(self, tokens,  offset=0,limit=20):
        """
        Grab a list of most active securities under Wealthsimple trade today
        """
        logger.debug("get_most_active_securities")
        r = requests.get(
            url='{}securities/top_market_movers?type=most_active&limit={}'.format(self.base_url, limit),
            headers=tokens[0]
        )
        logger.debug(f"get_most_active_securities {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()      
    
    def get_most_watched_securities(self, tokens, offset=0,limit=20):
        """
        Grabs all most watched securities under Wealthsimple trade today
        """
        logger.debug("get_most_watched_securities")
        r = requests.get(
            url='{}securities/most_watched?offset={}&limit={}'.format(self.base_url, offset, limit),
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
        if filter_type == None: 
            r = requests.get(
                url='{}security-groups/{}/securities?offset={}&limit={}'.format(self.base_url, group_id, offset, limit),
                headers=tokens[0]
            )
        else:
            r = requests.get(
                url='{}security-groups/{}/securities?offset={}&limit={}&filter_type={}'.format(self.base_url, group_id, offset, limit, filter_type),
                headers=tokens[0]
            )
        logger.debug(f"get_securities_in_groups {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
    
    def get_all_securities_groups(self, tokens, offset=0, limit=25, sort_order="desc"):
        """
        Grabs all security groups under Wealthsimple trade
        Where __offset__ is >= 0 and autoset to 0
        Where __limit__ is the limitation of the response, has to be greater than 1
        and less than 250 and autoset to 25
        Where __sort_order__ is order of the results and can be ["asc", "desc"] autoset to "desc"
        """
        if not (1 <= limit < 100):
            raise MethodInputError
        elif not offset >= 0:
            raise MethodInputError
        elif not sort_order == ("asc" or "desc"):
            raise MethodInputError
        logger.debug("get_all_securities_groups")
        r = requests.get(
            url="{}security-groups?offset={}&limit={}&sort_order={}".format(
                self.base_url, offset, limit, sort_order),
            headers=tokens[0]
        )
        logger.debug(f"get_all_securities_groups {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
        
    #! mobile dashboard functions
    def get_mobile_dashboard(self, tokens):
        """
        Get all info that is loaded when you Wealthsimple 
        account dashboard
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
    
    def enable_moblie_notification(self, token, type):
        """
        enable a specific type of notification for moblie
        """
        if type not in self.push_notification:
            raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.push_notification for allow notification type on moblie)""")
        notif = self._notification(token, type, "push")
        return notif
    
    def enable_email_notification(self, token, type):
        """
        disable a specific type of notification for email
        """
        if type not in self.email_notification:
            raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.email_notification for allow notification type on email)""")
        notif = self._notification(token, type, "email")
        return notif
    
    def disable_moblie_notification(self, token, type):
        """
        disable a specific type of notification for moblie
        """
        if type not in self.push_notification:
            raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.push_notification for allow notification type on moblie)""")
        notif = self._notification(token, type, "push", enable=False)
        return notif
    
    def disable_email_notification(self, token, type):
        """
        disable a specific type of notification for email
        """
        if type not in self.email_notification:
            raise MethodInputError(f"""given type of notification("{type}") is not allowed (check ws.email_notification for allow notification type on email)""")
        notif = self._notification(token, type, "email", enable=False)
        return notif 
    
    #! quotes
     
    #! global alerts
    def get_global_alerts(self, tokens):
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
     
    #! verification bank institutions 
    def get_bank_verification_institutions(self, tokens):
        logger.debug("get_bank_verification_institutions")
        r = requests.get(
            url='{}bank-verification/institutions'.format(self.base_url),
            headers=tokens[0]
        )
        logger.debug(f"get_bank_verification_institutions {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
     
    #! internal transfers 
    def get_supported_internal_transfers(self, tokens):
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
    def get_tax_documents(self, tokens):
        logger.debug("get_tax_documents")
        account_id = self.get_account(tokens)["results"][0]["id"]
        r = requests.get(
            url='{}tax-documents?account_id={}'.format(self.base_url, account_id),
            headers=tokens[0]
        )
        logger.debug(f"get_tax_documents {r.status_code}")
        if r.status_code == 401:
            raise InvalidAccessTokenError
        else:
            return r.json()
     
    #! monthly-statements
    def get_monthly_statements(self, tokens):
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
        uses the key id from get_monthly_statements method
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

    #! websocket_ticket
    def get_websocket_ticket(self, tokens):
        """
        get websocket ticket
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

    async def test(tokens):
        return None
    
    #! functions after this point are not core to the API
    
    def test_endpoint(self, tokens):
        """
        """
        logger.debug("test endpoint")
        account_id = self.get_account(tokens)["results"][0]["id"]
        r = requests.get(
            url='{}quotes'.format(self.base_url),
            headers=tokens[0]
        )
        print(f"{r.status_code} {r.url}")
        print(r.headers)
        print(r.content)
        # print(r.json())
        return r.json()

    def usd_to_cad(self, tokens, amount: Union[float, int]) -> float:
        """  
        change usd to cad:
        This function is used when selling us dollars to wealthsimple so that they can 
        return you cad dollars
        """
        logger.warning("not working correctly")
        forex = self.get_exchange_rate(tokens)['USD']
        buy_rate = forex['sell_rate']
        return round(amount * buy_rate, 3)

    def cad_to_usd(self, tokens, amount: Union[float, int]) -> float:
        """
        change cad to usd:
        this function is used buying us dollars from wealthsimple so that they can 
        return cad 
        """
        logger.warning("cad to usd => not working correctly")
        forex = self.get_exchange_rate(tokens)['USD']
        sell_rate = forex['buy_rate']
        return round(amount * sell_rate, 2)

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

    def stock_home(self, tokens):
        top_losers = self.get_top_losers_securities(tokens, limit=5)
        top_gainers = self.get_top_gainers_securities(tokens, limit=5)
        top_active = self.get_top_active_securities(tokens, limit=5)
        top_watched = self.get_top_watched_securities(tokens, limit=5)
        get_featured_security_groups = self.get_featured_security_groups(tokens, limit=5)

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
        Get security groups need for search page
        """
        try:
            featured_security_groups = self.get_featured_security_groups(tokens)
            get_top_losers_securities = self.get_top_losers_securities(tokens)
            get_top_gainers_securities = self.get_top_gainers_securities(tokens)
            get_top_gainers_securities = self.get_most_active_securities(tokens)
            get_most_watched_securities = self.get_most_watched_securities(tokens)
            return {
                "featured_security_groups": featured_security_groups,
                "most_watched": get_top_losers_securities,
                "most_active": get_top_gainers_securities,
                "top_gainers": get_top_gainers_securities,
                "top_losers": get_most_watched_securities,
            }
        except InvalidAccessTokenError:
            logger.error("search_page InvalidAccessTokenError")
            raise InvalidAccessTokenError

    def dashboard(self, tokens):
        """
        Get dashboard needed for /home route.
        dry test:

        #v1: 2+ seconds - 11 calls
        #v2: 1-2 seconds - 5 calls
        #-v3: 1-2 seconds - 4 calls
         #-v3: 0-1 seconds - 2 calls
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

    #! all functions after here are public and (can be used without logging in).
    @staticmethod
    def public_find_securities_by_ticker(ticker):
        """
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/{}".format(base_url_public, ticker)
        )
        # or json.loads(r.content)
        return r.json()

    @staticmethod
    def public_find_securities_by_ticker_historical(ticker, time):
        """
        staticmethod: get a company historical data based on time and by the actual ticker.    
        1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.  
        2.Where TIME is ("1d", "1w", "1m", "3m", "1y"): DOES NOT INCLUDE ("all").   
        ?May not work on smaller companies or ETFs.  
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/{}/historical_quotes/{}".format(
                base_url_public, ticker, time)
        )
        # json.loads(r.content)
        return r.json()

    @staticmethod
    def public_top_traded(offset=0, limit=5):
        """
        staticmethod: get top traded companies on wealthsimple trade.  
        1.Where OFFSET is the displacement between the selected offset and the beginning.   
        2.Where LIMIT is the amount of response you want from the request.  
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="""{}securities/top_traded?offset={}&limit={}""".format(
                base_url_public, offset, limit)
        )
        return r.json()

    @staticmethod
    def public_find_securities_news(ticker):
        """
        staticmethod: get public news based on ticker name.    
        1.Where TICKER is the ticker of the company or ETF. Ex. AMZN, APPL, GOOGL, SPY.   
        ?May not work on smaller companies or ETF. 
        """
        base_url_public = "https://trade-service.wealthsimple.com/public/"
        r = requests.get(
            url="{}securities/{}/news".format(base_url_public, ticker)
        )
        return r.json()

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
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/summary.json"
        )
        return json.loads(r.content)

    @staticmethod
    def current_status():
        """
        staticmethod: get current status/incidents of wealthsimple trade.    
        ?the data is in json format in body/content, json could be large. 
        """
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/status.json"
        )
        return json.loads(r.content)

    @staticmethod
    def historical_status():
        """
        staticmethod: get all previous history status/incidents of wealthsimple trade.   
        ?the data is in json format in body/content, json is large.  
        """
        r = requests.get(
            url="https://status.wealthsimple.com/api/v2/incidents.json"
        )
        return json.loads(r.content)
