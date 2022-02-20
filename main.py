from scrapper import Scrapper 
import sys
import datetime
from informer import Informer

info = Informer()

def is_valid():
    info.inform(0,f'Validating {sys.argv}')
    status = False
    if(len(sys.argv)<3):
        info.inform(2,f'Incorrect input {sys.argv}. Expected: year season')
    else: 
        season = sys.argv[1]
        year = sys.argv[2]
        season_list = ['winter', 'spring', 'summer', 'fall']
        if year.isdecimal():
            date = datetime.date.today()
            actual_year= int(date.strftime("%Y"))
            year_in = int(year)
            status = (season in season_list) and ((year_in>=1917) & (year_in <= actual_year)) 
    info.inform(1,f'Validate: {status}')
    return status

def test_all(year,season):
    scrap = Scrapper(year,season,info)
    scrap.process_data()
    data = scrap.get_data_set()
    scrap.export()

if __name__ == '__main__':
    if(is_valid()):
        test_all('2018','winter')
