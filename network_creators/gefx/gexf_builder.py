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
                index = nodes.index(source_node)
                source_node_id = str(index)
                weight = str(destination_node.edges[source_node])
                edge_xml = u'<edge id="{}" source="{}" target="{}" weight="{}" />'.format(edge_id, source_node_id, destination_node_id, weight)
                xml_edges += edge_xml
                edge_id += 1
        xml_edges += u'</edges>'
        self.append(xml_edges)