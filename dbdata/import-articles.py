import json
import sys
'''
	Generates SQL needed to populate a database.
	Args: in_file [out_file]
'''

def get_content(filename):
	'''
		Opens given file and translate JSON inside it to 
		python object.
	'''
	json_file = open(filename, 'r')
	data = json.load(json_file)
	return data

def SQL_add_author(author):
	return """INSERT INTO author (name, authorUrl, authorTwitter)
		VALUES ('""" + author['name'] + "', '" + author['url'] + "', '" + author['twitter'] + """,)
		ON DUPLICATE KEY UPDATE
		name='""" + author['name'] + "', authorTwitter='" + author['twitter'] + "';"
		
def SQL_add_tag(tag):
	return "INSERT IGNORE INTO tags (tag) VALUES ('" + tag + "');"
		

def SQL_add_article(article):
	return """INSERT INTO articles (authorUrl, title, timestamp, content, source)
		VALUES ('""" + article['url'] + "', '" + article['title'] + "', '" + article['timestamp'] + """
		', '""" + article['content'] + "', '" + article['source'] + "')" + """
		ON DUPLICATE KEY UPDATE
		title='""" + article['title'] + "', timestatmp='" + article['timestamp'] + "', content='" + article['content'] + "', source='" + article['source'] + "';";
	
def SQL_add_user(user):
	return "INSERT IGNORE INTO users(userId) VALUES ('" + user + "');" 
		

def SQL_add_comment(comment):
	return """INSERT INTO comments(userId, content, timestamp, url) 
		VALUES ('""" + comment['author'] + "', '" + comment['content'] + "', '" + comment['timestamp'] + "', '" + comment['url'] + """')
		ON DUPLICATE KEY UPDATE
		content='""" + comment['content'] + "', timestamp='" + comment['timestamp'] + "';"

def SQL_add_article_tag_relation(articleUrl, tag):
	return """INSERT INTO article_to_tags (tagId, articleUrl)
		VALUES ('""" + tag + "', '" + articleUrl + "');"

if __name__ == '__main__':
	out = False

	in_file = sys.argv[1]
	out_file = ''
	if len(sys.argv) > 2:
		out_file = sys.argv[2]
		out = True

 	articles = get_content(in_file)

	SQL = 'DROP DATABASE IF EXISTS tuaw;'
	SQL += 'CREATE DATABASE tuaw;'
	SQL += """CREATE TABLE articles (
		authorUrl VARCHAR(64) NOT NULL,
		title TEXT NOT NULL,
		timestamp TEXT NOT NULL,
		content LONGTEXT NOT NULL,
		source TEXT NOT NULL,
		url VARCHAR(128) NOT NULL AUTO_INCREMENT
		primary KEY (url));"""

	SQL += """CREATE TABLE comments (
		userId VARCHAR(32) NOT NULL,
		content TEXT NOT NULL,
		timestamp TIMESTAMP NOT NULL,
		id MEDIUMINT NOT NULL AUTO_INCREMENT,
		primary KEY (id)
		);"""
		
	SQL += """CREATE TABLE authors(
		authorUrl VARCHAR(64) NOT NULL,
		name TEXT NOT NULL,
		authorTwitter TEXT NOT NULL,
		primary KEY (authorUrl)
		);"""

	SQL += """CREATE TABLE users(
		userId VARCHAR(32) NOT NULL,
		primary KEY(userId)
		);"""

	SQL += """CREATE TABLE tags(
		tag VARCHAR(32) NOT NULL,
		primary KEY(tag)
		);"""

	SQL += """CREATE TABLE article_to_tags(
		tagId VARCHAR(32) NOT NULL,
		articleUrl VARCHAR(128) NOT NULL);
		"""

	for article in articles:
		author = {}
		author['url'] = article['authorUrl'] # to jest nasze ID
		author['twitter'] = article['authorTwitter']
		author['name'] = article['author']

		SQL += SQL_add_author(author)

		for tag in article['tags']:
			SQL += SQL_add_tag(tag)
			SQL += SQL_add_article_tag_relation(author['url'], tag)

		for comment in article['comments']:
			comment['url'] = article['url']
			SQL += SQL_add_comment(comment)
			SQL += SQL_add_user(comment['author'])

		SQL += SQL_add_article(article)

	print SQL
	
