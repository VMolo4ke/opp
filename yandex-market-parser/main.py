import time
import csv
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup


url = 'https://market.yandex.ru/catalog--stroitelnye-instrumenty/55166/list?hid=1618974&rs=eJwzsv3EaMXBILDwEKsEg8K8F0kaZ86warS9esum8eHnOnaNpicfWDVmnX7IpvHyNKtG4zMg78_DeawanUBVjWdYATR4G1M%2C&qrfrom=1'
items = []


def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver,
            platform='Win32')
    return driver


def get_full_page_height(driver):
    return driver.execute_script(
        "return Math.max("
        "document.body.scrollHeight, "
        "document.documentElement.scrollHeight,"
        "document.body.offsetHeight, "
        "document.documentElement.offsetHeight,"
        "document.body.clientHeight, "
        "document.documentElement.clientHeight"
        ");"
    )


def scroldown(driver):
    max_height_i = 0
    while max_height_i < 10:
        max_height_prev = get_full_page_height(driver)
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.5)
        if max_height_prev < get_full_page_height(driver):
            max_height_i = 0
        else:
            max_height_i += 1


def get_reviews_card(driver, url):
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)
    driver.get('https://market.yandex.ru' + url)
    time.sleep(0.5)
    page_html_main = BeautifulSoup(driver.page_source, 'html.parser')
    title = page_html_main.find('h1').getText()
    article = page_html_main.find('div', {'id': 'cardContent'}).find('div').find('div').find('div')
    article = article.findChildren('div', recursive=False)[2].findChildren('div', recursive=False)[1].find('div')
    article = article.findChildren('div', recursive=False)[5].find('div').find('div').find('div').find('div').find('div').find('div')
    article = article.findChildren('div', recursive=False)[1].find('div').find('div').find('span').getText()
    url_id = url.split('?')[0]
    driver.get('https://market.yandex.ru' + url_id + '/reviews')
    time.sleep(1)
    scroldown(driver)
    page_html = BeautifulSoup(driver.page_source, 'html.parser')
    content = page_html.find('div', {'id': 'ServerLayoutRenderer'})
    content = content.find('div').find('div').find('div')
    content = content.findChildren('div', recursive=False)
    for i in range(len(content)):
        box = content[i].find('div').find('div').findChildren('div', recursive=False)
        for index in range(len(box)):
            item = {
                'article': article,
                'name_yandex': title,
                'name_list': title,
                'date': '',
                'reviewId': '',
                'name': '',
                'rating': '',
                'worth': '',
                'flaws': '',
                'comment': '',
                'img': '',
                'ie_xml_id': ''
            }
            try:
                rating = box[index].find('div').find('div').find('div').find('div')
            except AttributeError:
                driver.close()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[0])
                return
            rating = rating.findChildren('div', recursive=False)[1].find('meta').attrs['content']
            item['rating'] = rating
            reviewId = box[index].find('div').find('div').attrs['id'].split('_')[1]
            item['reviewId'] = reviewId
            date = box[index].find('div').find('div').find('div').find('div').find('meta').attrs['content']
            item['date'] = date
            card = box[index].find('div').find('div').findChildren('div', recursive=False)[1].find('div')
            flag1 = 'no'
            flag2 = 'no'
            flag3 = 'no'
            flag_img = 1

            if len(card.findChildren('div', recursive=False)) > 3:
                flag_img = 2
                img = card.findChildren(recursive=False)[1].findChildren('img', recursive=True)
                for image in img:
                    item['img'] += ' ' + image.attrs['src'] + ','

            try:
                flag1 = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[0].findChildren(recursive=False)[0].getText()
            except IndexError:
                pass
            except AttributeError:
                pass

            try:
                flag2 = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[1].findChildren(recursive=False)[0].getText()
            except IndexError:
                pass
            except AttributeError:
                pass

            try:
                flag3 = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[2].findChildren(recursive=False)[0].getText()
            except IndexError:
                pass
            except AttributeError:
                pass

            try:
                item['name'] = card.find('div').findChildren(recursive=False)[1].find('div').find('a').find('span').getText()
            except IndexError:
                pass
            except AttributeError:
                pass

            try:
                if 'Достоинства' in flag1:
                    item['worth'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[0].findChildren(recursive=False)[1].getText()
                if 'Недостатки' in flag1:
                    item['flaws'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[0].findChildren(recursive=False)[1].getText()
                if 'Комментарий' in flag1:
                    item['comment'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[0].findChildren(recursive=False)[1].getText()
            except IndexError:
                pass

            try:
                if 'Достоинства' in flag2:
                    item['worth'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[1].findChildren(recursive=False)[1].getText()
                if 'Недостатки' in flag2:
                    item['flaws'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[1].findChildren(recursive=False)[1].getText()
                if 'Комментарий' in flag2:
                    item['comment'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[1].findChildren(recursive=False)[1].getText()
            except IndexError:
                pass

            try:
                if 'Достоинства' in flag3:
                    item['worth'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[2].findChildren(recursive=False)[1].getText()
                if 'Недостатки' in flag3:
                    item['flaws'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[2].findChildren(recursive=False)[1].getText()
                if 'Комментарий' in flag3:
                    item['comment'] = card.findChildren(recursive=False)[flag_img].find('span').find('div').findChildren(recursive=False)[2].findChildren(recursive=False)[1].getText()
            except IndexError:
                pass

            items.append(item)

    driver.close()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])


def get_mainpage_cards(driver, url):
    driver.get(url)
    scroldown(driver)
    main_page_html = BeautifulSoup(driver.page_source, 'html.parser')

    content = main_page_html.find_all('section', {'class': '_3BHKe'})
    for i in range(len(content)):
        block = content[i].find_all('div', recursive=False)
        for index in range(len(block)):
            try:
                card = block[index].find('div').find('article').find('div').find('div').find('div').find('div').find('div').find('div').find('div').find('a')
                get_reviews_card(driver, card['href'])
            except AttributeError:
                continue


def get_reviews(reviews):
    reviews = items

    with open('eggs.csv', 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Артикул/SKU', 'name parsing / название товара с нашего списка',
                             'name in yandex market / название товара с парсинга ', 'reviewId',
                             'name / имя', 'date / дата', 'Оценка', 'Комментарий', 'Достойснтво',
                             'Недостатки', 'Фото', 'Внешний код {IE_XML_ID}'])
        for review in reviews:
            writer.writerow([review['article'], review['name_list'], review['name_yandex'],
                             review['reviewId'], review['name'], review['date'], review['rating'],
                             review['comment'], review['worth'], review['flaws'], review['img'], 'hz'])


if __name__ == '__main__':
    driver = init_webdriver()
    get_mainpage_cards(driver, url)
    get_reviews(items)
    driver.quit()