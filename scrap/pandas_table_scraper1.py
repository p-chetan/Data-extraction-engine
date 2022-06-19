from os import lseek
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from django.core.mail import EmailMessage
from django.conf import settings
from sqlalchemy import create_engine
from selenium.webdriver import FirefoxOptions
import sqlite3
today = date.today()

class table_scraper:
    def __init__(self,ip):
        self.url=ip["url"]
        self.file_name=ip["file_name"]
        self.table_no=ip["table_no"]
        self.bxpath=ip["bxpath"]
        self.pages=ip["pages"]
        self.del_rows=ip["del_rows"]
        self.del_cols=ip["del_cols"]  
        self.email=ip["email"]      
  
    def extract_df(self,html,table_no):
        soup=BeautifulSoup(html,'html.parser')
        list_of_table=pd.read_html(str(soup))
        dataframe= list_of_table[table_no]
        df=pd.DataFrame(dataframe)
        df=df.dropna(how='all') 
        df=df.dropna(axis=1,how='all')
        df=df.drop(df.columns[self.del_cols],axis=1)
        df=df.drop(df.index[self.del_rows])
        return(df)
        
    def d_b(self,df):
        df.insert(0,"Date",True )
        df['Date']=today
        engine = create_engine('sqlite:///finmarka.db', echo=True)
        sqlite_connection = engine.connect()
        sqlite_table = self.file_name
        df.to_sql(sqlite_table, sqlite_connection,index_label='id',if_exists='append')
        sqlite_connection.close()
            

    def get_date(self):
        today =date.today()
        d_date= today.strftime("%Y-%m-%d")
        return (d_date)

    def write_file(self,fname,df):
        
        with open(fname, 'a') as f:
            df.to_csv(f, mode='a', header=f.tell()==0,index=False,na_rep=' ')
            
    def mail(self,fname):
        subject = self.file_name
        message = ''
        email = self.email
        try:
            with open(fname, "rb") as csvfile:
                email1 = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                email1.attach(fname, csvfile.read(), 'text/csv')
                print("\nSending email..")
                email1.send()
                print("Email sent successfully! ")
                print(email)
            csvfile.close()

        except Exception as e:
            print("Sorry mail was not sent.")            
        
    def genscraper(self):
        opts = FirefoxOptions()
        opts.add_argument('--headless')
        driver = webdriver.Firefox(options=opts)
        driver.get(self.url)
        counter=0
        while (counter<self.pages):
            try:
                
                html=driver.page_source
                df=self.extract_df(html,self.table_no)
                date1=self.get_date()
                fname=self.file_name+date1+'.csv'
                self.write_file(fname,df)
                self.d_b(df)
                
                driver.find_element_by_xpath(self.bxpath).click()
                counter+=1

            except  NoSuchElementException:
                print("last page")
                break

            except ElementClickInterceptedException:
                print(" ad intercepted ")
                break

        driver.close()
        self.mail(fname)
        

        return "Done"
  
