# -*- coding: utf-8 -*-
from os.path import basename
from urllib.parse import urlsplit

import scrapy
from scrapy.spiders import SitemapSpider
from tutorial.tutorial.items import FreshmartItem


# class FreshmartSpider(scrapy.Spider):
#     name = 'freshmart'
#     allowed_domains = ['freshmart.com.ua']
#     start_urls = ['https://freshmart.com.ua/sitemap.xml']
#     namespaces = {
#         'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
#     }
#     itertag = 'loc'
#
#     def parse_node(self, response, node):
#         self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))
#
#         item = FreshmartItem()
#         # item['id'] = node.xpath('@id').extract()
#         # item['name'] = node.xpath('name').extract()
#         # item['description'] = node.xpath('description').extract()
#         item['path'] = node.xpath('description').extract()
#         return item


class FreshmartSpider(SitemapSpider):
    name = 'freshmart'
    allowed_domains = ['freshmart.com.ua']
    sitemap_urls = ['https://freshmart.com.ua/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
        ('/catalog/', 'parse_category'),
    ]

    # def parse(self, response):
    #     items = []
    #     for sel in response.xpath('//loc'):
    #         item = FreshmartItem()
    #         item['link'] = sel.xpath('@href').extract()
    #         items.append(item)
    #     return items

    # def start_requests(self):
    #     for url in self.sitemap_urls:
    #         if url.startswith('http://'):
    #             url = 'https.{}'.format(url[4:])
    #         yield Request(url, self._parse_sitemap)

    def parse_product(self, response):
        item = FreshmartItem()
        item['name'] = response.css("head > meta[property='og:title']::attr(content)").extract_first()
        item['description'] = response.css("head > meta[property='og:description']::attr(content)").extract_first()

        item['category'] = response.css(
            "div.breadcrumbs ol li.breadcrumbs__item:nth-child(2) > a > span::text").extract_first()
        item['subcategory'] = response.css(
            "div.breadcrumbs ol li.breadcrumbs__item:nth-child(3) > a > span::text").extract_first()

        item['price'] = response.css(".product__order-item-number::text").extract_first()
        item['price_old'] = response.css(".product__order-item-old::text").extract_first()
        item['quantity_postfix'] = response.css(".quantity-postfix::text").extract_first()
        item['status'] = response.css(
            "#slider_recipe > li:nth-child(1) > div.status > div::attr(class)").extract_first()
        # item.order_info = scrapy.Field()
        item['order_info'] = response.css(".product__data .product__order-info").extract_first()
        # item.order_mess = scrapy.Field()
        if item['price'] is None:
            item['active'] = False
        else:
            item['active'] = True

        url = response.css("head > meta[property='og:url']::attr(content)").extract_first()
        filename = basename(urlsplit(url).path)[:-5]
        item['slug'] = filename.split('-')[0]
        item['product_id'] = filename.split('-')[1]
        item['content'] = response.css("#product_description > .textbox__content").extract_first()

        item['image'] = response.css("head > meta[property='og:image']::attr(content)").extract_first()
        #
        item['images'] = response.css("#tab_photo_ul > li > a > img::attr(src)").extract()
        # # _big.jpeg _obj.jpeg _cat.jpeg
        item['features'] = dict(zip(
            list(map(lambda x: x[:-1],
                     response.css(
                         ".product__feature > .product__feature-field > .product__feature-name::text").extract()
                     )),
            response.css(".product__feature > .product__feature-field > .product__feature-value::text").extract()
        ))
        item['goods_similar'] = response.css("#goods_similar a.catalog__picture::attr(href)").extract()

        self.logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {}'.format(item['name']))
        return item

    def parse_category(self, response):
        self.logger.info('Hi, this is a cat node!')
