from network_creators.article_user_comments import ArticleUserComments
from network_creators.author_user_comments import AuthorUserComments
from network_creators.comments_portal_urls import CommentsPortalUrls
#from network_creators.comments_tuawl_urls import CommentsTuawUrls
from network_creators.comments_tuaw_authors import CommentsTuawAuthors
from network_creators.gefx.json_to_gexf import JSONToGexf

def create_gexf(nodes_edges_creator, output_filename):
    converter = JSONToGexf(nodes_edges_creator, 'articles.json', output_filename)
    converter.convert()

#create_gexf(AuthorUserComments('Steven Sande'), 'author-user-comments.gexf')
#create_gexf(CommentsPortalUrls(), 'comments-portal-urls.gexf')
#create_gexf(CommentsTuawUrls(), 'comments-tuaw-urls.gexf')
#create_gexf(CommentsTuawAuthors(), 'comments-tuaw-authors.gexf')
create_gexf(ArticleUserComments(), 'article-user-comments.gexf')