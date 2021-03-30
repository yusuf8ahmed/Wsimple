"""
Name: Chromazmoves  
Project Name: Wsimple   
File Name: Wsimple/api/errors.py   
**File: Definition of all Wsimple Exceptions** 
"""

class LoginError(Exception):
    """Error thrown when user login failed"""
    def __init__(self):
        super(LoginError, self).__init__("A Login Error has occurred")
    
class MethodInputError(Exception):
    """Error thrown when an input to a method is unacceptable"""
    def __init__(self, message):
        super(MethodInputError, self).__init__(str(message).strip())

class EmptyTokensError(Exception):
    """Error thrown when an tokens list is empty"""
    def __init__(self):
        super(EmptyTokensError, self).__init__("tokens are empty?")

class InvalidAccessTokenError(Exception):
    """Error thrown when an access token is invalid"""
    def __init__(self):
        super(InvalidAccessTokenError, self).__init__("An Invalid access token error was given, please try again")

class InvalidRefreshTokenError(Exception):
    """Error thrown when an refresh token is invalid"""
    def __init__(self):
        super(InvalidRefreshTokenError, self).__init__("An Invalid refresh token error was given, please try again")

class OTPCallbackNone(Exception):
    """Error thrown when otp_callback == None"""
    def __init__(self):
        super(OTPCallbackNone, self).__init__("An wealthsimple otp user account was triggered, please use a callback function")

class WSOTPError(Exception):
    """Error thrown when an otp error occurs"""
    def __init__(self):
        super(WSOTPError, self).__init__("An Wealthsimple otp error happend, please try again and use a try block")
        
class WSOTPLoginError(Exception):
    """Error thrown when an otp login error occurs"""
    def __init__(self):
        super(WSOTPLoginError, self).__init__("An Wealthsimple otp login error happend, please try again")
        
class TSXStopLimitPriceError(Exception):
    """Error thrown when a stop order with a diffrent stop and limit price is made on a TSX/TSX-V securities"""
    def __init__(self):
        super(TSXStopLimitPriceError, self).__init__("TSX/TSX-V securities must have an equivalent stop and limit price")
        
class WealthsimpleServerError(Exception):
    """Error thrown when a endpoint returns a 5XX http code"""
    def __init__(self):
        super(WealthsimpleServerError, self).__init__("Wealthsimple endpoint might be down: return a 5XX http code")
        
class RouteNotFoundException(Exception):
    """Error thrown when a endpoint returns a 5XX http code"""
    def __init__(self):
        super(RouteNotFoundException, self).__init__("Wealthsimple endpoint not found: return a 404 http code")

