# Primary Mortgage Market Survey (PMMS) data fetcher with MS Excel user interface

### 1. Summary

- Motivation: proof-of-concept.
- Task type: web scraping; automation; business intelligence.
- Topic: NA
- Technologies:
  - VBA (Microsoft Excel) - read config; activate crawler with cmd argument; render result.
  - Python 3.6 with following packages:
    - xlwings - manipulate data in excel file through python
    - requests - download web file
    - pyinstaller - compile python script into executable to enable the application running in the environment without python installation

### 2. Introduction

This repo is a proof-of-concept which demonstrates how a data preparation task in business environment can be done with a well-designed automation tool. By running the macro stored in the master MS excel file, the tool will complete  the following works automatically:

1. activate a web scraping program written in python to download [the PMMS history file](http://www.freddiemac.com/pmms/docs/historicalweeklydata.xls) from [Freddie Mac's Website](http://www.freddiemac.com/pmms/about-pmms.html).
2. fetch the correspondent data entry in the PMMS history file according to the transaction date setting in the master MS excel file.
3. render the data entry back to the MS excel file for user validation. 

### 3. Running Instruction

1. clone this repo.
2. follow the instruction in "Dashboard" worksheet of `master.xlsm` to configure the task.
3. run the task by hitting `run` button.
4. During the program is running, follow the instruction appears on message box (i.e.: hitting `OK`)
5. enjoy the result :beers: