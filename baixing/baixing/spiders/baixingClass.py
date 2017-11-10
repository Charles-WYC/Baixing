# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
import time

class BaixingclassSpider(scrapy.Spider):
    name = "baixingClass"
    allowed_domains = ["baixing.com"]
    baseSite = 'http://shanghai.baixing.com'
    classes =[]
    #classRe =[]
    nowClassNum = 163
    totalLinks = 0
    pretotalLinks = 0
    requestTime = 0
    iterationTime = 1
    errorPageNum = 0
    errorPages =set()

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
        classfile = codecs.open("class.txt", "r", "utf-8")
        file = classfile.read()
        classfile.close()
        self.classes = file.split("\n")
        print len(self.classes)
        f = codecs.open("page_1.txt", "w", "utf-8")
        f.close()
        # for classSting in self.classes:
        #     index = classSting.find('/',1)
        #     self.classRe.append(classSting[0:index+1])

    def start_requests(self):
        site = self.baseSite+self.classes[self.nowClassNum]
        yield scrapy.http.Request(url=site, method="GET", headers=self.hdr, callback=self.parse)

    def parse(self, response):
        self.requestTime = self.requestTime + 1
        allA = response.xpath("//a[@target='_blank']")
        nextPageA = response.xpath(u"//a[text()='下一页']")
        nextPagelink = nextPageA.xpath("@href").extract_first()
        final = set()
        for A in allA:
            href = A.xpath("@href").extract_first()
            if(href != None and re.match(self.baseSite+'/[a-z]+/'+'a[0-9]+.html', href)):
                final.add(href)
                self.totalLinks = self.totalLinks + 1
        f = codecs.open("page_1.txt","a","utf-8")
        for href in final:
            f.write(href)
            f.write('\n')
        f.close()
        if self.pretotalLinks == self.totalLinks:
            self.errorPageNum = self.errorPageNum + 1
            self.errorPages.add(self.classes[self.nowClassNum])
        self.pretotalLinks = self.totalLinks
        print "IterationTime: "+str(self.iterationTime)
        print "ClassRate: "+str(self.nowClassNum)+"/"+str(len(self.classes))
        print "requestTime: "+str(self.requestTime)
        print "totalLinks: "+str(self.totalLinks)
        print "errorPageNum: "+str(self.errorPageNum)
        print "begin sleep 3s"

        time.sleep(1)

        if nextPagelink == None:
            print "changeClass"
            self.nowClassNum = self.nowClassNum + 1
            if self.nowClassNum < len(self.classes)-1:
                nextSite = self.baseSite+self.classes[self.nowClassNum]
                yield scrapy.http.Request(url=nextSite, method="GET", headers=self.hdr, dont_filter=True, callback=self.parse)
            else:
                if self.errorPageNum != 0:
                    self.classes = list(self.errorPages)
                    self.errorPages.clear()
                    self.errorPageNum = 0
                    self.iterationTime = self.iterationTime + 1
                    self.nowClassNum = 0
                    print self.classes         
                    nextSite = self.baseSite+self.classes[self.nowClassNum]
                    yield scrapy.http.Request(url=nextSite, method="GET", headers=self.hdr, dont_filter=True, callback=self.parse)
        else:
            print "nextPageLink: "+nextPagelink
            nextSite = self.baseSite + nextPagelink
            yield scrapy.http.Request(url=nextSite, method="GET", headers=self.hdr, dont_filter=True, callback=self.parse)