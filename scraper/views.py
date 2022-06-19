from logging import exception
from django import forms
from django.shortcuts import redirect, render, HttpResponse
from pandas.core.base import DataError
from scraper.models import New, Buzz, PDF,Sche
from django.views import View
from django.http import JsonResponse, response
import json
import csv
import sys
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from scrapy import Selector
import numpy as np
import pandas as pd
from django.contrib.auth.models import User
import datetime
from pathlib import Path
from django.contrib import messages
from .forms import InvestwithBuzz, PdfForm,SignupForm,EditScrap,Schedule
from django.core.mail import EmailMessage
from django.conf import settings
import tabula 
from bs4 import BeautifulSoup




#Create your views here.
def index(request):
    #return HttpResponse("this is home page")
    return render(request,'index.html')

def finviz(request):
  
    return render(request,'finviz.html')

def newO(request):
    if request.method == "POST":
        name = request.POST.get('name')
        url = request.POST.get('url')
        DXpath = request.POST.get('DXpath')
        BXpath = request.POST.get('BXpath')
        email= request.POST.get('email')

        new = New(user_id=request.user,name=name, url=url, DXpath=DXpath, BXpath=BXpath,email=email)
        new.save()

    file_name = 'name' + str(datetime.datetime.now())+'.csv'
    
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

    a = pd.read_csv(file_name)
    df=a.to_html(classes='mystyle', border=3)

    subject = "Data of Finviz Screeners"
    message = "Hi, \nPlease find the attached csv containing  of Finviz site."
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
        
    return render(request,'newO.html',{'table':df})

def json(request):
    
    data = list(New.objects.values())
    data=list.pop(data)
    if "id" in data:
        del data["id"]
    return JsonResponse(data, safe=False)

def search(request):
    nm=request.POST['search']
    obj=New.objects.filter(name=nm) 
    return render(request,'search.html',{'obj':obj})


def store(request):
    data=New.objects.all().values().order_by('-id')
    return render(request,'store.html',{"data":data})

def storepdf(request):
    data=PDF.objects.all().values().order_by('-id')
    return render(request,'storepdf.html',{"data":data})

def storebuzz(request):
    data=Buzz.objects.all().values().order_by('-id')
    return render(request,'storebuzz.html',{"data":data})

def about(request):
    return render(request,'about.html')

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render (request, 'signup.html', {'form':form}) 
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Sign Up Successfully...')
            form.save()
        return render (request, 'signup.html', {'form':form}) 
    
def profile(request):
    return render(request, 'profile.html')


