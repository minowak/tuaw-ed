import json
import sys
'''
	Generates SQL needed to populate a database.
	Args: in_file [out_file]
'''

def fix_string(obj):
	if isinstance(obj, basestring):
		return obj.replace("'", "\'")
	else:
		for nested in obj.keys():
			if isinstance(obj[nested], basestring):
				obj[nested] = obj[nested].replace("'", "\'")
	
	return obj

def get_content(filename):
	'''
		Opens given file and translate JSON inside it to 
		python object.
	'''
	json_file = open(filename, 'r')
	data = json.load(json_file)
	return data

def SQL_add_author(author):
	return """INSERT INTO authors (name, authorUrl, authorTwitter)
		VALUES ('""" + author['name'] + "', '" + author['url'] + "', '" + author['twitter'] + """')
		ON DUPLICATE KEY UPDATE
		name='""" + author['name'] + "', authorTwitter='" + author['twitter'] + "';\n"
		
def SQL_add_tag(tag):
	tag = tag.replace("'", "")
	return "INSERT IGNORE INTO tags (tag) VALUES ('" + tag + "');\n"
		

def SQL_add_article(article):
	# debug ifs
	if 'content' in article:
		article['content'] = article['content'].replace("'", "\\'").replace("\\\\'", "\\'")
	if 'title' in article:
		article['title'] = article['title'].replace("'", "\\'")
	if 'htmlContent' in article:
		article['htmlContent'] = article['htmlContent'].replace("'", "\\'")
	return """INSERT INTO articles (url, authorUrl, title, timestamp, content, source)
		VALUES ('""" + article['url'] + "', '" + article['authorUrl'] + "', '" + article['title'] + "', '" + article['timestamp'] + """
		', '""" + article['content'] + "', '" + article['source'] + "')" + """
		ON DUPLICATE KEY UPDATE
		title='""" + article['title'] + "', timestamp='" + article['timestamp'] + "', content='" + article['content'] + "', source='" + article['source'] + "';\n";
	
	
def SQL_add_user(user):
	return "INSERT IGNORE INTO users(userId) VALUES ('" + user + "');\n" 
		

def SQL_add_comment(comment):
	comment['content'] = comment['content'].replace("'", "\\'")
	comment['author'] = comment['author'].replace("'", "\\'")
	return """INSERT INTO comments(userId, content, timestamp, url) 
		VALUES ('""" + comment['author'] + "', '" + comment['content'] + "', '" + comment['timestamp'] + "', '" + comment['url'] + """')
		ON DUPLICATE KEY UPDATE
		content='""" + comment['content'] + "', timestamp='" + comment['timestamp'] + "';\n"

def SQL_add_article_tag_relation(articleUrl, tag):
	tag = tag.replace("'", "")
	return """INSERT INTO article_to_tags (tagId, articleUrl)
		VALUES ('""" + tag + "', '" + articleUrl + "');\n"

if __name__ == '__main__':
	out = False

	in_file = sys.argv[1]
	out_file = ''
	if len(sys.argv) > 2:
		out_file = sys.argv[2]
		out = True

 	articles = get_content(in_file)

	SQL = 'DROP DATABASE IF EXISTS tuaw;'
	SQL += 'CREATE DATABASE tuaw;USE tuaw;'
	SQL += """CREATE TABLE articles (
		authorUrl VARCHAR(64) NOT NULL,
		title TEXT NOT NULL,
		timestamp TEXT NOT NULL,
		content LONGTEXT NOT NULL,
		htmlContent LONGTEXT NOT NULL,
		source TEXT NOT NULL,
		url VARCHAR(128) NOT NULL,
		primary KEY (url));"""

	SQL += """CREATE TABLE comments (
		userId VARCHAR(32) NOT NULL,
		content TEXT NOT NULL,
		timestamp TIMESTAMP NOT NULL,
		url VARCHAR(128) NOT NULL,
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
		articleUrl VARCHAR(128) NOT NULL,
		id MEDIUMINT NOT NULL AUTO_INCREMENT,
		primary KEY(id));
		"""

	for article in articles:
		article = fix_string(article)
		author = {}
		author['url'] = article['authorUrl'] # to jest nasze ID
		author['twitter'] = article['authorTwitter']
		author['name'] = article['author'].replace("'", "\\'")

		SQL += SQL_add_author(author)

		for tag in article['tags']:
			SQL += SQL_add_tag(tag)
			SQL += SQL_add_article_tag_relation(author['url'], tag)

		for comment in article['comments']:
			comment = fix_string(comment)
			comment['url'] = article['url']
			SQL += SQL_add_comment(comment)
			SQL += SQL_add_user(comment['author'])

		SQL += SQL_add_article(article)

	SQL = SQL.encode('utf-8')
	if not out:
		print SQL
	else:
		o_file = open(out_file, 'w')
		o_file.write(SQL)
		o_file.close()
	
