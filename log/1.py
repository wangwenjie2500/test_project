# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 10:40:03 2015
@author: zhigang
"""

import urllib
import re   
from bs4 import BeautifulSoup 
import time

class my_qiubai:
    def __init__(self):        
        self.stories = []
        self.output ="E:\\02 python抓包\\01 糗百\\qiubai_hot_"+time.strftime('%Y-%m-%d',time.localtime(time.time()))+".txt"
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.pagecount = 1
        print('Spider has started...')
        
    def getPageCount(self):
        url = 'http://www.qiushibaike.com/hot/page/1'
        nowcontent = urllib.request.urlopen(urllib.request.Request(url,headers = self.headers)).read().decode('utf-8') 
        soup = BeautifulSoup(nowcontent)
        pagelist = soup.find("div", {"class": "pagenumber"}).stripped_strings
        for page in pagelist:            
           self.pagecount = int(page)             
        
    
    def getPageContent(self,pagenumber):
        url = 'http://www.qiushibaike.com/hot/page/' + str(pagenumber)
        #prepare the headers which will be needed when get request for quishibaike    
        request = urllib.request.Request(url,headers = self.headers)
        response = urllib.request.urlopen(request)
        try:
            content = response.read().decode('utf-8')
            
            pattern = re.compile('<div.*?class="author">.*?<a.*?<img .*?/>(.*?)</a>.*?<div.*?class="content">(.*?)</div>(.*?)<div class="stats">',re.S)
            items = re.findall(pattern,content)  
            
            for item in items:
                #item0:author_name;item1:content;item2:img
                hasImg = re.search('img',item[2])
                if not hasImg:
                    story=(item[0].strip()+":\n"+item[1].strip()+'\n')                   
                    self.stories.append(story)
        except urllib.error.HTTPError as e:
            if(e.code=='404'):
                return
            else:
                print(e.code)
                return
                
    def loadPage(self):
        self.getPageContent(1)
        
    def write(self):
        i=1
        with open(self.output,'w+',encoding='utf-8') as f:
            for story in self.stories:               
                f.write(str(i)+".\t"+story+"\n")
                i = i+1
        print(self.output+' has been stored.')
        
    def viewAll(self):
        startindex = 1
        self.getPageCount()
        for i in range(startindex,self.pagecount+1):
            self.getPageContent(1)            
            print('Page:'+str(i)+' has been fetched...')
        print('All pages have been fetched...')
    
        
spider = my_qiubai()
spider.viewAll()
spider.write()
print('Spider program stoped...')
