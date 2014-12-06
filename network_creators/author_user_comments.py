from network_creators.gefx.nodes_edges_creator import NodesEdgesCreator


class AuthorUserComments(NodesEdgesCreator):

    def __init__(self, author):
        self.author = author

    def create(self, articles):
        #articles = filter(lambda a: a['author'] == self.author, articles)
        authors = []
        all_users = []
        for article in articles:
            authorName = article['author']
            author = self.__find_or_create_author(authors, authorName)
            users = self.__get_users_from_comments(article['comments'])
            for user in users:
                author.add_commentator(user)
                if user not in all_users:
                    all_users.append(user)
        nodes = self.__build_nodes(authors, all_users)
        return nodes, authors

    def __find_or_create_author(self, authors, authorName):
        found = filter(lambda a: a.name == authorName, authors)
        if len(found) > 0:
            author =  found[0]
        else:
            author = Author(authorName)
            authors.append(author)
        return author

    def __get_users_from_comments(self, comments):
        users = []
        for comment in comments:
            user = comment['author']
            if user not in users:
                users.append(user)
        return users

    def __build_nodes(self, authors, all_users):
        nodes = []
        for author in authors:
            nodes.append(author)
        for user in all_users:
            nodes.append(user)
        return nodes


class Author:
    def __init__(self, name):
        self.name = name
        self.edges = {}

    def add_commentator(self, user):
        self.__assure_user_in_dict(user)
        self.edges[user] += 1

    def __assure_user_in_dict(self, user):
        if user not in self.edges:
            self.edges[user] = 0

    def __str__(self):
        return self.name
