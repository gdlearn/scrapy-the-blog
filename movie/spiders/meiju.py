# -*- coding: utf-8 -*-
import scrapy
import re
import os
import urllib
import MySQLdb
import sys
import html5lib
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request
from movie.items import MovieItem
 
class MeijuSpider(scrapy.Spider):
    name = "meiju" 
    allowed_domains = ["dawnfly.cn"]
    # start_urls = ['http://www.dawnfly.cn/article-0-25.html','http://www.dawnfly.cn/article-0-25-2.html']
    start_urls=['http://www.dawnfly.cn/']
    cat_urls=""
    def parse(self, response):
        # if(re.match("http://www.dawnfly.cn/article-0-\d+|\d+-\d+.html",response.url)):
            movies = response.xpath('//nav[@class="main-nav"]/div/ul/li')
            print response.url
            for each_movie in movies:
                item = MovieItem()
                item['cat_url']=each_movie.xpath('./a/@href').extract()[0]
                if(item['cat_url'].startswith("/article-")):
                    # 栏目分类url
                    # print item['cat_url']
                # if(re.match("/article-",item['cat_url']):
                    # yield item
                    yield Request("http://www.dawnfly.cn"+item['cat_url'],callback=self.parse_cat,meta={'cat_url':item})
            # all_urls=response.xpath("//nav/a/@href").extract()#提取界面所有的url
            # # # print all_urls    
            # for url in all_urls:
            #     # print url
            #     # print 123
            #     # if(re.match("http://www.dawnfly.cn/article-0-\d+|\d+-\d+.html",url)):
            #     if(url.startswith("/article-0-25")):
            #         print url
            #         yield Request("http://www.dawnfly.cn"+url,callback=self.parse)
        # all_urls=response.xpath("//a/@href").extract()#提取界面所有的url
	    	# print 123
	    # for url in all_urls:
	    # 	print url
	        	# if(url.startswith("/ye/")):
	        		# print "http://m.yse123.com"+url
                 	# yield Request("http://m.yse123.com"+url,callback=self.parse)
    def parse_cat(self,response):
        # print response.url
        # print response.meta['cat_url']
        print response.url
        all_url=response.xpath('//div[@class="primary-site"]/article/section/header/h2')
        for title in all_url:
            titles= title.xpath('./a/@title').extract()[0]
            item = MovieItem()
            item['detail_url']=title.xpath('./a/@href').extract()[0]
            item['title']=titles
            # item['cat_url']=response.meta.cat_url
            print titles
            
            yield Request("http://www.dawnfly.cn"+item['detail_url'],callback=self.parse_detail,meta={'detail_url':item})
            # print item['detail_url']
            # 翻页
            next_page = response.xpath('//nav[@id="pagenavi"]/a/@href')
            if next_page:
                url = response.urljoin(next_page[0].extract())
                #爬每一页
                # print url
                yield scrapy.Request(url,callback=self.parse_cat)
                # yield Request("http://www.dawnfly.cn"+item['detail_url'],callback=self.parse_detail,meta={'detail_url':item})
    def parse_detail(self,response):
        # print response.meta['detail_url']
        # view
        all_url=response.xpath('//div[@class="single-meta"]')
        # content
        content_html=response.xpath('//div[@class="content-main"]')
       
        for total in all_url:
            # /p[8]
            item = MovieItem()
            item =response.meta['detail_url']
            # item['cat_url']= response.meta.cat_url
            # item['title']= response.meta.title
            # item['detail_url']= response.meta.detail_url
            totals= total.xpath('./span[@class="views"]/text()').extract()[0]
            # soup= BeautifulSoup(content_html, 'html5lib')
            # item['content']=str(soup.find_all('div',class_="content-main"))
            item['views']=totals
            yield item
            # print totals