
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from .web import WebDriver 
from .constants import (
    EVENTS_MAP
)

class BasePage(WebDriver):

    def handle_alert(self,message: str = ''):

        try:
            WebDriverWait(self.driver,10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            if message != '':
                alert.send_keys(message)
            alert.accept() 
        except Exception as e:
            print(e)
            print("[WebDriverWait]: TIMEOUT!, alert tidak ditemukan")
            pass

    def wait_for_it(self,ec,locator: tuple[By, str] | WebElement,time: int = 10):
        try: 
            waiter = EVENTS_MAP.get(ec,None)

            if waiter == None:
                raise Exception(f'expected condition ({str(ec)}) not found')            

            target = WebDriverWait(self.driver,time).until(waiter(locator))
            return target
        except Exception as e:
            print(e)
            print(f"[WebDriverWait]: timeout!, element with {locator[1]} couldn't be found")

        return None

    
    def into_view(self,we: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", we) 

    def find(self,by: By,location: str):
        return self.driver.find_element(by,location)

    def finds(self,by: By,location: str):
        return self.driver.find_elements(by,location)

    def wait_for_prop_change(self,locator: tuple[By,str] | WebElement,prop_name: str,expected_value: str,time: int = 10,custom_condition=None):
        
        class PropEquals:
            def __init__(self,element):
                self.element = element

            def __call__(self,_):
                current_prop_val = self.element.get_attribute(prop_name) 
                ev = expected_value(current_prop_val) if callable(expected_value) else expected_value                

                return custom_condition(current_prop_val,ev) if custom_condition else current_prop_val == ev 

        
        target_element = locator if isinstance(locator,WebElement) else self.find(*locator)

        try:
            WebDriverWait(self.driver,time).until(
                PropEquals(target_element)      
            )
        except Exception as e :
            print(e)
            print("[WebDriverWait]: TIMEOUT!!, element with such prop and value didn't found")



    def wait(self,long: int):
        import time
        time.sleep(long)

    def reload(self):
        self.driver.refresh()


class Element(object):

    def __get__(self, obj, _):

        driver = obj.driver
        try:
            # element = WebDriverWait(driver, 15).until(lambda driver: driver.find_element(*self.locator))
            waiter = EVENTS_MAP.get(self.wait_until,None)

            if waiter == None:
                raise Exception(f'Expected Condition ({self.wait_until}) not define')             

            element = WebDriverWait(driver, 15).until(waiter(self.locator))
            return element
        except Exception as e:
            print(e)
            print(f"[WebDriverWait]: timeout!, element with {self.locator[1]} couldn't be found")

        return None


