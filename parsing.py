import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    'mongodb+srv://egorkalcenko69:ipadmini@yehorkalchenko.qdnz4xh.mongodb.net/?retryWrites=true&w=majority',
    server_api=ServerApi('1')
)

db = client.goit_homework

page_url = 'https://quotes.toscrape.com/'
response = requests.get(page_url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')

authors_list = []
quotes_list = []

for author in authors:
    author_url = 'http://quotes.toscrape.com/author/' + author.text.replace(' ', '-'). replace('.', '')
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip().replace('\n', '')

    authors_list.append(
        {
            'fullname': author.text,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }
    )

for author, quote, tag in zip(authors, quotes, tags):
    tag = tag.find_all('a', class_='tag')
    quotes_list.append(
        {
            'tags': [i.text for i in tag],
            'author': author.text,
            'quote': quote.text.strip().replace('\n', '')
        }
    )


with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_list, f)

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_list, f)

db.authors.insert_many(authors_list)
db.quotes.insert_many(quotes_list)
