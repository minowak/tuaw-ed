import codecs
import json

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

class GexfBuilder:
    def __init__(self):
        self.xml = ''

    def append(self, xml):
        self.xml += xml

    def start(self):
        self.xml = ''
        self.append(xml = u'<?xml version="1.0" encoding="UTF-8"?><gexf xmlns="http://www.gexf.net/1.2draft" version="1.2"><meta lastmodifieddate="2009-03-20"><creator>Gexf.net</creator><description>Network</description></meta><graph mode="static" defaultedgetype="directed">')

    def finish(self):
        self.append(u'</graph></gexf>')

    def append_nodes(self, nodes):
        xml_nodes = '<nodes>'
        node_id = 0
        for node in nodes:
            xml_node = u'<node id="{}" label="{}" />'.format(str(node_id), node)
            xml_nodes += xml_node
            node_id += 1
        xml_nodes += u'</nodes>'
        self.append(xml_nodes)

    def append_edges(self, nodes, destinations):
        xml_edges = u'<edges>'
        edge_id = 0
        for destination_node in destinations:
            destination_node_id = str(nodes.index(destination_node))
            for source_node in destination_node.edges:
                source_node_id = str(nodes.index(source_node))
                weight = str(destination_node.edges[source_node])
                edge_xml = u'<edge id="{}" source="{}" target="{}" weight="{}" />'.format(edge_id, source_node_id, destination_node_id, weight)
                xml_edges += edge_xml
                edge_id += 1
        xml_edges += u'</edges>'
        self.append(xml_edges)

class JSONToGexf:

    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.articles = []
        self.gexf_builder = GexfBuilder()
        self.__read_articles()

    def select_author(self, author):
        self.articles = filter(lambda a: a['author'] == author, self.articles)

    def convert(self):
        authors = []
        all_users = []
        for article in self.articles:
            author = Author(article['author'])
            users = self.__get_users_from_comments(article['comments'])
            if author not in authors:
                authors.append(author)
            for user in users:
                author.add_commentator(user)
                if user not in all_users:
                    all_users.append(user)
        nodes = self.__create_nodes(authors, all_users)
        self.gexf_builder.start()
        self.gexf_builder.append_nodes(nodes)
        self.gexf_builder.append_edges(nodes, authors)
        self.gexf_builder.finish()
        self.__write_xml()

    def __read_articles(self,):
        articles_file = open(self.input_filename, 'r')
        self.articles = json.load(articles_file)
        articles_file.close()

    def __write_xml(self):
        xml_file = codecs.open(self.output_filename, 'w', 'utf-8')
        xml_file.write(self.gexf_builder.xml)
        xml_file.close()

    def __get_users_from_comments(self, comments):
        users = []
        for comment in comments:
            user = comment['author']
            if user not in users:
                users.append(user)
        return users

    def __create_nodes(self, authors, all_users):
        nodes = []
        for author in authors:
            nodes.append(author)
        for user in all_users:
            nodes.append(user)
        return nodes

converter = JSONToGexf('articles.json', 'author-user-comments.gexf')
converter.select_author('Steven Sande')
converter.convert()