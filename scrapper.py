import urllib.robotparser
import requests
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS
from informer import Informer 
from threading import Thread
import datetime
class Scrapper: 
    def __init__(self,year,season):
        self.__info = Informer()
        self.__info.inform(0,f'Received values: {season} {year}')
        is_valid = self.__check_input(season,year)
        if is_valid == False:
            self.__info.inform(2,f'Invalid input: {season} {year} Status: {is_valid}')
            exit()
        self.__json = f"{year}-{season}.json"
        self.__url = 'https://myanimelist.net/anime/season/'+str(year)+'/'+season
        self.__headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0','Accept-Language':'es','Accept-Encoding':'gzip, deflate','Accept':'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Refer':'null'}
        self.__data_set = None
        self.__data_extrator = Thread(target=self.__build_data_set,args=())
    
    def __check_input (self,season,year):
        season_list = ['winter', 'spring', 'summer', 'fall']
        if year.isdecimal():
            date = datetime.date.today()
            actual_year= int(date.strftime("%Y"))
            year_in = int(year)
            return (season in season_list) and ((year_in>=1917) & (year_in <= actual_year))
        return False

    def check_headers(self):
        r = requests.get('http://httpbin.org/headers',headers=self._headers)
        print(r.json()) 

    def __get_response_data(self):
        self.__info.inform(0,f'Requesting response from: {self.__url}')
        response = requests.get(self.__url,headers=self.__headers)
        self.__info.inform(0,f'Response size: {len(response.text)}')
        return response

    def parse_xml(self,xml):
        tree = ET.parse(xml)
        root = tree.getroot()
        urls = [ url[0].text for url in root ] 
        return urls 

    def can_fetch(self,url):
        robot_parser = urllib.robotparser.RobotFileParser()
        robot_parser.set_url(self.root_url+'/robots.txt')
        robot_parser.read()
        return robot_parser.can_fetch(self.user_agent,url) 

    def __build_data_set(self):
        self.__info.inform(0,'Building data in process...') 
        #response = self.__get_response_data()
        data_set = {}
        #resp.status_code should be 200
        if(True):
           # self.__info.inform(0,f'Response code: {response.status_code}')
            file = open('t.html','r')
            soup = BS(file.read(),'html.parser')
            list_div = soup.find_all('div',{'class':'seasonal-anime'})
            #Get Anime title, date, episodes, time and tags
            self.__info.inform(0,f'Estimated anime count: [{len(list_div)}]')
            count = 0
            data_set=[]
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
                    rating = None
                    try:
                        rating = float(r)
                    except:
                        rating = "null"
                    data.update({"rating":rating})
                data_set.append(data)
                count+=1
        else:
            self.__info.inform(2,f'Response code: {response.status_code}')
        self.__info.inform(0,f'Processing finished. Processed anime count:[{len(data_set)}]')
        self.__data_set = data_set

    def process_data(self): 
        self.__info.inform(0,'Starting thread')
        self.__data_extrator.start() 

    def get_data_set(self):
        if(self.__data_extrator.is_alive()):
            self.__info.inform(1,'Data wasnt extracted yet. Waiting...')
        self.__data_extrator.join()
        self.__info.inform(1,f"Data extracted: data_set length:[{len(self.__data_set)}]")
        return self.__data_set
    
    def export(self):
        with open(self.__json,'w') as output:
            json.dump(self.__data_set,output,indent=2)
        self.__info.inform(1,'Data was saved to out.json')
