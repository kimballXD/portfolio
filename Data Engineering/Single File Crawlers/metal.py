# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 09:59:16 2016
    Crawl membership list of Taiwan Metal Indsutry Association (http://www.trmsa.org.tw/Member.aspx)
@author: Wu
"""

from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import time
import traceback
import pickle


def main(filePath, startIdx, endIdx, retryPath):
    """
    Save csv file to `filePath`. Default `filPath` is "metal.csv" of working directory.
    Uf crawling failed, current parsed results will saved to "metalSave.pkl". 
    Specify this file using cmd arg `--retryPath` to resume crawling starting from the failed page
    """

    # initalize selenium webdriver and crawl the page index
    driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
    if driver_path not in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + driver_path
    
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.get('http://www.trmsa.org.tw/Member.aspx')
    submit = driver.find_element_by_id('ctl00_ContentPlaceHolder1_queryImageButton')
    submit.click()
    
    enName = driver.find_elements_by_css_selector('.catalog1 a:nth-of-type(2)')
    enName.extend(driver.find_elements_by_css_selector('.catalog2 a:nth-of-type(2)'))
    enName = [x.text for x in enName]
    
    
    # start from the saved file or use a fresh start
    if os.path.isfile(retryPath):
        saved = pickle.load(open(retryPath,'rb'))
    else:
        saved = {'dataList':None, 'index':None, 'load':False}
        
    if saved['load']:
        dataList = saved['dataList']
        start = min(saved['index']-1, 0)
        print 'LoAe saved file!'    
    else:
        dataList = []
        start = 0
        print  'starting from page {}'.format(start+1)

    # crawl pages
    try:
        start = start if not startIdx else startIdx
        end = len(enName) if not endIdx else endIdx + 1 
        for index in range(start , end):
            # has to 'refind' element whenver page has any chaged. even just reload
            entries = driver.find_elements_by_css_selector('.catalog1 a:nth-of-type(1)')  
            entries.extend(driver.find_elements_by_css_selector('.catalog2 a:nth-of-type(1)'))
            entry = entries[index]
            entry.click()
            page = driver.page_source
            driver.back()
            soup = bs(page)
            dataDict={'name':soup.select('#ctl00_ContentPlaceHolder1_nameLabel')[0].text,
                      'registerNo':soup.select('#ctl00_ContentPlaceHolder1_uidLabel')[0].text,
                      'address':soup.select('#ctl00_ContentPlaceHolder1_addrLabel')[0].text,
                      'since':soup.select('#ctl00_ContentPlaceHolder1_setDateLabel')[0].text,
                      'capital':soup.select('#ctl00_ContentPlaceHolder1_capitalLabel')[0].text,
                      'employee':soup.select('#ctl00_ContentPlaceHolder1_employeeLabel')[0].text,
                      'productType':soup.select('#ctl00_ContentPlaceHolder1_itemLabel')[0].text,
                      'product':soup.select('#ctl00_ContentPlaceHolder1_productLabel')[0].text,
                      'source':driver.current_url,
                      'enName':enName[index]}
            dataList.append(dataDict)
            
            # rest for every page
            print 'page {}/{} finished. take a rest!'.format(index + 1, end)
            time.sleep(1)
            if index%10 == 0:
                time.sleep(3)
                
    except:
        traceback.print_exc()
        saved['dataList'] = dataList
        saved['index'] = index
        saved['load'] = True
        pickle.dump(saved, open(retryPath,'wb'))
        return saved
    
#%%
    # reindex data
    data = pd.DataFrame(dataList)
    data = data.drop_duplicates()
    data['NGOname'] = u'台灣區金屬品冶製工業同業公會'
    data['NGOtype'] = u'產業公會'
    data['orgType'] = u''
    data['id'] = u''
    data=data.reindex_axis(['id','NGOname','NGOtype','name','orgType','address',
                            'employee','capital','since','registerNo','productType',
                            'product','source','enName'], 1)
    data.to_csv(filePath, encoding='utf8',index=False,sep=';')
    print 'job has done for metal Association'
    print 'file Destination '+filePath
    print ''
    
#%%
if __name__=='__main__':
    import argparse
    import os
        
    parser = argparse.ArgumentParser()
    parser.add_argument('filePath', nargs='?',
                        default = os.path.join(os.getcwd(), 'metal.csv'))                     
    parser.add_argument('--startIdx', nargs='?', type=int, default=0)
    parser.add_argument('--endIdx', nargs='?', type=int, default=0)
    parser.add_argument('--retryPath',nargs='?',
                        default = os.path.join(os.getcwd(), 'metalSaved.pkl'))   
    args = parser.parse_args()
    main(args.filePath, args.startIdx, args.endIdx, args.retryPath)
