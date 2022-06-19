from os import lseek
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException


class table_scraper:
    def __init__(self,ip):
        self.url=ip["url"]
        self.file_name=ip["file_name"]
        self.table_no=ip["table_no"]
        self.bxpath=ip["bxpath"]
        self.pages=ip["pages"]
        self.del_rows=ip["del_rows"]
        self.del_cols=ip["del_cols"]        
  
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

    def get_date(self):
        today =date.today()
        d_date= today.strftime("%Y-%m-%d")
        return (d_date)

    def write_file(self,fname,df):
        
        with open(fname+'.csv', 'a') as f:
            df.to_csv(f, mode='a', header=f.tell()==0,index=False,na_rep=' ')
            
    def mail(self,fname):
        subject = self.file_name
        message = ''
        email = "varade1998@gmai.com"
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

        return "Done"
        
    def genscraper(self):
        driver= webdriver.Chrome()
        driver.get(self.url)
        counter=0
        while (counter<self.pages):
            try:                
                html=driver.page_source
                df=self.extract_df(html,self.table_no)
                date1=self.get_date()
                fname=self.file_name+date1
                self.write_file(fname,df)
                

                driver.find_element_by_xpath(self.bxpath).click()
                counter+=1
                print("next clicked")

            except  NoSuchElementException:
                print("last page")
                return
            
            except ElementClickInterceptedException:
                print(" ad intercepted ")
                return
        

'''def main():


    ip={
    "url":"https://cathiesark.com/arkk/trades",
    "file_name":f"'Cathies ark '{str(datetime.datetime.now())}",
    "table_no":0,
    "bxpath":'/html/body/div/div/section/main/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4
    }

    cathiesark=table_scraper(ip)
    cathiesark.genscraper()

main()'''
