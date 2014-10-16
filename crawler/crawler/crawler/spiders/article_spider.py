import re
from crawler.items import *
from scrapy.http import Request
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
        article = self.parseArticle(response.url)
        yield article
        #self.crawlAuthorUrl(article)
        #self.continueCrawlingArticles(article['urlsInContent'])

    def crawlEditorPage(self, response):
        self.crawlPage(response)#.until(EC.presence_of_element_located((By.ID, "micro-posts")))
        urls = self.parser.parseUrlsInEditorPage()
        #self.continueCrawlingArticles(urls)

    def crawlAuthorUrl(self, article):
        authorUrl = article['authorUrl']
        if authorUrl not in self.visitedUrls:
            yield Request(authorUrl, callback = self.crawlEditorPage)

    def continueCrawlingArticles(self, urls):
        for url in urls:
            if re.match("tuaw.com/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}", url) and url not in self.visitedUrls:
                yield Request(url, callback = self.crawlArticlePage)

    def parseArticle(self, url):
        article = ArticleItem()
        article['url'] = url
        article['title'] = self.parser.parseTitle()
        article['author'] = self.parser.parseAuthor()
        article['authorUrl'] = self.parser.parseAuthorUrl()
        article['authorTwitter'] = self.parser.parseAuthorTwitter()
        article['timestamp'] = self.parser.parseTimestamp()
        article['content'] = self.parser.parseContent()
        article['tags'] = self.parser.parseTags()
        article['source'] = self.parser.parseSource()
        article['urlsInContent'] = self.parser.parseUrlsInAuthorPage()
        article['comments'] = self.parser.parseComments()
        return article



