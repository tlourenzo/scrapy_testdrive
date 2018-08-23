"""
# title:full_author_detail.py .

# description: a webcrawler for retrieve quote author details
# author: Tome Lourenco
# date: 22 August 2018
# version: 1.0
# ==============================================================================
"""
# -*- coding: utf-8 -*-
import scrapy


class FullAuthorDetailSpider(scrapy.Spider):
    """Class Author detail Spider.

    Created to crawl a specific url in multiple
    Pages following detail links in each iteration.
    :param scrapy.Spider:
    :returns: dict with requested details, name and bday
    """

    name = 'full_author_detail'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        """Parse the response from the requested start_urls.

        A parser.
        :param response: from the requested start_urls
        :returns: a dict containing the keys as results from css keys
        """
        urls = response.css('div.quote > span > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        # follow pagination link to get next pages
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:  # Assuming that the next button link is available,
                            # make a new request and repeats the process.
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        """Parse the response from the requested start_urls.

        A parser for details.
        :param response: from the requested start_urls
        :returns: a dict containing the keys as results from css keys
        """
        yield {
            'name': response.css('h3.author-title::text').extract_first(),
            'bday': response.css('span.author-born-date::text').extract_first()
        }
