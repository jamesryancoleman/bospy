from bos import *

def ValueByNameTest(name:str|list[str]):
    pts = NameToPoint(name)
    value = Get(pts)
    print(name, "->", value)

if __name__ == "__main__":

    name1 = "air_temp" # a name that returns 1 point
    ValueByNameTest(name1)

    name2 = "status"
    ValueByNameTest([name1, name2])