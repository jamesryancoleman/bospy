from bos import *

def GetValueByNameTest(name:str):
    pt = NameToPoint(name)
    value = Get(pt)
    print(name, "->", value)

if __name__ == "__main__":

    name1 = "air_temp" # a name that returns 1 point
    GetValueByNameTest(name1)