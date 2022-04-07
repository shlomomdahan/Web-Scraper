import requests
from bs4 import BeautifulSoup
import os

if __name__ == "__main__":
    num_pages = int(input('Enter how many pages to search: '))
    type_of_article = input('Enter type of article to search: ')

    start_url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    r = requests.get(start_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    url_list = ['https://www.nature.com/nature/articles?sort=PubDate&year=2020']

    for page in range(num_pages):
        next_url = soup.find('li', {"data-test": "page-next"}).a.get('href')
        full_url = 'https://www.nature.com' + next_url
        url_list.append(full_url)
        r = requests.get(full_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        os.mkdir('Page_' + f'{page + 1}')

    del url_list[-1]

    for idx, url in enumerate(url_list):

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')

        links = []
        for article in articles:
            article_type = article.find('span', "c-meta__type").text
            if article_type == type_of_article:
                links.append(article.find('a').get('href'))

        full_paths = ['https://www.nature.com' + link for link in links]

        files = []
        for link in full_paths:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html.parser')
            title = soup.find('title').text
            article_body = soup.find('div', "c-article-body u-clearfix").text.strip()
            article_body.replace("\n", "")
            directory_name = 'Page_' + f'{idx + 1}'
            parent = os.getcwd()
            path = os.path.join(parent, directory_name)
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            file_name = f'{title.replace(" ", "_")}.txt'

            completeName = os.path.join(path, file_name)

            with open(completeName, 'w') as file:
                file.write(article_body)