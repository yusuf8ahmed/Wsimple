<p align="center">
  <a>
    <img src="images/logo64.svg">
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

## What is the Wsimple project?
Welcome! This project is an API and Web interface(In-development) for Wealthsimple Trade. The main goal of this project is to give developers the ability to create projects while hooking them straight into their Wealthsimple Trade account. Click [Here](https://yusuf8ahmed.github.io/Wsimple/api/api.html#app.api.api.Wsimple) for API wrapper documentation. When looking for a specific function use the left navbar to find it.

Before using the API, please read the [disclamer](#disclamer), and due to the nature of this project and goodwill, specific endpoints aren't available.

**This library was created with non-coders in mind and needs a minimal understand of python to get started.**

## Getting Started
  ### Project Status

  _v2.0.0_  

  This project is in the pre-alpha stage. if you find any bugs please submit an [issue](https://github.com/yusuf8ahmed/Wsimple/issues/new).

  ### Prerequisites
  * **python3+**, **pip** and **node** are required to use wsimple
  * to download pip and python go to ["Download Python"](https://realpython.com/installing-python/)
    * for windows click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-windows). 
    * for macos click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-macos)
  * to download node go to ["Download Node"](https://www.edureka.co/blog/node-js-installation/)

  ### Project Ideas
  * Buy/sell a stock as the end of every month.
  * Automatically create a deposit/withdrawal order every month.
  * Create a internal transfer order to your wealthsimple TSFA, invest accounts every month.
  * Automatically send tax and monthly trading statements to your email.
  * Create a system to do dollar cost averaging (**DCA**) or dividend reinvestment plan (**DRIP**)

  ### Install
  ```bash
  pip install wsimple 
  ```
  #### start website (Not finished)
  ```bash
  wsimple start
  ```

<a id="index"></a> 

## API
### Usage
  ```python
  from wsimple.api import Wsimple

  def get_otp():
      return int(input("Enter otpnumber: \n>>>"))

  email = str(input("Enter email: \n>>>"))
  password = str(input("Enter password: \n>>>"))

  ws = Wsimple(email, password, otp_callback=get_otp) 

  print(ws.get_market_hours(exchange="NYSE")) 

  # check the current operation status of internal Wealthsimple Trade
  print(ws.current_status())
  
  # return a list of securities that include GOOG and GOOGL
  print(ws.find_securities("GOOG")) 
  
  # create deposit order for 2000 CAD into your account
  ws.make_deposit(2000)
  
  # create withdrawal order for 6000 CAD into your account
  ws.make_withdrawal(6000)
  
  # return opening and closing of the exchange NYSE
  print(ws.get_market_hours(exchange="NYSE"))
  ```

<a id="disclamer"></a> 

## Disclaimer

  This software is provided so you can use Wealthsimple trade on your computer. This software is not built or maintained by Wealthsimple Trade or the company Wealthsimple. Remember your responsibility to not engage in illegal or unethical trading behaviours that can disrupt orderly market functions. Flooding the API/web-app with orders in a short time-frame may result in getting banned or locked out by Wealthsimple Trade.

  Remember when using this website and/or api you are still under Wealthsimple Trade services and they reserve the right to terminate anyone.

  **Wealthsimple Trade reserves the right to monitor anyone's trading activity and block transactions if the trading activity is determined to be inappropriate**

  Users of [wstrade-api](https://github.com/ahmedsakr/wstrade-api) have observed that trades in excess of 7 per hour are rejected by the WealthSimple Trade servers. You can use this observation as a baseline of how many trades you can perform on an hourly basis.

  This product was built with security in mind. This software was made to run personal and local webserver and to assure no data/credentials is being sent out. 
  
  The use of this software is done at your own discretion and risk and with the agreement that you will be solely responsible for any damages. By using this software you agree that you are solely responsible for any damages incurred to you or your account, and that I will not be liable for any damages that you may suffer in connection with downloading, installing, using, modifying or distributing this software.

  **This content, software and/or any comments are not intended to be investment advice or any other kind of professional advice.**

  Parts of this disclaimer are adapted from [wstrade-api](https://github.com/ahmedsakr/wstrade-api)
