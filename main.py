import os
import json
import time
import requests

import bs4
import fake_headers

def write_json(dict, dir = os.getcwd(), json_name = 'result.json'):
    with open(f'{dir}/{json_name}', 'w', encoding='utf-8') as f:
        json.dump(dict, f, ensure_ascii=False, indent=4, sort_keys=True)

words_search = ('Django Flask')
region = (1, 2,)

main_url = 'https://spb.hh.ru/search/vacancy'

def main():
    pages = 0
    result = list()
    while True:

        header_gen = fake_headers.Headers(browser="chrome", os="win")
        headers = header_gen.generate()
        params = {
            'text':words_search,
            'area':region,
            'order_by': 'publication_time',
            'search_period':0,
            'page':pages
        }
        response = requests.get(main_url, headers=headers, params=params)
        main_html = bs4.BeautifulSoup(response.text, "lxml")

        main_articles = main_html.find("div", id="a11y-main-content")
        articles_tags = main_articles.find_all("div", class_="serp-item", limit = 50)

        for article_tag in articles_tags:

            link = article_tag.find(class_ = 'serp-item__title').get('href')
            company = article_tag.find('a', class_ = 'bloko-link bloko-link_kind-tertiary').get_text().replace(' ', ' ')
            address = list(article_tag.find(class_="vacancy-serp-item__info").children)[1].text.replace(' ', ' ')
            if article_tag.find('span', class_ = 'bloko-header-section-3'):
                salary = article_tag.find('span', class_ = 'bloko-header-section-3').get_text().replace(" ", '.')
            else:
                salary = 'не указана'

            result.append({
                'ссылка':link,
                'вилка зп':salary,
                'название компании':company,
                'город':address
            })
        time.sleep(0.4)

        if len(articles_tags) >= 20:
            pages +=1
        else:
            break

    return result

if __name__ == '__main__':
    res = main()
    write_json(res)