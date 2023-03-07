import os
from env import *
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import csv

# this flow it may only works for courses enrollments
class MainActivity():

    def main():
        # create an HTML Session object
        asession = AsyncHTMLSession()
        url = 'https://auth.dio.me/realms/master/protocol/openid-connect/auth?client_id=spa-core-client&redirect_uri=https%3A%2F%2Fweb.dio.me%2F&state=cafdcd34-7704-4d02-b7e4-273d5be76329&response_mode=fragment&response_type=code&scope=openid&nonce=6db3188b-a107-4771-87b6-e13f5831828b'
        url_play = 'https://web.dio.me/play'
        # here it is the link with the filter of the programs/courses that I want
        # this one includes front-end, back-end, plus cloud courses
        url_play_with_filters = 'https://web.dio.me/play?career=9f3d4f16-ef54-412e-9156-38482e2d51a3&career=1b73eec2-c27b-4820-8e79-8238c93a5224&career=b87ed61c-d967-4a9b-a2ca-08dafcbf4785&tab=programas'
        url_track_base = "https://web.dio.me/track/"
        

        # ///  Chrome session
        chromeOptions = webdriver.ChromeOptions()

        driver = webdriver.Chrome(executable_path='/home/drew/Área de Trabalho/Andrew/selenium_python_scrapper_tdc/chromedriver', options=chromeOptions)
        driver.get(url)
        #set timeout for await any object/element that I may want to
        timeout = 30
        time.sleep(3)
       
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, 'username')))
        except TimeoutException:
            driver.quit()

        input_email = driver.find_element(By.ID,'username')
        input_email.send_keys(EMAIL_DIO)

        time.sleep(2)

        input_pass = driver.find_element(By.ID,'password')
        input_pass.send_keys(PASSWORD_DIO)

        time.sleep(1)
        proceed_button = driver.find_element(By.ID,'kc-login')
        proceed_button.click()
        time.sleep(5)
        
        try:
            play_button = driver.find_element(By.XPATH,'//span[text()="Play"]')
            play_button.click()
        except:
            driver.get(url_play_with_filters)
      
        time.sleep(7)
        # here you must check before running it. This may change 
        CLASS_IMG_TAG = "sc-dcvren"
        lista_raw = (driver.find_elements(By.CLASS_NAME, CLASS_IMG_TAG))
        lista = []
        for item in (lista_raw):
           lista.append(item.get_attribute("alt"))
        course_count = 0
        
        for course in (lista):
            time.sleep(5)
            print(course)
            
            driver.get(url_track_base+course)
            time.sleep(5)
                
            enroll_button = driver.find_element(By.CLASS_NAME,'sc-kjMGqw')
            
            if (('matrícula' in enroll_button.text.lower()) == False):
                course_count+=1
                print('matriculado ja em '+course )
                continue
            else:
                
                enroll_button.click()
                time.sleep(10)
                url_after = driver.current_url
                try:
                    #print(url_after)
                    #print((url_after.find('course')!= -1))
                    if (('confirmation' in url_after) == False):
                        course_count+=1
                        print('matriculado ja em '+course )
                        continue
                    else:
                        driver.execute_script("window.scrollTo({ left: 0, top: document.body.scrollHeight, behavior: 'smooth' });")
                        time.sleep(1)
                        while (url_after.find('confirmation')!= -1):
                            time.sleep(1)
                            driver.execute_script("window.scrollTo({ left: 0, top: document.body.scrollHeight, behavior: 'smooth' });")
                            time.sleep(2)
                            try:
                                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,'//button[text()="AVANÇAR"]')))
                                step_button = driver.find_element(By.XPATH,'//button[text()="AVANÇAR"]')
                            except:
                                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME,'px-4')))
                                step_button = driver.find_element(By.CLASS_NAME, 'px-4')

                            driver.execute_script("window.scrollTo({ left: 0, top: document.body.scrollHeight, behavior: 'smooth' });")
                            time.sleep(1)
                            step_button.click()
                            time.sleep(3)
                            url_after = driver.current_url
                       
                        time.sleep(3)
                        if(url_after.find('course')!= -1):
                            course_count+=1
                            print('matricula '+course )
                            
                except Exception as e:
                    print(e)
                    pass
       
        print('cursos matriculado '+ str(course_count))
        print('rotina finalizada.')
   
        driver.quit()

class MyMain():
    ui = MainActivity
    ui.main()
       
if __name__ == "__main__":
    MyMain()
    





