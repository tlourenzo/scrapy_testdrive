"""
# title:quotesjs.py .

# description: a webcrawler for retrieve quotes
    and its details from a js website
# author: Tome Lourenco
# date: 26 August 2018
# version: 1.0
# ==============================================================================
"""
# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuotesjsSpider(scrapy.Spider):
    """Class QuotesFromJsPage, created to crawl a specific js url."""

    name = 'quotesjs'
    url = 'http://quotes.toscrape.com/js'

    def start_requests(self):
        """Parse the response from the requested start_urls.

        Initializer.
        :returns: the parsing information after a splash request response
        """
        yield SplashRequest(
            url=self.url,
            callback=self.parse
        )

    def parse(self, response):
        """Parse the response from the requested start_urls.

        A parser.
        :param response: from the requested start_urls
        :returns: a dict containing the keys as results from css keys
        """
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('small.author::text').extract_first(),
                'quote': quote.css('span.text::text').extract_first(),
                'tags': quote.css('div.tags > a.tag::text').extract()
            }
