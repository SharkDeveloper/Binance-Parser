from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

headers = {
"cookie": "orioks_session=ab13391656fd1190f9b9eb52b1ae3007; _csrf=34e9fb8b4c9b9cb577d80faf0132b96a286d0b22ee6b86fca953a6f75eb6fa3aa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22l9yP4wBLkXx7DQ1Zax7zrkyTTUcUdjLf%22%3B%7D",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.787 Yowser/2.5 Safari/537.36"
}

headers_str = ""
for i in headers:
    headers_str += i+headers[i]+","
    

options = Options()
options.binary_location = "C:\\Users\\Valerian\\AppData\\Local\\Yandex\YandexBrowser\\Application\\browser.exe" #указываем путь до yandex
options.add_argument(headers_str)
WebDriver = webdriver.Chrome(chrome_options = options, executable_path=r'C:\\Users\\Valerian\Documents\\OneDrive\\Python\\Binance Parser\\chromedriver.exe') #путь до драйвера


try:
    url = "https://p2p.binance.com/ru/trade/TinkoffNew/RUB?fiat=RUB"
    url_login = "https://accounts.binance.com/ru/login?return_to=aHR0cHM6Ly93d3cuYmluYW5jZS5jb20vcnUvbXkvZGFzaGJvYXJk"
    url_search = "https://orioks.miet.ru/student/student/test?modID=91&kafID=33&idKM=1170605&debt=0"

    WebDriver.get(url_search)

    """data = WebDriver.find_element(By.XPATH,("//div[@class='css-8l9x78']"))
    print("--------------------")
    print(type(data))
    print("--------------------")"""
    time.sleep(500)
except Exception as ex: 
    print(ex)
finally:
    WebDriver.close()
    WebDriver.quit()
    
