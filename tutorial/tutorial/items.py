# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CategoryItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    description = scrapy.Field()


class FreshmartItem(scrapy.Item):
    name = scrapy.Field()
    # description = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    quantity_postfix = scrapy.Field()
    status = scrapy.Field()
    order_info_raw = scrapy.Field()
    order_info = scrapy.Field()
    active = scrapy.Field()

    slug = scrapy.Field()
    product_id = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()

    # _big.jpeg _obj.jpeg _cat.jpeg
    features = scrapy.Field()
    goods_similar = scrapy.Field()