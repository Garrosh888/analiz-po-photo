import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import smtplib # Модуль для работы с почтой

# Основной класс
class Currency:
	# Ссылка на нужную страницу
	DOLLAR_grn = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%BD&sca_esv=576160195&sxsrf=AM9HkKm1Po--KPGu1Nrsd_MPapPvq_cGHw%3A1698167901600&ei=Xfw3ZceWJIamwPAP1ZGAqAk&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+uhhy&gs_lp=Egxnd3Mtd2l6LXNlcnAiFNC00L7Qu9C70LDRgCDQuiB1aGh5KgIIADIHEAAYDRiABDIHEAAYDRiABDIHEAAYDRiABDIGEAAYHhgNMggQABgFGB4YDTIIEAAYBRgeGA0yCBAAGAUYHhgNMgoQABgFGB4YDRgPMggQABgFGB4YDUjdLFC1CljoEnACeAGQAQCYAW2gAc8DqgEDNC4xuAEByAEA-AEBwgIKEAAYRxjWBBiwA8ICChAAGIoFGLADGEPCAgcQIxiKBRgnwgIFEAAYgATCAgoQABiABBgUGIcCwgIHEAAYgAQYCsICBhAAGBYYHsICCBAAGBYYHhgKwgIJEAAYgAQYChgqwgILEAAYFhgeGPEEGArCAgkQABgWGB4Y8QTiAwQYACBBiAYBkAYK&sclient=gws-wiz-serp"


	# Заголовки для передачи вместе с URL
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

	current_converted_price = 0
	difference = 5 # Разница после которой будет отправлено сообщение на почту

	def __init__(self):
		# Установка курса валюты при создании объекта
		self.current_converted_price = float(self.get_currency_price().replace(",", "."))

	# Метод для получения курса валюты
	def get_currency_price(self):
		# Парсим всю страницу
		full_page = requests.get(self.DOLLAR_grn, headers=self.headers)

		# Разбираем через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser')

		# Получаем нужное для нас значение и возвращаем его
		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		return convert[0].text

	# Проверка изменения валюты
	def check_currency(self):
		currency = float(self.get_currency_price().replace(",", "."))
		if currency >= self.current_converted_price + self.difference:
			print("Курс сильно вырос, может пора что-то делать?")
			self.send_mail()
		elif currency <= self.current_converted_price - self.difference:
			print("Курс сильно упал, может пора что-то делать?")
			self.send_mail()

		print("Сейчас курс: 1 доллар = " + str(currency))
		time.sleep(3) # Засыпание программы на 3 секунды
		self.check_currency()

	# Отправка почты через SMTP
	def send_mail(self):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('ВАША ПОЧТА', 'ПАРОЛЬ')

		subject = 'Currency mail'
		body = 'Currency has been changed!'
		message = f'Subject: {subject}\n{body}'

		server.sendmail(
			'От кого',
			'Кому',
			message
		)
		server.quit()

# Создание объекта и вызов метода
currency = Currency()
currency.check_currency()
