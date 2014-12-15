import re
from network_creators.gefx.nodes_edges_creator import NodesEdgesCreator


class ArticleUserComments(NodesEdgesCreator):

    def create(self, articles):
        def get_user(users, user_name):
            users_with_the_same_name = filter(lambda u: u.name == user_name, users)
            if len(users_with_the_same_name) > 0:
                return users_with_the_same_name[0]
            else:
                return None

        articles = filter(lambda a: len(a['comments']) > 0, articles)
        users = []
        x = 1
        num_of_articles = len(articles)
        for article in articles:
            x += 1
            print str(x) + ' / ' + str(num_of_articles)
            article_url = article['url']
            for comment in article['comments']:
                user_name = comment['author']
                user = get_user(users, user_name)
                if user is None:
                    user = User(user_name)
                    users.append(user)
                user.add_article(article_url)
        nodes = self.__create_nodes(users)
        return nodes, users

    def __create_nodes(self, users):
        nodes = []
        x = 1
        num_of_users = len(users)
        for user in users:
            x += 1
            print str(x) + ' / ' + str(num_of_users)
            nodes.append(user)

            num_of_edges = len(user.edges)
            y = 0
            for article_url in user.edges:
                y += 1
                print str(y) + ' / ' + str(num_of_edges)
                if article_url not in nodes:
                    nodes.append(article_url)
        return nodes

class User:
    def __init__(self, name):
        self.name = name
        self.edges = {}

    def add_article(self, article_url):
        if article_url not in self.edges:
            self.edges[article_url] = 0
        self.edges[article_url] += 1

    def __str__(self):
        return self.name



