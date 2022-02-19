from scrapper import Scrapper 

def test_all(year,season):
    scrap = Scrapper(year,season)
    scrap.process_data()
    data = scrap.get_data_set()
    scrap.export()

def check (year,season):
    sc = Scrapper(year,season)


if __name__ == '__main__':
    test_all('2018','winter')
    #check('2021','fall')
