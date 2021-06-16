import scrapy
from .. import const
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import json
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class PostsSpider(scrapy.Spider):
	name = 'vkas'
	# start_urls = ["https://vkas.sudrf.ru/"]
	start_urls = const.urls
	allowed_domains = ["vkas.sudrf.ru"]
	rules = {
		Rule(follow=True)
	}
	custom_settings = {
		'DEPTH_LIMIT': 0
	}

	def parse(self, response):
		print('currentURL: ', response.url)
		def clean_texts(xpath, css_select='::text'):
			array_of_texts = [x.css(css_select).extract_first() for x in response.xpath(xpath) if x]
			texts = []
			for x in array_of_texts:
				if x:
					texts.append(x.strip())
				else:
					texts.append(x)
			return texts

		response.meta['next_page'] = ''

		doc_num = clean_texts(const.DOC_NUM)
		receipt_date = clean_texts(const.RECEIPT_DATE)
		info = clean_texts(const.INFO)
		judje = clean_texts(const.JUDJE)
		decision_date = clean_texts(const.DECISION_DATE)
		decision = clean_texts(const.DECISION)
		date_of_legal_force = clean_texts(const.DATE_OF_LEGAL_FORCE)
		judicial_acts = clean_texts(const.JUDICIAL_ACTS)
		judicial_acts_hrefs = clean_texts(const.JUDICIAL_ACTS_HREFS, 'a ::attr(href)')

		# next_page_link = 'https://vkas.sudrf.ru/' + response.css(
		# 		"a[title='Следующая страница']::attr(href)").extract_first()[2:]

		cases = []
		for i, doc in enumerate(doc_num):
			url = "https://vkas.sudrf.ru" + judicial_acts_hrefs[i]
			case = {
				"doc_num": doc_num[i],
				"receipt_date": receipt_date[i],
				"info": info[i],
				"judje": judje[i],
				"decision_date": decision_date[i],
				"decision": decision[i],
				"date_of_legal_force": date_of_legal_force[i],
				"judicial_acts": judicial_acts[i],
				"judicial_acts_url": url
			}
			cases.append(case)
			# if len(cases) == 25:
			# 	yield scrapy.Request(
			# 		url=url,
			# 		callback=self.parse_act,
			# 		meta={"case": case, 'next_page': next_page_link}
			# 	)
			# else:
			yield scrapy.Request(
				url=url,
				callback=self.parse_act,
				meta={"case": case}
			)

		# print(len(cases))
		# if len(cases)+1  == 25:
		# 	yield scrapy.Request(
		# 		url=next_page_link,
		# 		callback=self.parse_main_page,
		# 	)
		# 	print(len(cases),"nextpage: ", next_page_link)

	def parse_act(self, response):
		act = [x.css("::text").extract_first().strip() for x in response.xpath("//div[@id='content']/span/p")]
		act = ' '.join(act)
		case = response.meta['case']
		case['judicial_acts'] = act
		yield case
		# meta_keys = response.meta.keys()
		# if 'next_page' in meta_keys:
		# 	if response.meta['next_page']:
		# 		print('next Page')
		# 		yield scrapy.Request(
		# 			url=response.meta['next_page'],
		# 			callback=self.parse_main_page,
		# 		)
