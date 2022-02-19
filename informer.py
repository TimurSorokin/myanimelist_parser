from datetime import datetime

class Informer:
    def __init__(self):
        self._colors = ['\033[92m','\033[93m','\033[91m','\033[0m']
        self._code = ['[INFO]','[WARN]','[ERROR]']
    def inform(self,code,msg):
        if code < 0 or code > 2:
            print(f'{code} not a valid CODE')
        else:
            print(f"{self._colors[code]}->:{self._code[code]}:[{datetime.now().time()}]: {msg} {self._colors[3]}")



