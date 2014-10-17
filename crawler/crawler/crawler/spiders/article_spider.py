from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler.parser import Parser

class ArticleSpider(CrawlSpider):
    name = 'article'
    allowed_domains = ['tuaw.com']
    start_urls = [
        "http://www.tuaw.com/2014/09/17/psa-ios-8-is-going-to-make-your-iphone-4s-a-good-bit-slower/?ncid=rss_truncated&cps=gravity"
    ]
    rules = (
        Rule(LinkExtractor(allow=(r'tuaw.com/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}', )), callback='crawlArticlePage', follow=True),
        Rule(LinkExtractor(allow=(r'\/editor\/', )), callback='crawlEditorPage', follow=True)
    )

    def __init__(self):
        CrawlSpider.__init__(self)
        self.selenium = webdriver.Firefox()
        self.parser = Parser(self.selenium)
        self.visitedUrls = []
        self.webpageLoadTimeoutInSeconds = 10

    def parse_start_url(self, response):
        return self.crawlArticlePage(response)

    def crawlPage(self, response):
        url = response.url
        self.visitedUrls.append(url)
        self.selenium.get(url)
        return WebDriverWait(self.selenium, self.webpageLoadTimeoutInSeconds)

    def crawlArticlePage(self, response):
        self.crawlPage(response).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fyre-widget")))
        article = self.parser.parseArticle(response.url)
        yield article

    def crawlEditorPage(self, response):
        self.crawlPage(response)

