"""
# title:scrap_infite_scroll.py .

# description: a webcrawler for retrieve quotes in an infinite scroll page
# author: Tome Lourenco
# date: 26 August 2018
# version: 1.0
# ==============================================================================
"""
# -*- coding: utf-8 -*-
import scrapy
import json


class ScrapInfiniteScrollSpider(scrapy.Spider):
    name = 'scrap_infinite_scroll'
    allowed_domains = ['toscrape.com']
    api_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api_url.format(1)]

    def parse(self, response):
        data = json.loads(response.text)
        for quote in data['quotes']:
            yield {
                'author_name': quote['author']['name'],
                'text': quote['text'],
                'tags': quote['tags']
            }
        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(url=self.api_url.format(next_page),
                                 callback=self.parse)
