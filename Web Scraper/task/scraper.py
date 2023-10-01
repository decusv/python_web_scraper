import os

import requests
from bs4 import BeautifulSoup
import string


def scrape_articles(number_of_pages, type_of_article):
    for index in range(1, number_of_pages + 1):
        url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(index)
        translator = str.maketrans('', '', string.punctuation)
        directory_name = f'Page_{index}'
        os.makedirs(directory_name)
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

        if response.status_code == 200 and "articles" in url and "nature.com" in url:
            soup_response = BeautifulSoup(response.text, 'html.parser')
            list_of_articles = soup_response.find_all(class_='app-article-list-row__item')

            for article in list_of_articles:
                article_type = article.find(class_='c-meta__type')
                stripped_article_type = article_type.get_text()
                if stripped_article_type == type_of_article:
                    article_link = article.find(class_='c-card__link u-link-inherit').get('href')
                    article_response = requests.get("https://www.nature.com" + article_link,
                                                    headers={'Accept-Language': 'en-US,en;q=0.5'})
                    soup_response = BeautifulSoup(article_response.text, 'html.parser')
                    article_body = soup_response.find(class_='article__teaser').get_text()

                    title = (soup_response.find(class_='c-article-magazine-title').get_text().translate(translator)
                             .replace(" ", "_"))
                    file_name = title + ".txt"
                    file_path = os.path.join(directory_name, file_name)
                    print(file_path)

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(article_body)

        else:
            print("Invalid page!")


firstParam = int(input("> "))
secondParam = str(input("> "))
scrape_articles(firstParam, secondParam)
