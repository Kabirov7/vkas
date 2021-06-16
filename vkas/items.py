# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VkasItem(scrapy.Item):
    # define the fields for your item here like:
    doc_num = scrapy.Field()
    receipt_date = scrapy.Field()
    info = scrapy.Field()
    judje = scrapy.Field()
    decision_date = scrapy.Field()
    decision = scrapy.Field()
    date_of_legal_force = scrapy.Field()
    judicial_acts = scrapy.Field()
    judicial_acts_url = scrapy.Field()