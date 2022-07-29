from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import pandas as pd
import random
import numpy as np
from getpass import getpass




def runScript(keyword):
    try:
        options = ChromeOptions()
        #options.add_argument('--headless')
        driver = webdriver.Chrome('chromedriver.exe',options=options)
        driver.maximize_window()
        driver.get('https://www.instagram.com/')
        sleep(5)
        username = driver.find_element(By.XPATH,'//input[@name = "username"]')
        username.send_keys('worlddev7@gmail.com')
        password = driver.find_element(By.XPATH,'//input[@name = "password"]')
        password.send_keys('google@99')
        driver.find_element_by_xpath('//button[@type = "submit"]').click()
        sleep(5)
        driver.find_element(By.CLASS_NAME,'MTaRy').click()
        alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        alert2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        driver.find_element(By.CLASS_NAME,'jctW7').click()
        sleep(25)
        try:
            searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
            searchbox.clear()
            searchbox.send_keys(keyword)
            sleep(5) # Wait for 5 seconds
            my_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
            my_link.click()
        except:
            driver.get(f'https://www.instagram.com/explore/tags/{keyword[1:]}/')
        photo_urls = []
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True
        scroll_i = 0
        while scrolling:
            if scroll_i == 3:
                break

            photo_links = driver.find_elements(By.TAG_NAME,'a')
            
            link = [link.get_attribute('href') for link in photo_links if 'https://www.instagram.com/p/' in link.get_attribute('href')]
            for a in link:
                if a not in photo_urls:
                    photo_urls.append(a)
            scroll_attempt = 0
            while True:
                # check scroll position
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(4)
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    
                    # end of scroll region
                    if scroll_attempt >= 10:
                        scrolling = False
                        break
                    else:
                        sleep(3) # attempt another scroll
                else:
                    last_position = curr_position
                    break
            scroll_i += 1
        random.shuffle(photo_urls)
        photo_urls[:2]
        image_urls = []
        data = []
        for url in photo_urls[:40]:
            try:
                driver.get(url)
                sleep(3)
                urls = driver.find_element(By.CLASS_NAME,'_aagv').find_element(By.TAG_NAME,'img').get_attribute('srcset')
                alt = driver.find_element(By.CLASS_NAME,'_aagv').find_element(By.TAG_NAME,'img').get_attribute('alt')
                image_urls.append(urls)
                urls = urls.split(',')[0]
                
                
                text = driver.find_element(By.CLASS_NAME,'_aasx').text.split('\n')
                hastags = []
                for hashtag in text:
                    if '#' in hashtag:
                        hastags.append(hashtag)
                
                likes = ''
                username = ''
                caption = ''    
                try:
                    likes = text[0]
                except:
                    likes = ''
                try:
                    username = text[1]
                except:
                    username = ''
                try:
                    caption = text[2]
                except:
                    caption = ''
                try:
                    timeago = text[5]
                except:
                    timeago = ''
                
                
                dicts = {'likes':likes,'username':username,'caption':caption,'hastag':hastags,'timeago':text[-2]}
                k = {}
                k["alt"] = alt
                k["image_url"] = urls
                k["text_data"] = dicts
                data.append(k)  
            except:
                pass
        x = pd.DataFrame(data)
        filter = x['image_url'] != ''
        x = x[filter]
        x.image_url= x.image_url.apply(lambda x: x.split(' ')[0])
        x.to_csv('calldata.csv')
    except Exception as e:
        print(e)
        #driver.close()