import requests
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import customtkinter as ctk
import tkinter

key = '6dk7C6C075840l0rS4mDsTdTp78psGW'

username = 'vmolo4ke'
password = '13Qeadzc)'

tableLink = 'https://tradeback.io/ru/comparison'
min_prices = ['0.03', '0.1', '0.5', '2', '5']

code = ''
percent = 0


def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.code = ''

        self.geometry('460x270')
        self.title('Money')
        self.resizable(False, False)

        ctk.set_appearance_mode("Dark")

        self.min_percentage_label = ctk.CTkLabel(master=self, text='Укажите минимальный процент: 50.0%', width=120,
                                                 height=25, corner_radius=8)
        self.min_percentage_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.min_percentage_slider = ctk.CTkSlider(master=self, width=160, height=16,
                                                   border_width=5, command=self.slider_event)
        self.min_percentage_slider.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.steam_guard_label = ctk.CTkLabel(master=self, text='Steam Guard:', width=120, height=25, corner_radius=8)
        self.steam_guard_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.steam_guard_entry = ctk.CTkEntry(master=self, width=120, height=30, corner_radius=10, justify='center')
        self.steam_guard_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def slider_event(self, value):
        self.min_percentage_label.configure(text='Укажите минимальный процент: {}%'.format(to_fixed(value * 100, 1)))


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
        driver.get(tableLink)
        driver.implicitly_wait(5)

        driver.find_element_by_class_name('global_action_link').click()
        sleep(2)

        driver.find_element_by_css_selector('input[type=text]').send_keys(username)
        sleep(1)

        driver.find_element_by_css_selector('input[type=password').send_keys(password)
        sleep(1)

        driver.find_element_by_css_selector('button[type=submit').click()
        sleep(2)

        self.type_steam_guard_code()

    def type_steam_guard_code(self):
        global code, percent
        if self.xpath_exists('//div[@class="newlogindialog_SegmentedCharacterInput_1kJ6q"]'):
            app = App()
            while len(code) != 5:
                app.update_idletasks()
                app.update()
                code = app.steam_guard_entry.get()
                if len(code) == 5:
                    percent = to_fixed(app.min_percentage_slider.get() * 100, 1)
                    app.destroy()
            for i in range(5):
                self.driver.find_elements_by_css_selector('input[type=text]')[i].send_keys(code[i])
        sleep(3)
        if self.xpath_exists('//input[@class="btn_green_white_innerfade"]'):
            self.driver.find_element_by_xpath('//input[@class="btn_green_white_innerfade"]').click()

    def find_items(self):
        driver = self.driver
        items_best = []
        items_name = driver.find_elements_by_class_name('copy-name')
        items_price_tm = driver.find_elements_by_xpath('//span[@class="price rub"]')
        for i in range(7):
            items_best.append({'name': items_name[i].text, 'price_tm': float(items_price_tm[i].text)})
        return items_best

    def set_param(self, link):
        driver = self.driver

        driver.get(link)
        sleep(1)

        driver.refresh()
        sleep(3)

        driver.find_element_by_class_name('column-profit').click()
        sleep(2)

    def hard_worker(self, items_data):
        driver = self.driver
        for item in items_data:
            driver.get('https://steamcommunity.com/market/listings/730/{}'.format(item['name']))
            sleep(0.5)

            if len(driver.find_elements_by_xpath('//table[@class="market_commodity_orders_table"]')) == 1:
                driver.find_element_by_id('market_buyorder_info_show_details').find_element_by_tag_name('span').click()
                sleep(0.5)
                item_price_steam = float(driver.find_element_by_css_selector('td[align=right]').text.replace(',', '.')
                                         .partition(' ')[0])
                item_quantity_steam = int(driver.find_elements_by_css_selector('td[align=right]')[1].text)
            else:
                elements = driver.find_elements_by_css_selector('td[align=right]')
                item_price_steam = float(elements[12].text.replace(',', '.').partition(' ')[0])
                item_quantity_steam = int(elements[13].text)

            profit = to_fixed((item_price_steam - (item_price_steam / 100 * 13) - item['price_tm'])
                              / (item['price_tm'] / 100))
            if float(profit) >= float(percent):
                print('{}\n'
                      'Цена на TM: {}₽\n'
                      'Цена в Steam: {}₽ - {}\n'
                      'Выгода: {}%\n'.format(item['name'], item['price_tm'], item_price_steam,
                                             item_quantity_steam, profit))
                for i in range(item_quantity_steam):
                    buy = requests.post('https://market.csgo.com/api/v2/buy?key={}&hash_name={}&price={}'
                                        .format(key, item['name'], item['price_tm'] * 100))
                    sleep(2)
                    try:
                        if not buy.json()['success']:
                            break
                    except requests.exceptions.JSONDecodeError:
                        continue


if __name__ == '__main__':
    bot = Bot()
    bot.log_into_steam()
    while True:
        for index in range(5):
            bot.set_param('https://tradeback.io/ru/comparison#{%22app%22:2,%22services%22:'
                          '[%22tm_market%22,%22steamcommunity.com%22],%22updated%22:[],%22categories%22:'
                          '[[%22normal%22],[%22orders%22]],%22hold_time_range%22:[8,8],%22price%22:[['
                          + min_prices[index] + '],[]],%22count%22:[[],[1]],%22profit%22:[[],[]]}')
            best_items = bot.find_items()
            bot.hard_worker(best_items)
            sleep(10)
