import re
from publicsuffix import PublicSuffixList
from network_creators.gefx.nodes_edges_creator import NodesEdgesCreator


class CommentsPortalUrls(NodesEdgesCreator):

    def __init__(self):
        self.psl = PublicSuffixList()

    def create(self, articles):
        articles = filter(lambda a: len(a['comments']) > 0, articles)
        domains = []
        for article in articles:
            for comment in article['comments']:
                user = comment['author']
                urls = self.__extract_urls_from_comment(comment)
                extracted_domains = self.__convert_urls_to_domains(urls)
                for domain in extracted_domains:
                    ds = filter(lambda d: d.url == domain, domains)
                    if len(ds) > 0:
                        d = ds[0]
                    else :
                        d = Domain(domain)
                        domains.append(d)
                    d.add_user(user)
        nodes = self.__create_nodes(domains)
        return nodes, domains

    def __create_nodes(self, domains):
        nodes = []
        for domain in domains:
            nodes.append(domain)
            for user in domain.edges:
                if user not in nodes:
                    nodes.append(user)
        return nodes

    def __extract_urls_from_comment(self, comment):
        html = comment['htmlContent']
        matches = re.findall(r'<a href="(.*?)" target="_blank" rel="nofollow">\1</a>', html)
        return matches

    def __extract_domain(self, url):
        url = url.lower()
        matches = re.search(r'(h|Ht|Tt|Tp|Ps|S)?:[/\\]{2}([wW]{3}\.)?([^:/\\]+)', url)
        match = matches.group(3)
        domain = self.psl.get_public_suffix(match)
        return domain

    def __convert_urls_to_domains(self, urls):
        return map(lambda u: self.__extract_domain(u), urls)


class Domain:
    def __init__(self, url):
        self.url = url
        self.edges = {}

    def add_user(self, user):
        if user not in self.edges:
            self.edges[user] = 0
        self.edges[user] += 1

    def __str__(self):
        return self.url



