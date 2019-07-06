# Primary Mortgage Market Survey (PMMS) data fetcher with MS Excel user interface

### 1. Summary

- Motivation: Proof-of-concept.
- Task Type: Web Scraping; Automation; Business Intelligence.
- Topic: NA
- Technologies:
  - VBA (Microsoft Excel) - read config; activate crawler with cmd argument; render result.
  - Python
    - xlwings - manipulate data in excel file through python
    - requests - download web file
    - pyinstaller - compile python script into executable to enable the application running in the environment without python installation
- DISCLAMMER: This program is developed with personal free time and equipment. 

### 2. Introduction

This repo is a proof-of-concept which demonstrates how a data preparation task in business environment can be done with a well-designed automation tool. By running the macro stored in the master MS excel file, the tool will complete  the following works automatically:

1. activate a web scraping program written in python to download [the PMMS history file](http://www.freddiemac.com/pmms/docs/historicalweeklydata.xls) from [Freddie Mac's Website](http://www.freddiemac.com/pmms/about-pmms.html).
2. fetch correspondent data entry in the PMMS history file according to the transaction date setting configured in excel file.
3. render the data entry back to the MS excel file for user validation. 

It's intuitive, easy-to-use, and essentially effortless process. By using this tool, staffs can reduce their effort on data stewardship to practically zero and instead dedicate their time and expertise on other more valuable works. 

### 3. Running Instruction

1. clone this repo.
2. follow the instruction in "Dashboard" worksheet of `master.xlsm` to configure the task.
3. run the task by hitting `run` button.
4. During program is running, follow the instruction appears on message box (i.e.: hitting `OK`)
5. enjoy the result :beers: