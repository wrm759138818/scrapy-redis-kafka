# -*- coding: utf-8 -*-
import scrapy
import itertools

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from pronhub.items import PronhubItem
import re


class PronhubSpider(scrapy.Spider):
    name = "pronhub"

    def start_requests(self):
        f = open("C:/Users/ruiming/PycharmProjects/pronhub/pronhub/spiders/seed.txt", encoding="utf-8")
        urls = []
        for temp in f.readlines():
            print(temp)
            if temp is None:
                continue
            start = temp.index("【") + 1
            end = temp.index("】")
            print(end)
            seed = temp[start:end]
            print(seed)
            urls.append('https://www.ciliwang.club/list.html?keyword=%s' % seed)
        print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.url)
        page = response.url[response.url.index('=') + 1:len(response.url)]

        # for single_cont in response.xpath('//div[@class=$val]', val='single_cont'):
        #     # 番号，种子，url，time,热度，大小
        #     a_path = single_cont.xpath("./ul[1]/h3/a")
        #     # print(a_path.get())
        #     design = a_path.xpath("./@title").get()
        #     seed = a_path.xpath("./@data-src").get()
        #     url = a_path.xpath("./@href").get()
        #     ul_path = single_cont.xpath("./ul[2]")
        #     time = ul_path.xpath("./li[1]/text()").get()
        #     size = ul_path.xpath("./li[2]/span/text()").get().replace("\n", "").replace("\r","").replace(" ", "")
        #     hot = ul_path.xpath("./li[3]/text()").get()
        #     pronhubItem = PronhubItem(design=design, seed=seed, url=url, time=time, size=size, hot=hot)
        #     pronhubItems.append(pronhubItem)

        def parseItemLoader(father_path):
            itemLoader = ItemLoader(PronhubItem(), father_path)
            # 番号，种子，url，time,热度，大小
            a_xpath = "./ul[1]/h3/a%s"
            # print(a_path.get())
            itemLoader.add_xpath("design", a_xpath % "/@title")
            itemLoader.add_xpath("seed", a_xpath % "/@data-src")
            itemLoader.add_xpath("url", a_xpath % "/@href")
            ul_xpath = "./ul[2]%s"
            itemLoader.add_xpath("time", ul_xpath % "/li[1]/text()")
            itemLoader.add_xpath("size", ul_xpath % "/li[2]/span/text()", re="[^0-9]*([0-9,\.]*[GB,MB,KB]+)")
            itemLoader.add_xpath("hot", ul_xpath % "/li[3]/text()")
            return itemLoader.load_item()

            # print(resItems)
        def check_extract_next_url(design):
             match = re.search('[a-z,A-Z]{3,5}-[0-9]{3}', design)
             if match:
                return match.group(0)
             else:
                pass

        for father_path in response.xpath('//div[@class=$val]', val='single_cont'):
            item = parseItemLoader(father_path)
            # 这里判断是否与request的种子相同，不相同则回调
            r = check_extract_next_url(item['design'][0])
            if not r :
                return
            yield scrapy.Request(url='https://www.ciliwang.club/list.html?keyword=%s' % r, callback=self.parse)
            yield item




