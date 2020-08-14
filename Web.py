import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

class Web:
    def __init__(self):
        self.url = ""

    def openWeb(self):
        self.driver = webdriver.Chrome(executable_path = r"C:\Windows\chromedriver84.exe", chrome_options = self.chrome_opt())
         #ChromeDriverManager().install(),
        return self.driver
                                
    def chrome_opt(self):
        option = Options()
        option.add_argument("--disable-notifications")
        option.add_argument("--start-maximized")
        return option

    def bs(self):
        return BeautifulSoup(self.driver.page_source, features="html.parser")

    def enter(self, box, info):
        box.send_keys(info)
        time.sleep(0.2)

    def click(self, button):
        button.click()
        time.sleep(0.5)