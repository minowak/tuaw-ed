import scrapy

class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    author = scrapy.Field()
    authorUrl = scrapy.Field()
    authorTwitter = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    htmlContent = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()
    comments = scrapy.Field()
    urlsInContent = scrapy.Field()

