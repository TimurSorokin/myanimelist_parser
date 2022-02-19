import urllib.robotparser
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS
from informer import Informer 

class Scrapper: 
    def __init__(self,year,season):
        self.__url = 'https://myanimelist.net/anime/season/'+str(year)+'/'+season
        self.__headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0','Accept-Language':'es','Accept-Encoding':'gzip, deflate','Accept':'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Refer':'null'}
        self.__data_set = None
        self.__info = Informer()
        self.__info.inform(0,f'Received values: {season} {year}')
    def check_headers(self):
        r = requests.get('http://httpbin.org/headers',headers=self._headers)
        print(r.json()) 
    def get_response_data(self):
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
    def build_data_set(self,response): 
        data_set = []
        if(response.status_code==200):
            self.__info.inform(0,f'Response code: {response.status_code}')
            soup = BS(response.text,'html.parser')
            list_div = soup.find_all('div',{'class':'seasonal-anime'})
            #Get Anime title, date, episodes, time and tags
            self.__info.inform(0,f'Found div: class = "seasonal-anime": {len(list_div)}')
            for div in list_div:
                title = div.find('a',{'class':'link-title'})
                #Title
                if(title!=None):
                    data = []
                    data.append(title.text)
                    #Info: date,num episodes, duration
                    info = div.find('div',{'class':'info'})
                    for value in info:
                        if not value.text.isspace():
                            val = value.text.replace(' ','').replace('\n',r'')
                            data.append(val)
                     #Tags: Categories
                    tags = div.find('div',{'class':'genres'})
                    for tag in tags:
                        if not tag.text.isspace():
                         data.append(tag.text.split())
                    #Rating
                    rate = div.find('div',{'class':'score'})
                    r = rate.text.replace(' ','').replace('\n',r'')
                    #Parsing values
                    rating = None
                    try:
                        rating = float(r)
                    except:
                        self.__info.inform(2,f'Coudlnt parse: {r}. Assigned NaN')
                        rating = float('NaN')
                    data.append(rating)
                data_set.append(data)
        else:
            self.__info.inform(2,f'Response code: {response.status_code}')
        self.__info.inform(0,f'Processing finished. Total items: {len(data_set)}')
        self.__data_set = data_set

    def get_data_set(self):
        self.__info.inform(0,f"Scrapper's data set length: {len(self.__data_set)}")
        return self.__data_set
