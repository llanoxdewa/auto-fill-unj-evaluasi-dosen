#!\llano\python\web-scraping-bsoup\.env/Scripts/python

from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
os.environ['WDM_LOG'] = 'false' 
logging.getLogger('WDM').setLevel(logging.NOTSET)

# for explicity wait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import TimeoutException

# utils


class WebDriver(object):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = r"C:\Users\Lenovo\AppData\Local\Google\Chrome\Application\chrome.exe"
    chrome_options.add_experimental_option('detach',True)
    chrome_options.add_argument("--log-level=OFF")    



    # open driver connection
    def __init__(self,url):
        self.driver = webdriver.Chrome(options=self.chrome_options,service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5) # 10 for very lag network
        self.url = url

    
    # close driver connection
    def __del__(self):
        self.driver.quit()

    def headless(self,yes):
        if yes:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')   


    def run(self):
        print(f'fetching url: {self.url}')
        self.driver.get(self.url)


    @staticmethod
    def target_url(url: str):
        
        def base_page_class(cls):
     
            default_init = cls.__init__     

            def new_init(self, *args, **kwargs):
                default_init(self, url = url,*args, **kwargs)

            cls.__init__ = new_init

            return cls

        return base_page_class 