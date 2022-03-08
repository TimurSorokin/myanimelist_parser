import urllib.robotparser
import requests
import json
import xml.etree.ElementTree as ET
import os.path
from bs4 import BeautifulSoup as BS
from threading import Thread
import datetime
class Scrapper: 
    def __init__(self,year,season):
        self.__json = f"{year}{season}.json"
        self.__url = f'https://myanimelist.net/anime/season/{year}/{season}'
        self.__headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0','Accept-Language':'es','Accept-Encoding':'gzip, deflate','Accept':'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Refer':'null'}
        self.__data_set = []
        self.__data_extrator = Thread(target=self.__build_data_set,args=())     

    def __get_response_data(self):
        response = requests.get(self.__url,headers=self.__headers)
        return response
    def __build_data_set(self):
        response = self.__get_response_data()
        data_set=[]
        if(response.status_code==200):
            soup = BS(response.text,'html.parser')
            list_div = soup.find_all('div',{'class':'seasonal-anime'})
            #Get Anime title, date, episodes, time and tags
            count = 0
            for div in list_div:
                title = div.find('a',{'class':'link-title'})
                #Title
                if(title!=None):
                    data ={}
                    data.update({"title":title.text})
                    #Info: date,num episodes, duration
                    info = div.find('div',{'class':'info'})
                    info_array = []
                    for value in info:
                        if not value.text.isspace():
                            val = value.text.replace(' ','').replace('\n',r'')
                            info_array.append(val)
                    data.update({"info":info_array})
                     #Tags: Categories
                    tags = div.find('div',{'class':'genres-inner'})
                    categories_list = []
                    for tag in tags:
                        if not tag.text.isspace():
                            category = tag.text.replace(' ','').replace('\n','')
                            categories_list.append(category)
                    data.update({"tags":categories_list})
                    #Rating
                    rate = div.find('div',{'class':'score'})
                    r = rate.text.replace(' ','').replace('\n',r'')
                    #Parsing values
                    try:
                        rating = float(r)
                    except:
                        rating = 'N/A'
                    data.update({"rating":rating})
                data_set.append(data)
                count+=1
        else:
            print("Something went wrong while parsing html...")
        self.__data_set = data_set
    def process_data(self): 
        self.__data_extrator.start()  
    def get_data(self):
        self.__data_extrator.join()
        return self.__data_set
    def export(self,data):
        with open(self.__json,'w') as output:
            json.dump(data,output,indent=2)

