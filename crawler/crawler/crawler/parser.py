from items import ArticleItem

class Parser():
    def __init__(self, selenium):
        self.selenium = selenium

    def parseArticle(self, url):
        article = ArticleItem()
        article['url'] = url
        article['title'] = self.parseTitle()
        article['author'] = self.parseAuthor()
        article['authorUrl'] = self.parseAuthorUrl()
        article['authorTwitter'] = self.parseAuthorTwitter()
        article['timestamp'] = self.parseTimestamp()
        article['content'] = self.parseContent()
        article['htmlContent'] = self.parseHtmlContent()
        article['tags'] = self.parseTags()
        article['source'] = self.parseSource()
        article['urlsInContent'] = self.parseUrlsInAuthorPage()
        article['comments'] = self.parseComments()
        return article

    def parseTitle(self):
        return self.extractOne("h1.posttitle").text

    def parseAuthor(self):
        return self.extractOne("span.author a").text

    def parseAuthorUrl(self):
        return self.extractOne("span.author a").get_attribute('href')

    def parseAuthorTwitter(self):
        return self.extractOne("span.tweet a").get_attribute('href')

    def parseTimestamp(self):
        return self.extractOne("span.timestamp").text

    def parseContent(self):
        content = [x.text for x in self.extract("div.article div.body *")]
        contentWithoutEmptyLines = filter(lambda text: "\n" not in text, content)
        joinedContent = " ".join(contentWithoutEmptyLines)
        return joinedContent

    def parseHtmlContent(self):
        return self.extractOne("div.article div.body").get_attribute('innerHTML')

    def parseTags(self):
        return [x.get_attribute('text') for x in self.extract('div.collapse p a')]

    def parseSource(self):
        source = self.extractOne("#source a")
        if source is not None:
            return source.get_attribute('href')
        else:
            return ''

    def parseUrlsInAuthorPage(self):
        return [x.get_attribute('href') for x in self.extract("div.article div.body a")]

    def parseUrlsInEditorPage(self):
        return [x.get_attribute('href') for x in self.extract("div.micro-posts div.body a")]

    def parseComments(self):
        parsedComments = []
        comments = self.extract(".fyre-comment-wrapper")
        for comment in comments:
            parsedComment = {}
            parsedComment['author'] = self.extractOneChild(comment, "[itemprop='author']").text
            parsedComment['timestamp'] = self.extractOneChild(comment, "[itemprop='dateCreated']").get_attribute('content')
            parsedComment['content'] = self.extractOneChild(comment, "[itemprop='text'] p").text
            parsedComment['htmlContent'] = comment.get_attribute('innerHTML')
            parsedComments.append(parsedComment)
        return parsedComments

    def extract(self, cssSelector):
        return self.selenium.find_elements_by_css_selector(cssSelector)

    def extractOne(self, cssSelector):
        elements = self.extract(cssSelector)
        if len(elements) > 0:
            return elements[0]
        else:
            return None

    def extractOneChild(self, element, cssSelector):
        elements = element.find_elements_by_css_selector(cssSelector)
        if len(elements) > 0:
            return elements[0]
        else:
            return None