from bos import *

def GetValueByNameTest(name:str):
    pts = NameToPoint(name)
    value = Get(pts)
    print(name, "->", value)

if __name__ == "__main__":

    name1 = "air_temp" # a name that returns 1 point
    GetValueByNameTest(name1)