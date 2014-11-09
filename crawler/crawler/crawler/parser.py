from items import ArticleItem

class Parser():
    def __init__(self, selenium):
        self.selenium = selenium

    def containsComments(self):
        return self.extractOne('#lf_comment_stream') is not None

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
        element = self.extractOne("h1.posttitle")
        if element is not None: return element.text
        else: return ''

    def parseAuthor(self):
        element = self.extractOne("span.author a")
        if element is not None: return element.text
        else: return ''

    def parseAuthorUrl(self):
        element = self.extractOne("span.author a")
        if element is not None: return element.get_attribute('href')
        else: return ''

    def parseAuthorTwitter(self):
        element = self.extractOne("span.tweet a")
        if element is not None: return element.get_attribute('href')
        else: return ''

    def parseTimestamp(self):
        element = self.extractOne("span.timestamp")
        if element is not None: return element.text
        else: return ''

    def parseContent(self):
        content = [x.text for x in self.extract("div.article div.body *")]
        contentWithoutEmptyLines = filter(lambda text: "\n" not in text, content)
        joinedContent = " ".join(contentWithoutEmptyLines)
        return joinedContent

    def parseHtmlContent(self):
        element = self.extractOne("div.article div.body")
        if element is not None: return element.get_attribute('innerHTML')
        else: return ''

    def parseTags(self):
        elements = self.extract('div.collapse p a')
        if elements is not None:
            return [x.get_attribute('text') for x in elements]
        else: return ''

    def parseSource(self):
        element = self.extractOne("#source a")
        if element is not None: return element.get_attribute('href')
        else: return ''

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