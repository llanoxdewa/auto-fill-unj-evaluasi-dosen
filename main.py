#!\llano\selenium\projek-selenium\eval-dosen\.venv/Scripts/python

from selenium.webdriver.support.ui import Select
import time 
from helper import Logging
import re
from selenium.webdriver.common.by import By
from webotopy.page import (
    BasePage,
    WebDriver
)
from webotopy.constants import Events
from helper import Data
from helper import (
    InvalidDataException,
    InvalidLoginProcess,
    InvalidFillDosenEvaluation,
    InvalidMoveToKHSPage,
    InvalidSelectSemesterAndShowingKhs,
    InvalidProcessException
)


@WebDriver.target_url(url='https://siakad.unj.ac.id/')
class SiakadUNJ(BasePage,Data):

    def login(self):
        
        try:
            username = self.find(By.ID,'username') 
            password = self.find(By.ID,'password') 
            stupid_security_question = self.find(By.CLASS_NAME,'security-field')
            security_input_field = self.find(By.ID,'security') 
            login_button = self.find(By.CSS_SELECTOR,'button[type="submit"]')

            Logging.info('*** INPUT USERNAME DAN PASSWORD 🔃')
            try:
                username.send_keys(self.username)
                password.send_keys(self.password)
            except:
                raise Exception('input username dan password gagal ❌') 
                

            Logging.success('*** INPUT USERNAME DAN PASSWORD BERHASIL ✔')

            
            Logging.info('*** BYPASS SECURITY 👩‍💻')
            try:
                math_pattern_re = re.compile(r'\d+\+\d+')
                math_question = stupid_security_question.text 
                math_pattern = math_pattern_re.search(math_question)

                if math_pattern:
                    security_input_field.send_keys(eval(math_pattern.group(0)))
                    Logging.success('*** PROSES BYPASS SECURITY SUCCESS ✔')

            except:
                raise Exception('*** PROSES BYPASS SECURITY GAGAL ❌')

            # press the login button
            if login_button:
                login_button.click()
                # check if the username and password correct
                try:
                    self.find(By.CSS_SELECTOR,'div[class="alert alert-block alert-success"]')
                    Logging.success('*** LOGIN BERHASIL ✔')
                except:
                    raise Exception('username / password salah')
            else:
                raise Exception('*** LOGIN BUTTON NOT FOUND ❓')
            

        except Exception as e:
            print(e)
            raise InvalidLoginProcess(str(e))



    def move_to_khs_page(self):
        try:
            academic_dropdown_link = self.find(By.CSS_SELECTOR,'li:nth-child(5)')        
            academic_dropdown_link.click()

            khs_link_page = self.find(By.CSS_SELECTOR,'li:nth-child(5) ul li:nth-child(3)')        
            khs_link_page.click()
        except Exception as e:
            print(e)
            raise InvalidMoveToKHSPage('move to khs page is failed')

    def select_semester_and_showing_khs(self) -> None:
        try:
            sms_select = self.wait_for_it(Events.CLICKABLE,(By.ID,'kodeSMS'))
            sms_select.click()
            mewing_data = self.find(By.ID,'btnShowingData')

            semesters = Select(sms_select)
            semesters.select_by_value(str(self.semester))

            mewing_data.click()
        except Exception as e:
            print(e)
            raise InvalidSelectSemesterAndShowingKhs('selecting semester failed')

    def all_good_for_dosen(self) -> None:

        ## FAILED BECAUSE ITS SUCK
        # ek_buttons = self.find(By.CSS_SELECTOR,'button[id^="evaluasiKuliah_"]')        
        # for ek_button in ek_buttons:
        #     ek_button.click()
        #     ek_modal = self.find(By.ID,'modalEvaluasiKuliah')
            
        #     choices = ek_modal.find_elements(By.CSS_SELECTOR,f'input[type="radio"][name^="nilai_"][value="4"]')

        #     for choice in choices:
        #         self.into_view(choice)
        #         time.sleep(0.5)
        #         choice.click()

        #     save_button = self.find(By.ID,'btnSimpan')
        #     close_button = self.find(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[7]/div[2]/div[2]/div/div[3]/button[1]')
        #     close_button.click()
        #     # self.handle_alert()

        #     self.reload()
        #     self.select_semester_and_showing_khs(121)
        #     self.wait(1)

        try:
            while True: # while the evaluasi button is found
                try:
                    ek_button = self.find(By.CSS_SELECTOR,'button[id^="evaluasiKuliah_"]')        
                except: 
                    # if the evaluasi dosen sudah terisi semua
                    Logging.info("*** TIDAK ADA LAGI EVALUASI YANG PERLU DI ISI")
                    break    

                ek_button.click()
                ek_modal = self.find(By.ID,'modalEvaluasiKuliah')
                    
                choices = ek_modal.find_elements(By.CSS_SELECTOR,f'input[type="radio"][name^="nilai_"][value="{self.nilai_evaluasi_dosen}"]')

                for choice in choices:
                    self.into_view(choice)
                    self.wait(0.5) # less than 500ms, it will break
                    choice.click()

                save_button = self.find(By.ID,'btnSimpan')
                # close_button = self.find(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[7]/div[2]/div[2]/div/div[3]/button[1]') # for debugging purpose only
                save_button.click()
                self.handle_alert() # when the save button click, this must be execute

                self.reload()
                self.select_semester_and_showing_khs()
        except Exception as e:
            print(e)
            raise InvalidFillDosenEvaluation('something wrong happen when fil the evaluation dosen')


if __name__ == '__main__':

    try: # main try and catch
 
        siakad = SiakadUNJ()
        
        siakad.init_data('./data.json')
        siakad.validate_information()
            
        siakad.run()
        siakad.login()
        siakad.move_to_khs_page()
        siakad.select_semester_and_showing_khs()
        siakad.all_good_for_dosen()
        
    except InvalidDataException as DE: 
        print(DE)
    except InvalidProcessException as PE: 
        print(PE) 

    Logging.info('*** EVALUASI DOSEN TELAH SELESAI')
    time.sleep(3)

