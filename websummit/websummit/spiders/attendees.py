# -*- coding: utf-8 -*-
import scrapy
import json
from time import sleep

class AttendeesSpider(scrapy.Spider):
    """Class AttendeesSpider

    Created to crawl a websummit API in multiple pages mode.
    :param scrapy.Spider:
    :returns: dict with requested details
    """

    name = 'websummit_at'
    allowed_domains = ['websummit.com']
    api_url = 'https://api.cilabs.com/conferences/ws17/lists/featured_attendees?interleave=true&&page={}'
    page = 1
    start_urls = [api_url.format(page)]

    def parse(self, response):
        """Parse the response from the requested start_urls.

        A parser.
        :param response: from the requested start_urls
        :returns: a dict containing the keys as results from json api.
        """
        if response.status != 404:
            data = json.loads(response.text)
            for attendee in data['data']:
                yield {
                    'first_name': attendee['first_name'],
                    'last_name': attendee['last_name'],
                    'company': attendee['company_name'],
                    'job_title': attendee['job_title'],
                    'avatar': attendee['avatar_urls']['large'],
                    'bio': attendee['bio'],
                    'country': attendee['country']
                    }

            self.page += 1
            url = self.api_url.format(self.page)
            sleep(10)
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            print('ERROR!!!!! 404')
