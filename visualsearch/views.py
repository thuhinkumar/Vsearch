from django import forms
from .forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import datetime 
import urllib.request, urllib.error, urllib.parse
from urllib.request import Request, urlopen 
import html2text #turn html into ASCII text
from bs4 import BeautifulSoup
import sys
from unidecode import unidecode 
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import textract
import nltk
import re
from nltk.corpus import stopwords
from rake_nltk import Rake, Metric
import concurrent.futures # threading
import time
import random 


def Main(request): 
    search_form = Search(request.POST)
    if search_form.is_valid(): 
        query= request.POST['search_form']
        try: 
            from googlesearch import search 
        except ImportError:  
            print("No module named 'google' found") 
            
        all_key_words = []
        results= []
        images= []
        request.session['search']=random.randint(0,100000) 
        for result in search(query, tld="COM", num=10, stop=10, pause=2): 
            # Ignore converting links from HTML
            #url=result
            print(result)
            results.append(result) 
            response = Request(result, headers={'User-Agent': 'Mozilla/5.0'})
            webContent = urlopen(response).read()
            h= html2text.HTML2Text() 
            h.ignore_links=  True 
            h.ignore_images= True 
            text= h.handle(unidecode(str(webContent,errors='ignore')))
            #print(re.sub('[*#@$-]','', unidecode(text)))  
            print('hello1')
        # nlp 
            text = re.sub("[^0-9a-zA-Z]+"," ",text)# removes non-alphanumeric characters
            r = Rake(max_length = 2,ranking_metric=Metric.WORD_DEGREE)
            r.extract_keywords_from_text(text)
            key_words = r.get_ranked_phrases()
            # print('key_words='+str(key_words))
            try: 
                all_key_words.append(key_words[0]) # num of keywords per query
            except: 
                pass
        print('hello2')
        print("all_kws",all_key_words) # takes two most relevent terms for each
        #image search
        d = webdriver.Chrome(executable_path='/home/alisher/Desktop/Projects/IB/Drivers/chromedriver')
        def waits(time,xpath): 
            try:
                element = WebDriverWait(d, time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            except: 
                print("error occured")
                pass 
        for num,word in enumerate(all_key_words):
            d.get('https://duckduckgo.com/?q='+word+'&t=h_&iax=images&ia=images') 
            waits(3,'/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/span/img')
            img= d.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/span/img')
            src= img.get_attribute('src')
            images.append(src) 
        display={} 
        for i in range(10): 
            try: 
                display[results[i]]=images[i]
            except: 
                pass
        print(display)
        d.close() 
        print(results)
        print(images) 
        return render(request, 'results.html', {'display':display})

    return render(request, 'home.html', {'form': search_form})




# Create your views here.
