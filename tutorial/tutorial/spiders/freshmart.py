# -*- coding: utf-8 -*-
from os.path import basename
from urllib.parse import urlsplit

from scrapy.spiders import SitemapSpider

from tutorial.items import FreshmartItem


class FreshmartSpider(SitemapSpider):
    name = 'freshmart'
    allowed_domains = ['freshmart.com.ua']
    sitemap_urls = ['https://freshmart.com.ua/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
        ('/catalog/', 'parse_category'),
    ]

    def parse_product(self, response):
        item = FreshmartItem()
        item['name'] = response.css("head > meta[property='og:title']::attr(content)").extract_first()
        item['content'] = response.css("head > meta[property='og:description']::attr(content)").extract_first()

        item['category'] = response.css(
            "div.breadcrumbs ol li.breadcrumbs__item:nth-child(2) > a > span::text").extract_first()
        item['subcategory'] = response.css(
            "div.breadcrumbs ol li.breadcrumbs__item:nth-child(3) > a > span::text").extract_first()

        item['price'] = response.css(".product__order-item-number::text").extract_first()
        item['price_old'] = response.css(".product__order-item-old::text").extract_first()
        item['quantity_postfix'] = response.css(".quantity-postfix::text").extract_first()
        item['status'] = response.css(
            "#slider_recipe > li:nth-child(1) > div.status > div::attr(class)").extract_first()
        item['order_info_raw'] = response.css(".product__data .product__order-info").extract_first()
        if item['price'] is None:
            item['active'] = False
        else:
            item['active'] = True

        url = response.css("head > meta[property='og:url']::attr(content)").extract_first()
        filename = basename(urlsplit(url).path)[:-5]
        filename_splitted = filename.split('-')
        item['slug'] = '-'.join(filename_splitted[:-1])
        item['product_id'] = filename_splitted[-1]

        item['image_urls'] = response.css("#tab_photo_ul > li > a > img::attr(src)").extract()
        # # _big.jpeg _obj.jpeg _cat.jpeg

        features_names = response.css(
            ".product__feature > .product__feature-field > .product__feature-name::text").extract()
        features_values = response.css(
            ".product__feature > .product__feature-field > .product__feature-value::text").extract()
        item['features'] = dict(zip(list(map(lambda x: x[:-1], features_names)), features_values))

        goods_similar = response.css("#goods_similar a.catalog__picture::attr(href)").extract()

        item['goods_similar'] = list(map(lambda similar_url: basename(urlsplit(similar_url).path)[:-5], goods_similar))

        self.logger.info('!!! Parsed {}'.format(item['name']))
        return item

    def parse_category(self, response):
        # TODO: Need create parse category
        self.logger.info('Hi, this is a cat node!')
