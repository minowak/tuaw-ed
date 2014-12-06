import re
from network_creators.gefx.nodes_edges_creator import NodesEdgesCreator


class CommentsTuawUrls(NodesEdgesCreator):

    def create(self, articles):
        articles = filter(lambda a: len(a['comments']) > 0, articles)
        urls = []
        for article in articles:
            for comment in article['comments']:
                user = comment['author']
                extracted_urls = self.__extract_urls_from_comment(comment)
                tuaw_urls = self.__extract_tuaw_urls(extracted_urls)
                for url in tuaw_urls:
                    us = filter(lambda d: d.url == url, urls)
                    if len(us) > 0:
                        u = us[0]
                    else :
                        u = Url(url)
                        urls.append(u)
                    u.add_user(user)
        nodes = self.__create_nodes(urls)
        return nodes, urls

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


class Url:
    def __init__(self, url):
        self.url = url
        self.edges = {}

    def add_user(self, user):
        if user not in self.edges:
            self.edges[user] = 0
        self.edges[user] += 1

    def __str__(self):
        return self.url



