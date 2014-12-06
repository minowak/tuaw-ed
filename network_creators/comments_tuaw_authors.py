import re
from network_creators.gefx.nodes_edges_creator import NodesEdgesCreator


class CommentsTuawAuthors(NodesEdgesCreator):

    def create(self, articles):
        def get_article_by_url(url):
            article = filter(lambda a: a['url'][:40] == url[:40], articles)
            if article is None or len(article) < 1:
                return None
            else:
                return article[0]
        articles = filter(lambda a: len(a['comments']) > 0, articles)
        authors = []
        for article in articles:
            for comment in article['comments']:
                user = comment['author']
                extracted_urls = self.__extract_urls_from_comment(comment)
                tuaw_urls = self.__extract_tuaw_urls(extracted_urls)
                for url in tuaw_urls:
                    art = get_article_by_url(url)
                    if art is None:
                        continue
                    author = art['author']
                    ats = filter(lambda a: a.author == author, authors)
                    if len(ats) > 0:
                        u = ats[0]
                    else :
                        u = Author(author)
                        authors.append(u)
                    u.add_user(user)
        nodes = self.__create_nodes(authors)
        return nodes, authors

    def __create_nodes(self, urls):
        nodes = []
        for url in urls:
            nodes.append(url)
            for user in url.edges:
                if user not in nodes:
                    nodes.append(user)
        return nodes

    def __extract_urls_from_comment(self, comment):
        html = comment['htmlContent']
        matches = re.findall(r'<a href="(.*?)" target="_blank" rel="nofollow">\1</a>', html)
        return matches

    def __links_tuaw(self, url):
        url = url.lower()
        matches = re.match(r'(.*tuaw\.com.*)', url)
        return matches is not None

    def __extract_tuaw_urls(self, urls):
        return filter(self.__links_tuaw, urls)


class Author:
    def __init__(self, author):
        self.author = author
        self.edges = {}

    def add_user(self, user):
        if user not in self.edges:
            self.edges[user] = 0
        self.edges[user] += 1

    def __str__(self):
        return self.author



