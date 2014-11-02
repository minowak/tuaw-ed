import json

new_articles_filename   = "articles.json"
old_articles_filename   = "crawled-articles.json"
output_filename         = "merged.json"

new_articles_file = open(new_articles_filename, 'r')
new_articles = json.load(new_articles_file)
new_articles_file.close()
number_of_accepted_new_articles = 0

old_articles_file = open(old_articles_filename, 'r')
old_articles = json.load(old_articles_file)
old_articles_file.close()
old_articles_urls = [article['url'] for article in old_articles]

for new_article in new_articles:
    if not new_article['url'] in old_articles_urls:
        if len(new_article['author']) > 0:
            number_of_accepted_new_articles += 1
            old_articles.append(new_article)

with open(output_filename, 'w') as output:
    output.write('[')
    for article in old_articles[:-1]:
        json.dump(article, output)
        output.write(',\n')
    json.dump(old_articles[-1], output)
    output.write(']')

print 'accepted new articles: {} / {}'.format(number_of_accepted_new_articles, len(new_articles))

