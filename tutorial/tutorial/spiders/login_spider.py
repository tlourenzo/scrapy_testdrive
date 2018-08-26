"""
# title:login_spider.py .

# description: a webcrawler for retrieve quotes in a page visible after login
# author: Tome Lourenco
# date: 26 August 2018
# version: 1.0
# ==============================================================================
"""
# -*- coding: utf-8 -*-
import scrapy


class LoginSpiderSpider(scrapy.Spider):
    """Class LoginSpiderSpider.

    Created to crawl a specific url with a login method.
    :param scrapy.Spider:
    :returns: dict with requested details, name and author url
    """

    name = 'login_spider'
    allowed_domains = ['toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        """Parse the response from the requested start_urls.

        A parser.
        :param response: from the requested start_urls
        :returns: a dict containing the the form values needed to login.
        """
        # extract the csrf token value
        token = response.css('input[name="csrf_token"]::attr(value)'
                             ).extract_first()
        # create a dict with the form names
        data_to_send = {
            'csrf_token': token,
            'username': 'abc',
            'password': 'abc'
        }
        # submit a POST request to it
        yield scrapy.FormRequest(url=self.login_url, formdata=data_to_send,
                                 callback=self.parse_quotes)

    def parse_quotes(self, response):
        """Parse the response from the requested start_urls after login.

        A parser.
        :param response: from the requested start_urls
        :returns: a dict containing the data from each quote.
        """
        for quote in response.css('div.quote'):
            yield {
                'author_name': quote.css('small.author::text').extract_first(),
                'author_hidden_url': quote.css(
                    'small.author ~ a[href*="goodreads.com"]::attr(href)'
                    ).extract_first()
            }
