#-*- coding: utf-8 -*-
# 모듈명 : 뉴스사이트 웹 크롤링 bbc
# 작성자 : dongsu, kang
# 작성일 : 2015.08.29

import scrapy
from scrapy.spider import BaseSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
import datetime
import time

import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

class KodbItem(scrapy.Item):
	news_link_url = scrapy.Field()
	news_title = scrapy.Field()
	news_content = scrapy.Field()
	news_topic = scrapy.Field()
	news_date = scrapy.Field()
	continent = scrapy.Field()	
	media_company = scrapy.Field()		
	
class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["bbc.com"]
    start_urls = (
        'http://www.bbc.com/news/',
    )
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22 AlexaToolbar/alxg-3.1"
    #DOWNLOAD_DELAY = 2 #크롤링 다운로드 속조 조절입니다.
    rules = (Rule(LxmlLinkExtractor(allow=()), callback='parse', follow=True),)
    
    def parse(self, response):

        links = []
        for link in LxmlLinkExtractor(allow=(".com/news")).extract_links(response):			
            #print link.url
	    links.append(link.url)

	#페이지안의 news 폴더 링크들을 모두 크롤링하게 설정	
	rg = range(len(links)) 
	for i in rg:
		yield Request(links[i], callback=self.parse_loop)

    def parse_loop(self, response):

	#HTML데이터가져오기
	hxs = HtmlXPathSelector(response)
	
	news_date = hxs.xpath("//li[@class='mini-info-list__item'][1]/div[@class='date date--v2']/text()").extract()
	news_topic = hxs.xpath("//li[@class='mini-info-list__item'][2]/a[@class='mini-info-list__section']/text()").extract()
	media_company = "bbc"
	continent = ""
	news_link_url = response.url
	news_title = hxs.xpath("//div[@class='story-body']/h1[@class='story-body__h1']/text()").extract()
	news_content = hxs.xpath("//div[@class='story-body__inner']/p/text()").extract()
	ncontent = ""
	
	#특정페이지에서는 똑같은 데이터가 여러개 있을수있어서 첫 1건만가져온다.
	for data in news_date:
		news_date = data
		break
		
	for data in news_topic:
		news_topic = data
		break
		
	for data in news_title:
		news_title = data
		break
		
	for p in news_content:
		ncontent = ncontent + p
		
	news_content = ncontent
	
	if(len(news_title) > 0):
		item = KodbItem()
		item["news_date"] = news_date
		item["news_topic"] = news_topic
		item["media_company"] = media_company
		item["continent"] = continent
		item["news_link_url"] = news_link_url
		item["news_title"] = news_title
		item["news_content"] = news_content
		yield item
	
        links = []
        for link in LxmlLinkExtractor(allow=(".com/news")).extract_links(response):			
            #print link.url
	    links.append(link.url)

	#if(len(links) > 5):	
	#	rg = range(5) #페이지 안의 링크들을 몇개 가져올건지 설정
	#else:
	rg = range(len(links)) #설정된값보다 링크가 적을 경우 링크 총 수로 설정
	
	for i in rg:
		yield Request(links[i], callback=self.parse_loop)

		