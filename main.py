from scrapper import Scrapper 

scrap = Scrapper(2019,'winter')
scrap.process_data()
data = scrap.get_data_set()
print('\n',data[0])
