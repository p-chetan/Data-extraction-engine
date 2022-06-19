import datetime
import celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from scrapy import Selector
import numpy as np
import pandas as pd
import datetime
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from django.core.mail import EmailMessage
from django.conf import settings
from scraper.models import New, Buzz, PDF,Sche




@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=5))
def fintask():
    data = New.objects.get(id=id)
    name=data.name
    url=data.url
    DXpath=data.DXpath
    BXpath=data.BXpath
    email=data.email

    file_name = name + str(datetime.datetime.now())+'.csv'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver= webdriver.Chrome(options=chrome_options)
    driver.get(url)
    DXpath=int(DXpath)
 
    
    while True:
        try:
            html=driver.page_source
            soup=BeautifulSoup(html,'html.parser')
            list_of_table=pd.read_html(str(soup))
            dataframe= list_of_table[DXpath]
            df=pd.DataFrame(dataframe)

            df.to_csv(file_name, mode='a',header=False,index=False)
            print("file updated")  
            driver.find_element_by_xpath(BXpath).click()
            
        except  NoSuchElementException:
            print("last page")
            break
        
        except ElementClickInterceptedException:
            print(" ad intercepted ")
            #self.driver.close()

    a = pd.read_csv(file_name)
    df=a.to_html(classes='mystyle')

    subject = "Data of Finviz Screeners"
    message = "Hi,"
    email = email

    try:
        with open(file_name, "rb") as csvfile:
            email1 = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
            email1.attach(file_name, csvfile.read(), 'text/csv')
            print("\nSending email..")
            email1.send()
            print("Email sent successfully!")
        csvfile.close()
    except Exception as e:
        print("Sorry mail was not sent.")
    
