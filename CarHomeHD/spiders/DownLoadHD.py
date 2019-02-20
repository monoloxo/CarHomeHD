# -*- coding: utf-8 -*-
import re

import scrapy
from CarHomeHD.items import CarhomehdItem


class DownloadhdSpider(scrapy.Spider):
    name = 'DownLoadHD'  # 爬虫名
    allowed_domains = ['car.autohome.com.cn']  # 限制爬取的网站
    start_urls = ['https://car.autohome.com.cn/jingxuan/list-0-p1.html']  # 开始爬取的链接

    def parse(self, response):
        # 套图链接的提取
        detail_urls = response.xpath("//ul[@class='content']/li/a/@href").getall()
        for url in detail_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_detail_urls)

        next_page = response.xpath("//div[@class='pageindex']/a[last()-1]/@href").get()
        if next_page:
            print("*" * 90)
            print(next_page)
            print("*" * 90)
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_detail_urls(self, response):
        # 处理详情页面
        list_pattern = response.xpath("//*[@id='cMode']/div/div[@class='side']/script").get()  # 提取列表模式的URL
        list_pattern = re.findall("/photolist/.*.html", list_pattern)[0]  # 匹配列表模式的url
        yield scrapy.Request(url=response.urljoin(list_pattern), callback=self.parse_image)  # 将Request对象交给下载函数

    def parse_image(self, response):
        # 下载图片
        category = response.xpath("//div[@class='mini_left']/a[last()-1]/text()").get()
        print(category)
        image_urls = response.xpath("//ul[@id='imgList']/li/a/img/@src").getall()
        image_urls = list(map(lambda x: x.replace("t_", ""), image_urls))  # 去除url中的"t_"得到高清大图
        image_urls = list(map(lambda x: response.urljoin(x), image_urls))
        yield CarhomehdItem(category=category, image_urls=image_urls)
        next_page = response.xpath("//div[@class='page']/a[last()-1]/@href").get()  # 匹配下一页链接
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_image)
