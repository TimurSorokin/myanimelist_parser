from datetime import datetime
import inspect

class Informer:
    def __init__(self):
        self.__colors = ['\033[32m','\033[33m','\033[91m','\033[36m','\033[0m','\033[35m']
        self.__code = ['[INFO]','[WARN]','[ERROR]'] 
    def __parse_caller(self,caller):
        index = 0
        path = caller[1][1]
        for i in range(len(path)-1,0,-1):
            if(path[i]=='/' or path[i] == '"\"'):
                index = i
                break
        file = path[i:len(path)]
        return [file, caller[1][3]]
    def inform(self,code,msg):
        current = inspect.currentframe()
        caller = self.__parse_caller(inspect.getouterframes(current,2))
        if code < 0 or code > 2:
            print(f'{code} not a valid CODE')
        else:
            print(f"{self.__colors[code]}->:{self.__code[code]}:[{datetime.now().time()}]:{self.__colors[5]}{msg} >> {self.__colors[3]}{caller} {self.__colors[4]}") 
