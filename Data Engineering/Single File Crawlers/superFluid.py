# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 15:19:34 2016
    Crawl membership list of Taiwan Supercritical Fluid Association ('http://www.tscfa.org.tw/')
@author: Wu
"""
#%%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re


def main(filePath, startPage, endPage):    
    #c rawl index page
    host='http://www.tscfa.org.tw/'
    indexPage = requests.get('http://www.tscfa.org.tw/group.asp#')
    soup = bs(indexPage.text, 'html.parser')
    pages = int(soup.select('font')[1].text.split('/ ')[-1])

    # start crawling 
    dataList=[]    
    start = 1 if not startPage else startPage
    end = pages + 1 if not endPage else endPage + 1 
    for page in range(start, end):           
        pageUrl = 'http://www.tscfa.org.tw/group.asp?page={}&ParentID=&Condition=&ConditionKey='.format(page)
        pageHtml = requests.get(pageUrl)
        soup = bs(pageHtml.text, 'html.parser') 
        urls = soup.select('a[onclick]')
        urls = [host+ re.search('"(.+?)"', x.get('onclick')).group(1) for x in urls]
        
        # items 
        for url in urls:
            page = requests.get(url)
            page.encoding = 'big5'
            soup = bs(page.text, 'html.parser')
            tables = soup.select('table')           
            tds = tables[2].select('td')
            dataDict={'id':tds[9].text,  #會員編號
                      'name':tds[12].text.strip(),  #公司名稱
                      'address':tds[18].text.strip(), #地址
                      'product':tds[24].text.strip(), #產品
                      'source':url}
            dataList.append(dataDict)
            
    # reindex crawled data
    data=pd.DataFrame(dataList)
    data['NGOname'] = u'台灣超臨界流體協會'
    data['NGOtype'] = u'產業公會'
    data['orgType'] = u''
    data['employee'] = u''
    data['capital'] = u''
    data['since'] = u''
    data['registerNo'] = u''
    data['product'] = u''
    data['enName'] = u''
    data = data.reindex_axis(['id','NGOname','NGOtype','name','orgType','address','employee','capital','since','registerNo','productType','product','source','enName'],1)
    data.to_csv(filePath,encoding='utf8',index=False,sep=';')

    print 'job has done for superFluid Association, get {} records'.format(len(data))
    print 'file Destination '+filePath
    print ''
    return data
    #%%
if __name__=='__main__':
    import argparse
    import os
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filePath', nargs='?',
                        default = os.path.join(os.getcwd(), 'superFluid.csv'))                     
    parser.add_argument('--startPage', nargs='?', type=int, default=0)
    parser.add_argument('--endPage', nargs='?', type=int, default=0)
    args = parser.parse_args()
    main(args.filePath, args.startPage, args.endPage)
        

