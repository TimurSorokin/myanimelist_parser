import json
from ccolors import ccolors
class Reporter:

    def __init__(self,data):
        self.__data = data
    
    def __sort_key(self,e):
        key = None
        try:
            key = float(e.get('rating'))
        except:
            key = 0
        return key
    
    def __get_longest(self,data_json,key,num_entries):
        max_size = 0
        for i in  range(num_entries):
            item = data_json[i]
            item_size = len(str(item.get(key)))
            if(item_size>max_size):
                max_size=item_size
        return max_size
    
    def __build_container(self,data,max_size,space=0,separator=' '):
        if(len(data)>max_size):
                return data[0:max_size-3]+'...'
        diff = max_size - len(data)
        return (separator*space)+data+(separator*diff)
    
    def __print_table(self,data_json,num_entries):
        max_index = len(str(num_entries))+1 
        #max_title = self.__get_longest(data_json,'title',num_entries)+1
        max_title = 40
        max_rating = self.__get_longest(data_json,'rating',num_entries)+5
        max_genres = 30 
        
        head_id = self.__build_container('ID',max_index,0,'_')
        head_title = self.__build_container('TITLE',max_title,0,'_')
        head_rating = self.__build_container('RATING',max_rating,0,'_')
        head_genres = self.__build_container('GENRES',max_genres,0,'_')
        table = [head_id+head_title+head_rating+head_genres]
        print(table[0])
        for i in range(num_entries):
            item = data_json[i]
            title = item.get('title')
            rating = item.get('rating')
            genres = ', '.join(item.get('tags'))
            id_cont = self.__build_container(str(i+1),max_index)
            title_cont = self.__build_container(title,max_title)
            rating_cont = self.__build_container(str(rating),max_rating)
            genre_cont = self.__build_container(genres,max_genres)
            color = ccolors.GREEN if i%2==0 else ccolors.CYAN
            entry = (f'{id_cont}{color}{title_cont}{ccolors.BLUE}{rating_cont}{ccolors.MAGENTA}{genre_cont}{ccolors.DEFAULT}')  

            table.append(entry)
            print(entry) 
    def show_data(self,num_entries):
        self.__data.sort(key=self.__sort_key,reverse=True)
        if(num_entries == 'all' or num_entries>len(self.__data)):
            num_entries = len(self.__data) 
        self.__print_table(self.__data,num_entries)
    def show_json (self,num_entries):
        data_json = json.load(self.__data)
        data_json.sort(key=self.__sort_key,reverse=True)
        if(num_entries == 'all' or num_entries>len(data_json)):
            num_entries = len(data_json) 
        self.__print_table(data_json,num_entries)
