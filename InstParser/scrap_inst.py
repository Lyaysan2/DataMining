from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
from bs4 import BeautifulSoup as bs
import json
import re

import config


class Inst:
    def __init__(self, url_inst, login, password):
        self.url = url_inst
        self.login = login
        self.password = password
        self.data = {'posts': []}
        self.partners = {'items': []}
        self.driver = webdriver.Safari()

    def send_keys_with_delays(self, element, value):
        wait = WebDriverWait(self.driver, 10)
        for i in range(len(value)):
            element.send_keys(value[i])
            wait.until(lambda _: element.get_property('value')[:i] == value[:i])

    def auth_inst(self):
        print(datetime.today().strftime(f'%H:%M:%S | Выполняется авторизация в Instagram.'))
        self.driver.get(self.url)
        time.sleep(3)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
        lgn = self.driver.find_element_by_name('username')
        passwd = self.driver.find_element_by_name('password')
        self.send_keys_with_delays(lgn, self.login)
        self.send_keys_with_delays(passwd, self.password)
        passwd.send_keys(Keys.ENTER)
        time.sleep(6)
        notn = self.driver.find_element_by_class_name("yWX7d")
        notn.click()
        print(datetime.today().strftime(f'%H:%M:%S | Авторизация в Instagram выполнена.'))

    def first_post(self):
        self.driver.find_element_by_class_name("kIKUG").click()
        time.sleep(2)

    def scrap_post(self, url):
        self.driver.get(url)
        soup = bs(self.driver.page_source, 'html.parser')
        time.sleep(5)

        # amount of post
        num_post = soup.find('div', class_='_7UhW9 vy6Bb MMzan KV-D4 uL8Hv T0kll').find_all('span')[-1].text

        self.first_post()
        self.analysis()

        for i in range(num_post):
            self.driver.find_elements_by_css_selector(
                'body > div.RnEpo._Yhr4 > div.Z2Inc._7c9RR > div > div.l8mY4.feth3 > button')[0].click()
            self.analysis()

        self.get_partners()

    def analysis(self):
        user_dict = {}
        time.sleep(5)

        # url
        url = self.driver.current_url
        # text
        try:
            text = self.driver.find_elements_by_css_selector('body > div.RnEpo._Yhr4 > div.pbNvD.QZZGH.bW6vo > div > article > div > div.HP0qD > div > div > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > div.MOdxS > span')[0].text
        except IndexError:
            text = ''
        # partner
        partner = re.findall(r'@[\w\.]*\b', text)
        # like
        try:
            like = self.driver.find_elements_by_css_selector('body > div.RnEpo._Yhr4 > div.pbNvD.QZZGH.bW6vo > div > article > div > div.HP0qD > div > div > div.eo2As > section.EDfFK.ygqzn > div > div.qF0y9.Igw0E.IwRSH.eGOV_.vwCYk.YlhBV > div > a > div > span')[0].text
        except IndexError:
            like = 0

        user_dict['url'] = url
        user_dict['title'] = text
        user_dict['like'] = like
        user_dict['partners'] = partner
        self.write_json(user_dict)

    def get_partners(self):

        list_partn = {}
        with open("data.json", "r") as read_file:
            data = json.load(read_file)
            for d in data['posts']:
                if len(d['partners']) != 0:
                    for i in d['partners']:
                        if i not in list_partn:
                            list_partn[i] = []
                            list_partn[i].append(1)
                            list_partn[i].append([])
                            list_partn[i][1].append(d['like'])
                        else:
                            list_partn[i][0] += 1
                            list_partn[i][1].append(d['like'])

        for item in list_partn:
            url = 'https://www.instagram.com/' + re.search(r'(@)(.+)', item)[2]
            self.driver.get(url)
            soup = bs(self.driver.page_source, 'html.parser')
            time.sleep(3)

            prtn = {}
            if soup.find(class_='QGPIr') is None:
                partner_name = 'None Object'
            else:
                try:
                    partner_name = soup.find(class_='QGPIr').find_all('span')[-1].text
                except IndexError:
                    partner_name = ''

            prtn['url'] = url
            prtn['name'] = partner_name
            prtn['count'] = list_partn.get(item)[0]
            prtn['likes'] = list_partn.get(item)[1]

            self.write_json2(prtn)

    def write_json(self, info):
        self.data['posts'].append(info)
        with open('data.json', 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def write_json2(self, info):
        self.partners['items'].append(info)
        with open('partners.json', 'w') as f:
            json.dump(self.partners, f, ensure_ascii=False, indent=2)

    def close_browser(self):
        print('Работа завершена.')
        self.driver.quit()
