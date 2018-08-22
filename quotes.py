# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):  # Name quotes.py
    """Class Quote Spider, created to crawl a specific url."""

    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        """Parse the response from the requested start_urls.

        A parser.
        param: response, from the requested start_urls
        returns a dict containing the keys as results from css keys
        """
        self.log("Visited: " + response.url)
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract(),
                'quote': quote.css('span.text::text').extract(),
                'tags': quote.css('a.tag::text').extract(),
            }
            yield item
        # follow pagination link to get next pages
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:  # Assuming that the next button link is available,
                            # make a new request and repeats the process.
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
