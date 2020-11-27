<p align="center">
  <a>
    <img src="app/static/media/logo64.svg">
    <br>
    <img src="https://forthebadge.com/images/badges/made-with-javascript.svg">
    <img src="https://forthebadge.com/images/badges/open-source.svg">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg">
    <br>
    <img src="https://forthebadge.com/images/badges/powered-by-oxygen.svg">
    <img src="https://forthebadge.com/images/badges/powered-by-overtime.svg">
    <img src="https://forthebadge.com/images/badges/powered-by-responsibility.svg">
  </a>
</p>

### What is the Wsimple project?
Welcome! This project is a web interface and API for Wealthsimple Trade. The main goal this project is to give a simple yet robust interface for Wealthsimple Trade users and also give the ability to allow developers to create projects while hooking straight into their Wealthsimple Trade account. Click [Here](#index) for API wrapper documentation. 

Before using this please read the [disclamer](#disclamer), and due to the nature of this project and goodwill, specific endpoints aren't available.

## Getting Started
  ### Project Status
  <p style="">
  Pre-alpha v1.0
  </p>

  This project is in the pre-alpha stage. if you find any bugs please submit an [issue](https://github.com/yusuf8ahmed/Wsimple/issues/new).

  ### Prerequisites
  * python and pip is required to use/download wsimple
  * to download pip and python goto ["Download Python"](https://realpython.com/installing-python/)
    * for windows click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-windows). Windows Subsystem for linux(wsl) is need for wsimple website to run
    * for macos click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-macos)

  ### Installation
  ```bash
  # Production
  pip install wsimple
  # Testing
  git clone https://github.com/yusuf8ahmed/Wsimple.git
  ```
  #### start website
  ```bash
  # Production
  wsimple start
  # Testing
  python3.9 app
  ```

<a id="index"></a> 

## API

### Usage
  ```python
  from Wsimple import Wsimple

  email = str(input("Enter email: \n>>>"))
  password = str(input("Enter password: \n>>>"))
  try:
      ws = Wsimple(email, password) # Wsimple("email_account", "password")
      tokens = ws.tokens
  except WSOTPUser: # Exception occurs on one time password only.
      otpnumber = int(input("Enter otpnumber: \n>>>"))
      ws = Wsimple.otp_login(email, passw, otpnumber)
      tokens = ws.tokens  

  ws.current_status()
  # check the current operation status of internal Wealthsimple Trade

  print(ws.find_securities(tokens, "GOOG")) 
  # return a list of securities that include GOOG and GOOGL

  ws.make_deposit(tokens, 2000)
  # create deposit order for 2000 CAD into your account

  ws.make_withdrawal(tokens, 6000)
  # create withdrawal order for 6000 CAD into your account

  ws.get_market_hours(tokens, exchange="NYSE")
  # return opening and closing of the exchange NYSE 

  ```

<a id="disclamer"></a> 
## Disclaimer 
  #### **DO NOT LEVERAGE THIS IN ATTEMPT TO DISRUPT ORDERLY MARKET FUNCTIONS**.
  This software is provided so you can use Wealthsimple trade on your computer. **This software is not built or maintained by Wealthsimple Trade or the company Wealthsimple.** Remember your responsibility to not engage in illegal or unethical trading behaviours that can disrupt orderly market functions. Flooding the website/api with orders in a short timeframe may result in getting banned or locked out by Wealthsimple Trade.

  Remember when using this website and/or api you are still under Wealthsimple Trade services and they reserve the right to terminate anyone.

  Users of [wstrade-api](https://github.com/ahmedsakr/wstrade-api) have observed that trades in excess of 7 per hour are rejected by the WealthSimple Trade servers. You can use this observation as a baseline of how many trades you can perform on an hourly basis.

  This product was built with security in mind. This software was made to run personal and local webserver and to assure no data/credentials is being sent out. 
  
  The use of this software is done at your own discretion and risk and with the agreement that you will be solely responsible for any damages. By using this software you agree that you are solely responsible for any damages incurred to you or your account, and that I will not be liable for any damages that you may suffer in connection with downloading, installing, using, modifying or distributing this software.

  **This content, software and/or any comments are not intended to be investment advice or any other kind of professional advice.**

  Parts of this disclaimer are adapted from [wstrade-api](https://github.com/ahmedsakr/wstrade-api)
