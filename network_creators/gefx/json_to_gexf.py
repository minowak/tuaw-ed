import codecs
import json
from xml.dom import minidom
from network_creators.gefx.gexf_builder import GexfBuilder

class JSONToGexf:

    def __init__(self, nodes_edges_creator, input_filename, output_filename):
        self.nodes_edges_creator = nodes_edges_creator
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.articles = []

    def convert(self):
        self.__read_articles()
        nodes, edges = self.nodes_edges_creator.create(self.articles)
        self.__save(nodes, edges)

    def __save(self, nodes, edges):
        gexf_builder = GexfBuilder()
        gexf_builder.start()
        gexf_builder.append_nodes(nodes)
        gexf_builder.append_edges(nodes, edges)
        gexf_builder.finish()
        self.__write_xml(gexf_builder.xml)

    def __read_articles(self,):
        articles_file = open(self.input_filename, 'r')
        self.articles = json.load(articles_file)
        articles_file.close()

    def __write_xml(self, xml):
        pretty_xml = minidom.parseString(xml.encode('utf-8')).toprettyxml()
        xml_file = codecs.open(self.output_filename, 'w', 'utf-8')
        xml_file.write(pretty_xml)
        xml_file.close()
