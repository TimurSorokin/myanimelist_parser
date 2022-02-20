from pprintpp import pprint
import json

class Reporter:
    def __init__(self,file):
        self.__file = file 
        self.__colors = ['\033[34m','\033[35m','\033[36m','\033[92m','\033[0m']
        #self.__category = [file.info, file.rating, file.tags, file.tittle]
    def show_json (self):
        data_json = json.load(self.__file)
        #data_json.keys()
        for item in data_json:
            print(f'{self.__colors[0]}{item.get("info")}{self.__colors[4]}{self.__colors[1]}{item.get("rating")}{self.__colors[4]}{self.__colors[2]}{item.get("tags")}{self.__colors[4]}{self.__colors[3]}{item.get("tittle")}{self.__colors[4]}')
            