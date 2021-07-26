# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapingwebItem(scrapy.Item):
    img_url = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
# ScrapingList Residential & Yield Estate for sale
class ListResidentialItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()