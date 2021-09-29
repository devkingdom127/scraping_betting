# from django.http import HttpResponseRedirect
# from django.shortcuts import render, redirect
# from .models import *
# from django.contrib import messages
import os

# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import requests
from bs4 import BeautifulSoup
import time


def autologin(driver, url, username, password):
    driver.get(url)
    username_input = driver.find_element_by_name('UserName')
    username_input.send_keys(username)
    password_input = driver.find_element_by_name('Password')
    
    password_input.send_keys(password)
    user_input = input("Please pass captcha")
    driver.find_element_by_name("btnSubmit").click()
    
    return driver

def scrap(url):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install())

    USERNAME='kesley'
    PASSWORD='Aa6960014'    

    
    autologin(driver, url,
            USERNAME, PASSWORD)

    time.sleep(5)

    tables = driver.find_elements_by_class_name("table-horarios")
    results = []
  
    for table in tables:
        contents_tbody = table.find_elements_by_tag_name('tbody')# for td in table:
        
        for content_tbody in contents_tbody:
            tempResults = []
            elements_tr = content_tbody.find_elements_by_tag_name('tr')[:2]
            for element_tr in elements_tr:
                contents_td = element_tr.find_elements_by_tag_name('td')[1:-1]
                
                for i in reversed(range(len(contents_td))):
                    if len(tempResults) == 10:
                        break
                    txt = contents_td[i].text.replace("x", ",")
                    if(txt == ""):
                        continue
                    tempResults.append(txt)
        temp_1 = []            
        for str in tempResults:
            a = str.split(',')
            for i in range(len(a)):
                a[i] = int(a[i])
            temp_1.append(tuple(a))
        results.append(temp_1)
    print(results)

    scores = []
    for result in results:
        score = [0,0,0]
        for item in result:
            sum = float(item[0] + item[1])
            
            if sum==0:
                score[0] = score[0] + 1
            if 1.5 < sum < 2.5:
                score[1] = score[1] + 1
            if sum> 2.5:
                score[1] = score[1] + 1
                score[2] = score[2] + 1
        scores.append(score)        

    print (results)
    print (scores)
    

  
if __name__ == '__main__':
    url = "https://www.milionariotips.com.br/Home/CampeonatosHorarios"
    scrap(url)