def edit(request,id):
    obj = New.objects.get(id=id)
    Edit = EditScrap(instance=obj)
    if request.method=='POST':
        form = EditScrap(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Scraper has been updated')

            return redirect('/store')
    return render(request, 'edit.html', {'edited':Edit})
    
def editbuzz(request,id):
    obj = Buzz.objects.get(id=id)
    Edit = InvestwithBuzz(instance=obj)
    if request.method=='POST':
        form = InvestwithBuzz(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Scraper has been updated')

            return redirect('/storebuzz')
    return render(request, 'edit.html', {'edited':Edit})

def editpdf(request,id):
    obj = PDF.objects.get(id=id)
    Edit = PdfForm(instance=obj)
    if request.method=='POST':
        form = PdfForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Scraper has been updated')

            return redirect('/storepdf')
    return render(request, 'edit.html', {'edited':Edit})

        
def delete(request,id):
    obj1 = New.objects.get(id=id)
    obj1.delete()
    messages.success(request,'Scraper has been deleted')
    return redirect("store")

def deletebuzz(request,id):
    obj = Buzz.objects.get(id=id)
    obj.delete()
    messages.success(request,'Scraper has been deleted')
    return redirect("storebuzz")

def deletepdf(request,id):
    obj = PDF.objects.get(id=id)
    obj.delete()
    messages.success(request,'Scraper has been deleted')
    return redirect("storepdf")



def apply(request,id):
    df=fin(request,id)
    return render(request,'newO.html',{'table':df})

def applybuzz(request,id):
    df=buzzinv(request,id)
    return render(request, 'newO.html',{'table': df})  

def applypdf(request,id):
    df=pdfapp(request,id)
    return render(request, 'newO.html',{'table': df})  


def Invest(request):
    form = InvestwithBuzz()
    #if form.is_valid():
    #    form.save()
    #context={'form':form}
    return render(request, 'Invest.html',{'form':form})

def buzz(request):
    if request.method == 'POST':
        scraper_name= request.POST.get('name')
        click_b=request.POST.get('BXpath')
        url=request.POST.get('url')
        xp=request.POST.get('DXpath')
        n_col= request.POST.get('col')
        email= request.POST.get('email')

        new = Buzz(user_id=request.user,name=scraper_name, url=url, DXpath=xp, BXpath=click_b, col=n_col,email=email)
        new.save()

        file_name = scraper_name+str(datetime.datetime.now())+'.csv'
        n_col=int(n_col)

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        driver= webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.find_element_by_xpath(click_b).click()

        sel = Selector(text =driver.page_source)
        data=sel.xpath(xp).extract()
        num= np.array(data)
        tab = num.reshape(-1,n_col)

        df= pd.DataFrame(tab)
        file_name = scraper_name+str(datetime.datetime.now())+'.csv'

        df.to_csv(file_name, mode='a')
        
        b = pd.read_csv(file_name)
        df=b.to_html(classes='mystyle',border=3)
 
        subject = "Scraper for Invest With Buzz"
        message = "Hi, \nPlease find the attached csv containing list of Invest with Buzz site."
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
            
        return render(request, 'newO.html',{'table': df})  


def pdf(request):
    f = PdfForm()

    return render(request, 'pdf.html',{'form':f})

def pdf1(request):
    if request.method == 'POST':
        scraper_name= request.POST.get('name')
        url=request.POST.get('url')
        pgs= request.POST.get('pages')
        email= request.POST.get('email')
        new = PDF(user_id=request.user,name=scraper_name, url=url, pages=pgs ,email=email)
        new.save()
        file_name = scraper_name+str(datetime.datetime.now())+'.csv'
      
        df= tabula.read_pdf(url,pages=pgs)
        obj=tabula.read_pdf(url,pages=pgs,multiple_tables=True)
        for ob in obj:
            print(ob)

            df1=ob.to_html(classes='mystyle',border=3)

        tabula.convert_into(url,file_name,output_format="csv",pages=pgs)

        subject = "Scraper Data of PDF"
        message = "Hi, \nPlease find the attached csv containing list of pdf scraper."
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
      
        
        return render(request, 'newO.html',{'table':df1})  

    
def schedule1(request,id):
    obj = New.objects.get(id=id)
    ob=Sche.objects.get()
    sche = Schedule(instance=ob)
    if request.method=='POST':
        form = Schedule(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Scraper has been updated')

            return redirect('/store')
    
    return render(request, 'schedule1.html', {'sc':sche})
    
def fin(request,id):
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
    
    return df

def buzzinv(request,id):
    data = Buzz.objects.get(id=id)
    scraper_name=data.name
    url=data.url
    xp=data.DXpath
    click_b=data.BXpath
    n_col=data.col
    email=data.email

    file_name = scraper_name+str(datetime.datetime.now())+'.csv'
    n_col=int(n_col)

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver= webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.find_element_by_xpath(click_b).click()

    sel = Selector(text =driver.page_source)
    data=sel.xpath(xp).extract()
    num= np.array(data)
    tab = num.reshape(-1,n_col)

    df= pd.DataFrame(tab)
    file_name = scraper_name+str(datetime.datetime.now())+'.csv'

    df.to_csv(file_name, mode='a')
    
    b = pd.read_csv(file_name)
    df=b.to_html(classes='mystyle',border=3)

    subject = "Scraper for Invest With Buzz"
    message = "Hi, \nPlease find the attached csv containing list of Invest with Buzz site."
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
        
    return df

def pdfapp(request,id):
    data = PDF.objects.get(id=id)
    scraper_name=data.name
    url=data.url
    pgs=data.pages
    email=data.email

  
    file_name = scraper_name+str(datetime.datetime.now())+'.csv'
    
    df= tabula.read_pdf(url,pages=pgs)
    obj=tabula.read_pdf(url,pages=pgs,multiple_tables=True)
    for ob in obj:
        print(ob)

        df1=ob.to_html(classes='mystyle',border=3)

    tabula.convert_into(url,file_name,output_format="csv",pages=pgs)

    subject = "Scraper Data of PDF"
    message = "Hi, \nPlease find the attached csv containing list of pdf scraper."
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
    
        return df1


def naming(request):
    return render(request,'naming.html')