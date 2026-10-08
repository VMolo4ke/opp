import requests
from time import sleep
from math import floor
from steampy.client import SteamClient
from steampy.models import GameOptions
from steampy.exceptions import ApiException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


while True:
    try:
        steam_client = SteamClient('7D87AFD6C9BF1FBB614D4275EE26148C')
        steam_client.login('vmolo4ke', '13Qeadzc)', 'steam_guard.json')
        break
    except AttributeError:
        sleep(5)


def find_item_in_inventory(items):
    for item in items.values():
        return {'id': item['id'], 'name': item['market_hash_name']}


class Bot:

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=r'geckodriver.exe')

    def close_browser(self):
        self.driver.close()
        self.driver.quit()

    def xpath_exists(self, xpath) -> bool:
        try:
            self.driver.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False

        return exist

    def log_into_steam(self):
        driver = self.driver
        driver.get('https://steamcommunity.com/login/home/')
        driver.implicitly_wait(5)

        driver.find_element_by_class_name('global_action_link').click()
        sleep(2)

        driver.find_element_by_css_selector('input[type=text]').send_keys('vmolo4ke')
        sleep(1)

        driver.find_element_by_css_selector('input[type=password').send_keys('13Qeadzc)')
        sleep(1)

        driver.find_element_by_css_selector('button[type=submit').click()
        sleep(2)

        self.type_steam_guard_code()

    def type_steam_guard_code(self):
        if self.xpath_exists('//div[@class="newlogindialog_SegmentedCharacterInput_1kJ6q"]'):
            code = input('Введите код: ')
            for i in range(5):
                self.driver.find_elements_by_css_selector('input[type=text]')[i].send_keys(code[i])
        sleep(3)
        if self.xpath_exists('//input[@class="btn_green_white_innerfade"]'):
            self.driver.find_element_by_xpath('//input[@class="btn_green_white_innerfade"]').click()

    def fetch_price(self, item_name):
        driver = self.driver
        driver.get('https://steamcommunity.com/market/listings/730/{}'.format(item_name))
        sleep(0.5)
        if len(driver.find_elements_by_xpath('//table[@class="market_commodity_orders_table"]')) == 1:
            price = float(
                driver.find_elements_by_xpath('//span[@class="market_commodity_orders_header_promote"]')[1]
                .text.replace(',', '.').partition(' ')[0])
        else:
            price = float(driver.find_elements_by_xpath('//span[@class="market_commodity_orders_header_promote"]')[3]
                          .text.replace(',', '.').partition(' ')[0])
        return str(floor(price * 0.868 * 100))


key = '6dk7C6C075840l0rS4mDsTdTp78psGW'

bot = Bot()
bot.log_into_steam()

while True:
    trades = requests.get('https://market.csgo.com/api/v2/trades/?key={}'.format(key))
    print(trades.text)
    try:
        if not trades.json()['success']:
            sleep(10)
            continue
        for trade in trades.json()['trades']:
            if trade['dir'] == 'out' and trade['trade_id'] != '0':
                requests.post('https://market.csgo.com/api/v2/trade-request-take?key={}'.format(key))
                sleep(1)

                try:
                    steam_client.accept_trade_offer(trade['trade_id'])
                    quantity_items_to_receive = steam_client.get_trade_offer(trade['trade_id'])['response']['offer'][
                        'items_to_receive']
                except ApiException:
                    continue
                sleep(1)

                for num_of_iterations in range(len(quantity_items_to_receive)):
                    item_sell = find_item_in_inventory(steam_client.get_my_inventory(GameOptions.CS))
                    steam_client.market.create_sell_order(item_sell['id'], GameOptions.CS,
                                                          bot.fetch_price(item_sell['name']))
        sleep(5)
    except requests.exceptions.JSONDecodeError or KeyError:
        sleep(1)
        continue
