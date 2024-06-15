from bs4 import BeautifulSoup
import sqlite3
import requests
import csv


for index in range(1,5):
    url = f'https://ss.ge/ka/sales/list?Page={index}&CategoryId=100'
    response = requests.get(url)
    info = BeautifulSoup(response.text, 'html.parser')
    data = info.find('div', class_='sales-results')
    articles = data.find_all('div', class_='jobs_latest_article_each latest_article_each')


    for article in articles:
        price = article.find('div', class_='latest_price').text.strip().replace(' ', '')
        title = article.find('div', class_='latest_title').text.strip()
        place = article.find('div',class_='time-loaction').span.text.strip().replace('-','')
        datetime = article.find('div',class_='time-loaction').find_all('span')[1].text.strip().replace('-','')


        conn = sqlite3.connect('items.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items
        (Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Price INTEGER,
        Title Varchar(100),
        place VARCHAR(100),
        Datetime TEXT
        )
        ''')

        cursor.executemany('''
        INSERT INTO items
        (Price, Title, place, Datetime)
        VALUES (?,?,?,?)
        ''',[(price,title, place, datetime)])

        conn.commit()


        with open('items.csv', 'a', encoding='utf-8_sig', newline='') as file:
            write = csv.writer(file)
            write.writerow([price, title, place, datetime])

    conn.close()