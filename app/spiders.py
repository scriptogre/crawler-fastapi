from typing import Any

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field
import scrapy.utils.log


class PageDetails(Item):
    """A Scrapy Item to store information about each page."""
    url = Field()
    is_suspicious = Field()


class KeywordSearchSpider(scrapy.Spider):
    """
    A Scrapy Spider to crawl webpages and check for suspicious words.
    """
    name = "keywordsearchspider"

    custom_settings = {
        "ITEM_PIPELINES": {"__main__.PageAnalysisPipeline": 1},
    }

    def __init__(self, start_urls: list[str], keywords: list[str], *args, **kwargs):
        super(KeywordSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.suspicious_words = keywords

    def parse(self, response: scrapy.http.Response) -> Any:
        is_suspicious = any(word in response.text for word in self.suspicious_words)
        webpage = PageDetails()
        webpage["url"] = response.url
        webpage["is_suspicious"] = is_suspicious
        yield webpage

        extractor = LinkExtractor()
        links = extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse)
