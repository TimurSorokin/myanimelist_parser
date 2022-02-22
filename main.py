import json
from scrapper import Scrapper 
import sys
import datetime
import os.path
from informer import Informer
from reporter import Reporter

info = Informer()
def __do_exist(season,year):
    status = os.path.isfile(f'{season}-{year}.json') 
    info.inform(0,f'checking if file exists {season}-{year}.json status: {status}')
    return status
def __validate_year(year):
    min_limit = 1927
    max_limit = int(datetime.date.today().strftime('%Y'))
    return year.isdecimal and int(year)>=min_limit and int(year)<=max_limit
def __validate_season(season):
    season_list = ['winter', 'spring', 'summer', 'fall']
    return season in season_list
def __validate_arguments():
    status = True
    if(len(sys.argv)<3 or not __validate_season(sys.argv[1]) or not __validate_year(sys.argv[2])): 
        info.inform(2,f'Incorrect input {sys.argv}')
        status = False
    return status
def test_all(year,season):
    scrap = Scrapper(year,season,info)
    scrap.process_data()
    data = scrap.get_data_set()
    scrap.export()

if __name__ == '__main__':
    if(__validate_arguments() and not __do_exist(sys.argv[1],sys.argv[2])):
        test_all('2018','winter')
    else:
        with open ("winter-2018.json") as file:
            rep = Reporter (file)
            rep.show_json(15)
