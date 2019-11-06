# Single-File Web Crawler

### 1. Summary

- Motivation: working result. Done under the supervise of Dr. Hsieh-Fei Yu, Sinica Academia.

- Task Type: Web crawling

- Topic: Industrial Research

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

  **This script stop working because of the change of website structure.**

  The member information of this website has to be accessed with `POST` request.  I retrieved the whole set of possible `post`payload values by searching the source code of the webpages and the cookie.

- `metal.py` -  crawls [Taiwan Metal Industry Association](http://www.trmsa.org.tw/Member.aspx)
  Since the website is built with AJAX technology, the member information will not be contained in the response of a "direct" HTTP request to the website.  To solve the problem, I use `Selenium` browser simulator to interact with the website and to trigger the browser events, such as mouse clicking, to make the website return the member information. 

- `superFluid.py` - crawls [Taiwan Supercritical Fluid Association](http://www.tscfa.org.tw/)
  The member information can be retrieved with a simple`GET` request. 



Sample results of the three crawlers can be found in `foundry.csc`, `metal.csv`, and `superFluid.csv`,