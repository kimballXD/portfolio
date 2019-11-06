# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:35:10 2019

Crawling the member list of Taiwan Foundry Association (http://www.foundry.org.tw:8080/institute/')
20191106: stop working because the changing of the site structure

@author: Wu
"""

#%%
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

host='http://www.foundry.org.tw:8080/institute/'
queryUrl='http://www.foundry.org.tw:8080/institute/listFactory.do?forward=factorys&isFree=false'
    
formData={'factory.corpName': '',
          'factory.corpType': '',
          'factory.moldingMethod': '-1',
          'factory.remark': '',
          'factoryConvert.breadWinningProduct': '-1',
          'factoryConvert.bwproductCondition': '-1',
          'factoryConvert.isoCondition': '-1',
          'x': '28',
          'y': '15'}
 
formData2={'factory.corpName': '',
           'factory.corpType': '',
           'factory.moldingMethod': '-1',
           'factory.remark': '',
           'factoryConvert.breadWinningProduct': '-1',
           'factoryConvert.bwproductCondition': '-1',
           'factoryConvert.isoCondition': '-1',
           'toPage': '',
           'nextPages': '1'}
 
productTypeDict={'aa': u'鑄造設備廠',
                 'zz': u'其它',
                 'bb': u'鑄造材料廠',
                 'cc': u'模型製造廠',
                 'dd': u'鑄件生產廠',
                 'gg': u'材料設備代理',
                 'ee': u'鑄造顧問',
                 'hh': u'學術／研究機構',
                 'ff': u'鑄件買賣'} 

itemTypeDict={'factory.autoPart': u'汽機車零件',
              'factory.aviation': u'航空國防零件',
              'factory.axis': u'軸件',
              'factory.boatPart': u'船舶及機械零件',
              'factory.engine': u'壓縮機及發動機',
              'factory.handcraft': u'手工具',
              'factory.motor': u'馬達及減速機',
              'factory.mould': u'模具',
              'factory.pipe': u'管接頭、凸緣及閥',
              'factory.pump': u'抽水機',
              'factory.sportingGoods': u'休閒及體育用品',
              'factory.tool': u'工具機及零件'}


def crawlProductType(prodType, startPage, endPage, dataDict):
    #  get productType indexPage
    session = requests.session()
    session.get('http://www.foundry.org.tw:8080/institute/listNotice.do?forward=manfactures')
    formData['factory.corpType'] = prodType
    urlPage = session.post(queryUrl, data = formData)
    soup = bs(urlPage.text)
    pages = len(soup.select('#pageselect option'))

    
    start = 1 if not startPage else startPage
    end = pages + 1 if not endPage else endPage + 1 
    print 'crawling {} from {} to {}....'.format()
    for page in range(start, end):                        
        if page != 1:
            formData2['toPage'] = str(page)
            formData2['factory.corpType'] = prodType
            urlPage = session.post(queryUrl, data = formData2)                                            
        soup = bs(urlPage.text, 'lxml')
        urls = soup.select('a.aNews1')
        urls = [host + x.get('href') for x in urls]
        
        # for every url in the given page
        for url in urls:
            urlId = re.search('id=(\d+)', url).group(1)
            if urlId in dataDict:
                continue
            
            # parse item 
            itemPage = requests.get(url)
            soup = bs(itemPage.text,'lxml')
            tables = soup.select('table')
            rows = tables[-4].select('td.zt12px_10')
            rows = [x.find_next_siblings('td')[1] for x in rows]
            productType = tables[-4].find_all(lambda tag: True if ((tag.name=='input')&(tag.get('checked')=='checked')&(tag.get('name')=='factory.corpType')) else False)
            productType = [productTypeDict[x.get('value')] for x in productType]
            itemType = tables[-4].find_all(lambda tag: True if ((tag.name=='input')&(tag.get('checked')=='checked')&(tag.get('name')in ['factory.autoPart', 'factory.aviation', 'factory.axis', 'factory.boatPart', 'factory.engine', 'factory.handcraft', 'factory.motor', 'factory.mould', 'factory.pipe', 'factory.pump', 'factory.sportingGoods', 'factory.tool'])) else False)
            itemType = [itemTypeDict[x.get('name')] for x in itemType]
            itemType = list(set(itemType))
            
            # dump
            dataDict[urlId] = {'id':rows[0].text.strip(),
                    'name':rows[3].text.strip(),
                    'address':rows[18].text.strip(),
                    'employee':rows[6].text.strip(),
                    'capital':rows[1].text.strip(),
                    'since':rows[5].text.strip(),
                    'registerNo':rows[11].text.strip(),      
                    'product':itemType,
                    'productType':productType,
                    'source':url,
                    'enName':rows[4].text.strip()}
            
#%%            
def main(args):
    
    dataDict = {}    
    if not args.prodType:
        # crawl for all productType    
        for key in productTypeDict:        
            crawlProductType(key, 0, 0, dataDict)
    else:
        # crawl onlyOne productType
        crawlProductType(args.prodType, args.startPage, args.endPage, dataDict)

    # reindex data
    data = pd.DataFrame(dataDict).T
    data['NGOname'] = u'台灣鑄造學會'
    data['NGOtype'] = u'產業公會'
    data['orgType'] = u''
    data=data.reindex_axis(['id','NGOname','NGOtype','name','orgType','address','employee','capital','since','registerNo','productType','product','source','enName'],1)
    data.to_csv(args.filePath,encoding='utf8',index=False,sep=';')

    print 'job has done for foundry Association, get {} records'.format(len(data))
    print 'file Destination '+ args.filePath

    #%%
if __name__=='__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('filePath',nargs='?',default=os.path.join(os.getcwd(), 'foundry.csv'))
    parser.add_argument('--prodType',nargs='?')
    parser.add_argument('--startPage',nargs='?',type=int, default=0)
    parser.add_argument('--endPage',nargs='?',type=int, default=0)
    args = parser.parse_args()
    
    main(args)
        