import requests
from bs4 import BeautifulSoup
import time
import smtplib

class Currency:
    DOLLAR_RUB = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&rlz=1C5CHFA_enRU905RU905&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E+&aqs=chrome..69i57j0l3j0i131i433j0l3.5566j1j7&sourceid=chrome&ie=UTF-8"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'}

    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",","."))

    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "DFlfde SwHCTb", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(",","."))
        if currency >= self.current_converted_price + self.difference:
            print("Курс вырос пора валить")
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print("Курс упал пора назад")
            self.send_mail()
        print("Сейчас 1 доллар = " + str(currency))
        self.send_mail()
        time.sleep(3)
        self.check_currency()

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('sivan9458@gmail.com', 'sghtcsxvkfamescq')
        subject = 'Currency'
        body = 'cource changed'
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(
            'sivan9458@gmail.com',
            'sivan9458@gmail.com',
            message
        )
        server.quit()

currency = Currency()
currency.check_currency()