class LoginError(Exception):
    def __init__(self):
        super(LoginError, self).__init__("A Login Error has occurred")
    
class MethodInputError(Exception):
    def __init__(self, message):
        super(MethodInputError, self).__init__(str(message).strip())

class EmptyTokensError(Exception):
    def __init__(self):
        super(EmptyTokensError, self).__init__("Some how the tokens are Empty ?")

class InvalidAccessTokenError(Exception):
    def __init__(self):
        super(InvalidAccessTokenError, self).__init__("An Invalid Access Token Error was, given please try again")

class InvalidRefreshTokenError(Exception):
    def __init__(self):
        super(InvalidRefreshTokenError, self).__init__("An Invalid Refresh Token Error was given, please try again")

class WSOTPUser(Exception):
    def __init__(self):
        super(WSOTPUser, self).__init__("An Wealthsimple otp user account was triggered, please try again and use a try block")

class WSOTPError(Exception):
    def __init__(self):
        super(WSOTPUser, self).__init__("An Wealthsimple otp error happend, please try again and use a try block")

