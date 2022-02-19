from scrapper import Scrapper 

scrap = Scrapper(2021,'fall')
response = scrap.get_response_data()
scrap.build_data_set(response)
data = scrap.get_data_set()
print(data[0])
