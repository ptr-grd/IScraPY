#!/usr/bin/env python3

# ===== IMPORTS ===== #

import os
import csv
import time
import config
import pickle
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ===== GENERAL-LOGIC ===== #

# ПОЛЬЗОВАТЕЛЬ. Взаимодействие и настройка скрипта
def user_config():

	print(datetime.now().strftime("%H:%M:%S"), "| [INFO] Запуск скрипта")
	bg_mode = "Включен" if config.BACKGROUND_MODE else "Выключен"
	ua_mode = "Включен" if config.FAKE_USER_AGENT else "Выключен"

	print(datetime.now().strftime("%H:%M:%S"), f"| [INFO] Текущие настройки: \n \n \
  Фоновый режим: {bg_mode} \n \
  Фейк UserAgent: {ua_mode} \n")
	time.sleep(10)

# ДРАЙВЕР. Инициализация, настройка и опции
def init_driver(link):

	# ОПЦИИ БРАУЗЕРА. Фоновый режим
	if config.BACKGROUND_MODE == True:

		options = webdriver.ChromeOptions()
		options.add_argument("--headless")

		driver = webdriver.Chrome(
			executable_path = config.path_driver,
			options=options)

	elif config.BACKGROUND_MODE == False:

		options = webdriver.ChromeOptions()
		driver = webdriver.Chrome(
			executable_path = config.path_driver,
			options=options)
	else:
		print("Ошибка запуска драйвера Chrome")
		exit()

	# ОПЦИИ БРАУЗЕРА. Фейковый юзер-агент
	if config.FAKE_USER_AGENT == True:

		user_agent = UserAgent()
		options.add_argument(f"user-agent={user_agent.random}")

	# ЗАПУСК. Открытие браузера с нужными страницами и опциями
	print(datetime.now().strftime("%H:%M:%S"), "| [INFO] Запуск браузера")
	driver.get('https://www.instagram.com')
	time.sleep(3)

	# КУКИ. Открытие сохраненных cookies
	cookies = pickle.load(open("session.pkl", "rb"))

	for cookie in cookies:
		driver.add_cookie(cookie)
	time.sleep(2)

	# ВХОД. Переход на целевую страницу
	print(datetime.now().strftime("%H:%M:%S"), "| [INFO] Вход в аккаунт")
	driver.get(link)
	time.sleep(10)

	return driver

# ЗАПИСЬ. Запись полученных данных в csv-файл #
def write_csv(data):
	
	with open("../data/data.csv", mode='w', encoding="utf-8") as csv_file:
		
		names = ["Никнейм", "Комментарий"]
		file = csv.DictWriter(csv_file, delimiter = ",", lineterminator = "\r",
			fieldnames = names)
		file.writeheader()

		for item in data.items():
			
			one_user_list = {}
			one_user_list[0] = item[0]
			one_user_list[1] = item[1]
			file.writerow({"Никнейм": one_user_list[0], "Комментарий": one_user_list[1]})

# КОММЕНТАРИИ. Скроллинг, сбор html-данных
def scrolling_comments(driver):

	scroll_target_element = driver.find_element(By.XPATH, config.elements["scroll"])
	action_scroll = ActionChains(driver)

	def check_item(xpath: str) -> bool:
		return len(driver.find_elements(By.XPATH, xpath)) > 0

	print(datetime.now().strftime("%H:%M:%S"), "| [INFO] Начало сбора комментариев")

	# ГЛАВНЫЙ ЦИКЛ. Скроллит все комментарии до конца ленты
	while True:

		check_load_comm_btn = check_item(config.elements["load_comm_btn"])

		if not check_load_comm_btn:
		 	break
			
		soup = BeautifulSoup(driver.page_source, "html.parser")
		comments = soup.find_all("ul", {"class": "Mr508"})

		data = {}

		for index, comment in enumerate(comments):

			nick = comment.find("a", {'class': 'sqdOP'}).text
			text = comment.find("span", {'class': ""}).text

			data[nick] = text
			write_csv(data)

		action_scroll.move_to_element(scroll_target_element).perform()
		
		loading_comm_btn = driver.find_element(By.XPATH, config.elements["load_comm_btn"]).click()
		wait_comm_btn = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, config.elements["load_comm_btn"])))
		
	print(datetime.now().strftime("%H:%M:%S"), f"| [INFO] Конец сбора комментариев")

	
if __name__ == "__main__":

	with open("../link.txt", "r") as file:
		target_link = file.read()

	start_time = datetime.now()

	user_config()
	driver = init_driver(target_link)
	scrolling_comments(driver)

	end_time = datetime.now()
	driver.quit()

	total_time = end_time - start_time
	print(datetime.now().strftime("%H:%M:%S"), "| [INFO] Итоговое время:", str(total_time))
