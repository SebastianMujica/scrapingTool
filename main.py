# This is a sample Python script.
import os
import random
import urllib.request

import exceptiongroup
import requests as requests
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and
from urllib.parse import unquote
# from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import logging
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def check_exists_by_classname(driver_param, classname):
    try:
        driver_param.find_elements(By.CLASS_NAME, classname)
    except:
        return False
    return True


def clear_folder_name(foldername):
    return foldername.replace(' ', '_').replace('|', '').replace('?', '').replace(':', '').replace(';', '').replace(',',
                                                                                                                    '').replace(
        '-', '').replace('.', '').replace('https://', '').replace('.echoscomm.com/', '').replace('-', '_')


def get_category_list(category_list_param):
    categories_list = []
    for category_brand in category_list_param:
        categories_list.append(category_brand.get_attribute('href'))
        print(category_brand.get_attribute('href'))
    return categories_list


service = Service(ChromeDriverManager().install())

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.ERROR)
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://echos-showroom.echoscomm.com/')

WebDriverWait(driver, 5) \
    .until(EC.element_to_be_clickable((By.ID, 'cookie-consent-agree'))) \
    .click()
category_list = driver.find_elements(By.CLASS_NAME, 'hub-rooms-logos__link')
# Extract the links to each brand
# Final info arrays
contador = 0
categories_csv = []
titles_csv = []
slug_csv = []
created_csv = []
body_csv = []
images_csv = []
folder_cvs = []
post_type_csv = []
errors = []

print('Lista total de Marcas ')
categories = get_category_list(category_list)
print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

for category in categories:
    try:
        driver.get(category)
        print('Revisando '+category)
        # load more button
        buttons = []
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR,'button.Button_button__nz0om InfiniteStories_loadMore__dIX_B Button_secondary__tWb_n'.replace(' ', '.'))
        except:
            print("not load more button")

        # print(len(buttons))
        # press each load more button
        while len(buttons) > 0:
            WebDriverWait(driver, 5) \
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.Button_button__nz0om InfiniteStories_loadMore__dIX_B Button_secondary__tWb_n'.replace(
                                                       ' ', '.')))) \
                .click()
            # wait for the next load button apears
            time.sleep(3)
            buttons = driver.find_elements(By.CSS_SELECTOR,
                                           'button.Button_button__nz0om InfiniteStories_loadMore__dIX_B Button_secondary__tWb_n'.replace(
                                               ' ', '.'))
            # print(len(buttons))
        # print('no more buttons')
        post_list = []
        # look for the highlighted post

        highlighted = driver.find_elements(By.CLASS_NAME, 'HighlightedStoryCard_titleLink__e5UuW')
        highlighted_count = len(highlighted)

        normal_post_list = driver.find_elements(By.CLASS_NAME, 'StoryCard_titleLink__El6wj')
        post_list.append(highlighted[0].get_attribute('href'))

        print(' Cantidad de Posts normales ' + str(len(normal_post_list)))

        for normal_post in normal_post_list:
            post_list.append(normal_post.get_attribute('href'))

        print('Tiene ' + str(len(post_list)) + ' posts')
        # post_list = driver.find_elements(By.CLASS_NAME, 'StoriesList_highlightedStoriesContainer__qF7o5')
        # print(post_list)
        # for loop for the post

        for post in post_list:
            print('post numero : ' + str(contador) + ' de ' + str(len(post_list)))
            print(post)
            driver.get(post)
            slug_csv.append(post)
            time.sleep(3)
            # get the images src
            images = driver.find_elements(By.XPATH, "//img[contains(@class,'prezly-slate-media')]")

            dates = driver.find_elements(By.TAG_NAME, "meta")

            for date in dates:
                if date.get_attribute('property') == 'article:published_time':
                    created_csv.append(date.get_attribute('content'))

            urls = []
            for image in images:
                # print(image.get_attribute('src'))
                urls.append(image.get_attribute('src'))
            # create the directory
            try:
                if check_exists_by_classname(driver, 'prezly-slate-heading'):

                    folder_name = clear_folder_name(category) + '/' + clear_folder_name(driver.find_element(By.CLASS_NAME, 'prezly-slate-heading').text)
                    titulo_post = driver.find_element(By.CLASS_NAME, 'prezly-slate-heading').text
                    print(titulo_post)
                else:
                    if check_exists_by_classname(driver, 'prezly-slate-heading prezly-slate-heading--heading-1 prezly-slate-heading--align-center'):
                        folder_name = clear_folder_name(category) + '/' + clear_folder_name(
                            driver.find_element(By.CLASS_NAME, 'prezly-slate-heading prezly-slate-heading--heading-1 prezly-slate-heading--align-center').text)
                        titulo_post = driver.find_element(By.CLASS_NAME, 'prezly-slate-heading prezly-slate-heading--heading-1 prezly-slate-heading--align-center').text
                        print(titulo_post)
                    else:
                        print('Folder Name no encontrado')
                        folder_name = 'no encontrado'
                # driver.find_element(By.CLASS_NAME, 'prezly-slate-heading prezly-slate-heading--heading-1 prezly-slate-heading--align-center')
                folder_cvs.append(folder_name)
            except Exception as e:
                print(e)
                print('Error con ' + post)
                folder_name = random.Random
                titulo_post = 'No encontrado'
                folder_cvs.append(folder_name)
                continue

            # os.makedirs(folder_name, exist_ok=True)
            # download the images
            format_url = []
            for url in urls:
                format_url.append(unquote(os.path.basename(url)))
                print('Image Url : ' + url)
                print('Folder name : ' + folder_name)
                print(f'wget -nc -P {folder_name} {url} ')
                os.system(f'wget -nc -P {folder_name} {url} ')
            try:
                categories_csv.append(category.replace('https://', '').replace('.echoscomm.com/', '').replace('-', ' '))
                titles_csv.append(titulo_post)
                body_csv.append(driver.find_element(By.CLASS_NAME, 'ContentRenderer_renderer__tPJbs').get_attribute(
                    'innerHTML').encode())
            except NoSuchElementException as e:
                print(e)
            if highlighted_count > 0:
                post_type_csv.append('highlighted')
                highlighted_count -= 1
            else:
                post_type_csv.append('normal')
            images_csv.append(' ,'.join(format_url))
    except Exception as e:
        logging.error(e)
print(len(categories_csv))
print(len(post_type_csv))
print(len(titles_csv))
print(len(slug_csv))
print(len(body_csv))
print(len(images_csv))

diferencia = len(created_csv) - len(images_csv)
i = 0
while i < diferencia:
    created_csv.pop()
    i += 1

diferencia = len(slug_csv) - len(images_csv)
i = 0
while i < diferencia:
    slug_csv.pop()
    i += 1

print(len(created_csv))
print(len(folder_cvs))

df = pd.DataFrame(
    {'category': categories_csv, 'post_type': post_type_csv, 'titles': titles_csv, 'slug': slug_csv, 'body': body_csv,
     'images': images_csv, 'created_at': created_csv, 'folder_name': folder_cvs})
df.to_csv('test.csv', index=True, sep=';')
