import pandas as pd
import io
import requests
from datetime import date
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings

def kraneshare(email,holding):
    holdings=holding
    date_format="%m_%d_%Y"
    file_datefm="%Y_%m_%d"
    fname=f"{holdings}_Consolidated.csv"


    today= date.today()# get today's date
    yesterday= today -timedelta(days=1)
    today1=yesterday.strftime(date_format)# convert date to string fromat for the url.
    opdate=today.strftime(file_datefm)# convert date to string fromat for the file name.
    attchment=f"{holdings}_{opdate}.csv"
    s= requests.session()  #create a session
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}  
    url=f'https://kraneshares.com/csv/{today1}_{holdings}.csv'
    download = s.get(url,headers=headers).content #get the content of csv file

    df=pd.read_csv(io.StringIO(download.decode('utf-8')),skiprows=[0]) #get download into dataframe
    print(df)
    df.insert(loc=0, column='date', value=today1)

    with open(fname, 'a') as f:
                df.to_csv(f, mode='a', header=f.tell()==0,index=False,na_rep=' ')

    subject = fname
    message = ''
    email = email
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
    