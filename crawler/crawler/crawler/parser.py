class Parser():
    def __init__(self, selenium):
        self.selenium = selenium

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

    def parseTags(self):
        return [x.get_attribute('text') for x in self.extract('div.collapse p a')]

    def parseSource(self):
        return self.extractOne("#source a").get_attribute('href')

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
            #TODO: comment responses ?
            parsedComments.append(parsedComment)
        return parsedComments

    def extract(self, cssSelector):
        return self.selenium.find_elements_by_css_selector(cssSelector)

    def extractOne(self, cssSelector):
        return self.extract(cssSelector)[0]

    def extractOneChild(self, element, cssSelector):
        return element.find_elements_by_css_selector(cssSelector)[0]
