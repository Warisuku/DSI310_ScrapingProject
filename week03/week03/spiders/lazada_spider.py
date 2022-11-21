#scrapy crawl lazada -O lazada.csv

import scrapy
from scrapy_selenium import SeleniumRequest

class LazadaSpider(scrapy.Spider):
    name = "lazada"  

    def start_requests(self):
        start_urls = [
            'https://www.lazada.co.th/tag/steam-game/'
        ]

        for url in start_urls :
            yield SeleniumRequest(
                url=url, 
                callback=self.parse,
                )

    def parse(self, response):        
        for quote in response.css('img::attr(alt)').getall():
            yield {
                'text': quote,
                'url' : response.url,
            } 
            
        next_page = response.css('li.ant-pagination-item-active + li a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SeleniumRequest(url=next_page, callback=self.parse)
    