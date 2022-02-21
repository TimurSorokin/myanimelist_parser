import json

class Reporter:
    def __init__(self,file):
        self.__file = file 
        self.__colors = ['\033[34m','\033[35m','\033[36m','\033[92m','\033[0m'] 

    def __sort_key(self,e):
        key = None
        try:
            key = float(e.get('rating'))
        except:
            key = 0
        return key

    def show_json (self,num):
        data_json = json.load(self.__file)
        data_json.sort(key=self.__sort_key,reverse=True)
        for i in range(num):
            item = data_json[num]
            print(f'{self.__colors[0]}{item.get("info")}{self.__colors[4]}{self.__colors[1]}{item.get("rating")}{self.__colors[4]}{self.__colors[2]}{item.get("tags")}{self.__colors[4]}{self.__colors[3]}{item.get("title")}{self.__colors[4]}')
            
