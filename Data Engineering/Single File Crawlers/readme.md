# Single-File Python Web Crawlers - Industrial Association Membersp

### 1. Summary

- Motivation: professional working result. Done under the supervise of Dr. Hsieh-Fei Yu, Sinica Academia.
- Task type: web scraping
- Topic: industrial research
- Technologies: 

  - **Python 2.7** 
    - argparse

    - Requests

    - BeautifulSoup

    - Selenium

    - Pandas


### 2. Introduction

This repo consists of three single-file web crawlers,  `foundry.py`,`metal.py`, and `superFluid.py`. Each of the crawler is designed to gather the member information from a industrial association's website. Since each of the website is built with different web technology, I have to apply different techniques to access to the data I need:

- `foundry.py` - crawls [Taiwan Foundry Association](http://www.foundry.org.tw:8080/institute/')

  **This script stop working because of the change of the website structure.**

  The member information of this website has to be accessed with `POST` request.  I gathered the whole set of possible `POST` payload values by searching through the source code of the webpages and the cookie.

- `metal.py` -  crawls [Taiwan Metal Industry Association](http://www.trmsa.org.tw/Member.aspx)

  A direct HTTP `GET` request to the website will not receive the response which contains the member information we need because of the application of AJAX technology of the website.  To solve the problem, I use Selenium browser simulator to interact with the website and to trigger some browser events, such as mouse clicking, to send out a `POST` request that makes the website return the member information. 

- `superFluid.py` - crawls [Taiwan Supercritical Fluid Association](http://www.tscfa.org.tw/)

  The member information can be retrieved with a straightforward `GET` request. 

All three scripts can be executed in command line. Sample results of the three crawlers can be found in `foundry.csc`, `metal.csv`, and `superFluid.csv`,