# -*- coding: utf-8 -*-
import scrapy
import re
import codecs

class BaixingmainSpider(scrapy.Spider):
    name = "baixingMain"
    allowed_domains = ["baixing.com"]

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

    def start_requests(self):
        site = 'http://shanghai.baixing.com/'
        yield scrapy.http.Request(url=site, method="GET", headers=self.hdr, callback=self.parse)

    def parse(self, response):
        allA = response.xpath("//a[@target='_blank' and @class='one-category ' and @data-param]")
        final = set()
        for A in allA:
            href = A.xpath("@href").extract_first()
            if(re.match('/[a-z]+/*', href)):
                final.add(href)
        f=codecs.open("class.txt","w","utf-8")
        for href in final:
            f.write(href)
            f.write('\n')
        f.close()