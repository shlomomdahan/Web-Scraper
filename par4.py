import requests
from bs4 import BeautifulSoup

a = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'

if __name__ == "__main__":

    url = a

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    articles = soup.find_all('article')

    links = []
    for article in articles:
        article_type = article.find('span', "c-meta__type").text
        if article_type == 'News':
            links.append(article.find('a').get('href'))

    full_paths = ['https://www.nature.com' + link for link in links]

    files = []
    for link in full_paths:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('title').text
        article_body = soup.find('div', "c-article-body u-clearfix").text.strip()
        article_body.replace("\n", "")
        with open(f'{title.replace(" ", "_")}.txt', 'w') as file:
            file.write(article_body)