<p align="center">
  <a>
    <img src="Wsimple/static/media/logo64.svg">
    <br>
    <img src="https://forthebadge.com/images/badges/contains-technical-debt.svg">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg">
    <img src="https://forthebadge.com/images/badges/uses-badges.svg">
  </a>
</p>

## Getting Started

  #### Prerequisites
  * python and is required to use wsimple
  * to download pip and python goto ["Download Python"](https://realpython.com/installing-python/)
  * for windows click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-windows)
  * for macos click ["Here"](https://realpython.com/installing-python/#how-to-install-python-on-macos)

  #### Installing
  ```bash
  pip install wsimple
  ```
  #### start webserver
  ```bash
  wsimple start
  ```
## API

#### Usage
  ```python
  from Wsimple import Wsimple
  from getpass import getpass

  ws = Wsimple("john.doe@gmail.com", "johndoepass")
  # Wsimple("gmail", "password")

  print(ws.find_securities("AAPL"))
  ```

## Disclaimer
  #### **DO NOT LEVERAGE THIS IN ATTEMPT TO DISRUPT ORDERLY MARKET FUNCTIONS**.
  This software is provided so you can use Wealthsimple trade on your computer duh, but you should understand that you have a responsibility to not engage in illegal trading behaviours that can disrupt orderly market functions. This means that you should not flood the website with orders in a fast manner. You might even get banned or locked out by WealthSimple Trade.

  You would be abusing this tool if you are leveraging it to carry out tactics that would provide you illegitimate personal gains. For example, [Spoofing](https://en.wikipedia.org/wiki/Spoofing_(finance)) is a forbidden tactic that has demonstrable negative effects on the operation of the markets.

  Remember when using this website you are still in agreement with Wealthsimple Trade and Crypto terms of service and they reserve the right to terminate anyone

  My recommendation is to be very conservative about how many orders you place within a small timeframe. I have no idea what
  the maximum amount of orders is by any timeframe, but if you have a gut feeling that it is too much, then it is too much.

  Users of [wstrade-api](https://github.com/ahmedsakr/wstrade-api) have observed that trades in excess of 7 per hour are rejected by the WealthSimple Trade servers. You can use this observation as a baseline of how many trades you can perform on an hourly basis.

  #### **USE AT YOUR OWN RISK**.
  Even though this software is 1000% secure due to everyone running an independent and secluded webserver and that no data is being sent out. But I still must say that this software is not built by or affiliated in way with Wealthsimple Trade or the company Wealthsimple. The use of this software is done at your own discretion and risk and with the agreement that you will be solely responsible for any damage to your computer system or loss of data that results from such activities. By using this software you solely responsible for any damages to you or your Wealthsimple account, and that I will not be liable for any damages that you may suffer connection with downloading, installing, using, modifying or distributing this software.

  to reiterate
  >I take NO responsibility and/or liability for how you choose to use the software. By using the software, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again, ALL software here is for PERSONAL and ONLY PERSONAL use.
