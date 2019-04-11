# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
import time
import pymongo

class BaixingpageSpider(scrapy.Spider):
    name = "baixingPage"
    allowed_domains = ["baixing.com"]

    pages =[]
    TotalPageNum = 0
    nowPageNum =-1
    errorNum = 0

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://www.baidu.com/link?url=JBjBHjY6RFS4wsN8f1izkk4H7fHGx6vM-Sa1chdMW4NB5pTNAwfc_AKTjxo2g5Zp&wd=&eqid=92491f5100030068000000035a03e46e',
        'Cache-Control':'max-age=0',
        'Host':'shanghai.baixing.com',
        'Upgrade-Insecure-Requests':'1',
        'Cookie':'__trackId=150961423812263; __city=shanghai; __s=l10201b12rdu0trh8fser1l231; __admx_track_id=nrc_w4tqKKwXK5Qx8J6ybA; __admx_track_id.sig=gAxkNXI0CRxMPLksJXPLLWkS2us; __sense_session_pv=38; Hm_lvt_5a727f1b4acc5725516637e03b07d3d2=1509614239,1510204531; Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2=1510205541'
    }

    def __init__(self):
        classfile = codecs.open("final_page.txt", "r", "utf-8")
        file = classfile.read()
        classfile.close()
        self.pages = file.split("\n")
        self.TotalPageNum = len(self.pages)

        errorUrlFile = codecs.open("errorUrl.txt", "w", "utf-8")
        errorUrlFile.close()

        logFile = codecs.open("log.txt", "w", "utf-8")
        logFile.close()
        time.sleep(30)
        connection = pymongo.MongoClient(self.settings['MONGODB_SERVER'], self.settings['MONGODB_PORT'])
        db = connection[self.settings['MONGODB_DB']]
        self.collection = db[self.settings['MONGODB_COLLECTION']]
        

    def start_requests(self):
        self.nowPageNum = self.nowPageNum + 1
        site = self.pages[self.nowPageNum]
        yield scrapy.http.Request(url=site, method="GET", headers=self.hdr, callback=self.parse)

    def parse(self, response):
        logFile = codecs.open("log.txt", "a", "utf-8")
        logFile.write("Rate: "+str(self.nowPageNum)+"/"+str(self.TotalPageNum))
        logFile.write("\n")
        pageBody = response.body
        pageUrl = response.url
        if pageUrl == self.pages[self.nowPageNum]:
            endIndex = pageUrl.find('/',28)
            pageClass = pageUrl[28:endIndex]
            temp = {
                '_id': pageUrl,
                'class': pageClass,
                'body': pageBody
            }
            try:
                self.collection.insert(temp)
            except:
                logFile.write("DuplicateKeyError")
                logFile.write('\n')
        else:
            self.errorNum = self.errorNum+1
            errorUrlFile = codecs.open("errorUrl.txt", "a", "utf-8")
            errorUrlFile.write(self.pages[self.nowPageNum])
            errorUrlFile.write('\n')
            errorUrlFile.close()
            logFile.write("UrlNotMatchError errorTimes: "+str(self.errorNum))
            logFile.write('\n')
            time.sleep(60)

        time.sleep(1)
        self.nowPageNum = self.nowPageNum + 1
        if self.nowPageNum < self.TotalPageNum-1:
            site = self.pages[self.nowPageNum]
            yield scrapy.http.Request(url=site, method="GET", headers=self.hdr, callback=self.parse)




        

