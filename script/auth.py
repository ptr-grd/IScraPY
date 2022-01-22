#!/usr/bin/env python3

import time
import config
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# === Описание === #
# Авторизации аккаунта и сохранение
# файлов cookies в файловую систему
# для дальнейшей работы скрипта.
# Требуется выполнить единожды.

authorization_link = 'https://www.instagram.com'

options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server={config.PROXY}')

driver = webdriver.Chrome(
	executable_path = config.path_driver,
	options=options)

driver.get(authorization_link)
time.sleep(3)

# Вводим данные: логин
user_login = driver.find_element(By.XPATH, config.elements["user_login"])
user_login.send_keys(config.USER)

# Вводим данные: пароль
user_password = driver.find_element(By.XPATH, config.elements["user_password"])
user_password.send_keys(config.PASSWORD)
time.sleep(2)

# Заход в аккаунт
login_btn_windowsite = driver.find_element(By.XPATH, config.elements["login_link"]).click()
time.sleep(10)

# Обход диалогового окна при входе в аккаунт
dialog_window = driver.find_element(By.XPATH, config.elements["dialog_window"]).click()
time.sleep(5)

# Сохранение cookie для дальнейшего входа
pickle.dump(driver.get_cookies(), open("session.pkl","wb"))
time.sleep(2)

driver.quit()
