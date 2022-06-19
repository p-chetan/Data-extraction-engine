from __future__ import absolute_import, unicode_literals
import os
from re import A
from celery import Celery
from scrap import pandas_table_scraper1, pandas_table_scraper
from scrap import csv_kranshare

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrap.settings')
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
app = Celery('scrap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = BASE_REDIS_URL

@app.task()
def krane_krbn():
    holding="krbn_holdings"
    email="mmscrapers@gmail.com"
    krane_krbn=csv_kranshare.kraneshare(email,holding)

@app.task()
def krane_kcca():
    holding="kcca_holdings"
    email="mmscrapers@gmail.com"
    krane_kcca=csv_kranshare.kraneshare(email,holding)

@app.task()
def krane_keua():
    holding="keua_holdings"
    email="mmscrapers@gmail.com"
    krane_keua=csv_kranshare.kraneshare(email,holding)

@app.task
def kraneshares_kcca():  
    ip={
    "url":"https://kraneshares.com/kcca/",
    "file_name":"KCCA_Top_10_Daily_Report",
    "table_no":7,
    "bxpath":' ',
    "pages":1,
    "del_cols":[],
    "del_rows":[],
    "email":"varade1998@gmail.com"
    #"email":"mmscrapers@gmail.com"
    }

    kraneshares_kcca=pandas_table_scraper1.table_scraper(ip)
    kraneshares_kcca.genscraper()

@app.task
def kraneshares_keua():    
    ip={
    "url":'https://kraneshares.com/keua/',
    "file_name":"KEUA_Top_10_Holdings_Daily_Report",
    "table_no":7,
    "bxpath":' ',
    "pages":1,
    "del_cols":[],
    "del_rows":[],
    "email":"varade1998@gmail.com"
    #"email":"mmscrapers@gmail.com"
    }

    kraneshares_keua=pandas_table_scraper1.table_scraper(ip)
    kraneshares_keua.genscraper()

@app.task
def kraneshares_krbn():  
    ip={
    "url":'https://kraneshares.com/krbn/',
    "file_name":"KRBN_Daily_Report",
    "table_no":7,
    "bxpath":' ',
    "pages":1,
    "del_cols":[],
    "del_rows":[],
    "email":"varade1998@gmail.com"
    #"email":"mmscrapers@gmail.com"
    }

    kraneshares_krbn=pandas_table_scraper1.table_scraper(ip)
    kraneshares_krbn.genscraper()

@app.task
def dataroma_am():
    ip={
    "url":'https://www.dataroma.com/m/holdings.php?m=AM',
    "file_name":"AM_dataroma_Holdings",
    "table_no":0,
    "bxpath":' ',
    "pages":1,
    "del_cols":[0],
    "del_rows":[],
    #"email":"varade1998@gmail.com"
    "email":"mmscrapers@gmail.com"
    }

    dataroma_am=pandas_table_scraper1.table_scraper(ip)
    dataroma_am.genscraper()

@app.task
def dataroma_baupost():
    ip={
    "url":'https://www.dataroma.com/m/holdings.php?m=BAUPOST',
    "file_name":"BAUPOST_dataroma_Holdings",
    "table_no":0,
    "bxpath":' ',
    "pages":1,
    "del_cols":[0],
    "del_rows":[],
    #"email":"varade1998@gmail.com"
    "email":"mmscrapers@gmail.com"
    }

    dataroma_baupost=pandas_table_scraper1.table_scraper(ip)
    dataroma_baupost.genscraper()

@app.task
def dataroma_ffh():    
    ip={
    "url":'https://www.dataroma.com/m/holdings.php?m=FFH',
    "file_name":"FFH_dataroma_Holdings",
    "table_no":0,
    "bxpath":' ',
    "pages":1,
    "del_cols":[0],
    "del_rows":[],
    #"email":"varade1998@gmail.com"
    "email":"mmscrapers@gmail.com"
    }

    dataroma_ffh=pandas_table_scraper1.table_scraper(ip)
    dataroma_ffh.genscraper()

@app.task

def dataroma_psc():  
    ip={
    "url":'https://www.dataroma.com/m/holdings.php?m=psc',
    "file_name":"PSC_dataroma_Holdings",
    "table_no":0,
    "bxpath":' ',
    "pages":1,
    "del_cols":[0],
    "del_rows":[],
    #"email":"varade1998@gmail.com"
    "email":"mmscrapers@gmail.com"
    }

    dataroma_psc=pandas_table_scraper1.table_scraper(ip)
    dataroma_psc.genscraper()

@app.task

def dataroma_sam():
    ip={
    "url":'https://www.dataroma.com/m/holdings.php?m=SAM',
    "file_name":"SAM_dataroma_Holdings",
    "table_no":0,
    "bxpath":' ',
    "pages":1,
    "del_cols":[0],
    "del_rows":[],
    #"email":"varade1998@gmail.com"
    "email":"mmscrapers@gmail.com"
    }

    dataroma_sam=pandas_table_scraper1.table_scraper(ip)
    dataroma_sam.genscraper()

@app.task
def dataroma_managers():
    ip={
    "url":'https://www.dataroma.com/m/managers.php',
    "file_name":"managers_dataroma_Holdings",
    "table_no":0,
    "bxpath":' ',
    "pages":1,
    "del_cols":[],
    "del_rows":[],
    #"email":"varade1998@gmail.com"
    "email":"mmscrapers@gmail.com"
    }

    dataroma_managers=pandas_table_scraper1.table_scraper(ip)
    dataroma_managers.genscraper()

@app.task
def cathies_arkk():   
    ip={
    "url":'https://cathiesark.com/arkk/trades',
    "file_name":"ARKK_cathiesark",
    "table_no":0,
    "bxpath":'//*[@id="rc-tabs-0-panel-TRADES"]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4,
    "del_cols":[],
    "del_rows":[],
    #"email":"varade1998@gmail.com",
    "email":"mmscrapers@gmail.com"
    }

    cathies_arkk=pandas_table_scraper.table_scraper(ip)
    cathies_arkk.genscraper()

@app.task
def cathies_arkq():    
    ip={
    "url":'https://cathiesark.com/arkq/trades',
    "file_name":"ARKQ_cathiesark",
    "table_no":0,
    "bxpath":'//*[@id="rc-tabs-0-panel-TRADES"]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4,
    "del_cols":[],
    "del_rows":[],
    #"email":"varade1998@gmail.com",
    "email":"mmscrapers@gmail.com"
    }
    cathies_arkq=pandas_table_scraper.table_scraper(ip)
    cathies_arkq.genscraper()

@app.task
def cathies_arkf():
    ip={
    "url":'https://cathiesark.com/arkf/trades',
    "file_name":"ARKF_cathiesark",
    "table_no":0,
    "bxpath":'//*[@id="rc-tabs-0-panel-TRADES"]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4,
    "del_cols":[],
    "del_rows":[],
    "email":"mmscrapers@gmail.com"
    }
    cathies_arkf=pandas_table_scraper.table_scraper(ip)
    cathies_arkf.genscraper()

@app.task
def cathies_arkg():
    ip={
    "url":'https://cathiesark.com/arkg/trades',
    "file_name":"ARKG_cathiesark",
    "table_no":0,
    "bxpath":'//*[@id="rc-tabs-0-panel-TRADES"]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4,
    "del_cols":[],
    "del_rows":[],
    "email":"mmscrapers@gmail.com"    
    }
    cathies_arkg=pandas_table_scraper.table_scraper(ip)
    cathies_arkg.genscraper()

@app.task
def cathies_arkw():
    ip={
    "url":'https://cathiesark.com/arkw/trades',
    "file_name":"ARKW_cathiesark",
    "table_no":0,
    "bxpath":'//*[@id="rc-tabs-0-panel-TRADES"]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4,
    "del_cols":[],
    "del_rows":[],
    "email":"mmscrapers@gmail.com"    
    }
    cathies_arkw=pandas_table_scraper.table_scraper(ip)
    cathies_arkw.genscraper()

@app.task
def cathies_arkx():
    ip={
    "url":'https://cathiesark.com/arkx/trades',
    "file_name":"ARKX_cathiesark",
    "table_no":0,
    "bxpath":'//*[@id="rc-tabs-0-panel-TRADES"]/div[2]/div/div/div/ul/li[6]/button',
    "pages":4,
    "del_cols":[],
    "del_rows":[],
    "email":"mmscrapers@gmail.com"    
    }

    cathies_arkx=pandas_table_scraper.table_scraper(ip)
    cathies_arkx.genscraper()


