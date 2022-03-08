import json
from scrapper import Scrapper 
import sys
import datetime
import os.path
import sys
from reporter import Reporter

def __do_exist(year,season):
    status = os.path.isfile(f'{year}{season}.json') 
    return status
def __get_arguments():
    year = int(datetime.date.today().strftime('%Y'))
    season = 'winter'
    num = 15
    try:
        year = int(sys.argv[1])
        season = sys.argv[2]
        num = int(sys.argv[3])
    except:
        print(f"Coudln't parse arguments {sys.argv}")
        return [year,season,num]

if __name__ == '__main__':
    arguments = __get_arguments()
    if(__do_exist(arguments[0],arguments[1])): 
        path = str(arguments[0])+arguments[1]+'.json'
        with open (path) as file:
            rep = Reporter (file)
            rep.show_json(int(arguments[2]))
    else:
        scrap = Scrapper(arguments[0],arguments[1])
        scrap.process_data()
        data = scrap.get_data()
        scrap.export(data)
        rep = Reporter(data)
        rep.show_data(int(arguments[2]))
    
