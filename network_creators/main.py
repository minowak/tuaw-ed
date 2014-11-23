from network_creators.author_user_comments import AuthorUserComments
from network_creators.comments_portal_urls import CommentsPortalUrls
from network_creators.gefx.json_to_gexf import JSONToGexf

def create_gexf(nodes_edges_creator, output_filename):
    converter = JSONToGexf(nodes_edges_creator, 'articles.json', output_filename)
    converter.convert()

create_gexf(AuthorUserComments('Steven Sande'), 'author-user-comments.gexf')
create_gexf(CommentsPortalUrls(), 'comments-portal-urls.gexf')