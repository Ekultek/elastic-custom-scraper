import scrapy


class BgpviewSpider(scrapy.Spider):
    name = 'bgpview'
    allowed_domains = ['bgpview.io']
    start_urls = ['https://bgpview.io/']

    def parse(self, response):
        pass
