from bos import *

def NameTest(name:str):
    pt = NameToPoint(name)
    print(pt)
    return pt
    
def NameTest2(name:str):
    pts = NameToPoint(name, multiple_matches=True)
    print(" ".join(pts))
    return pts

def TypeTest(_type:str):
    pts = TypeToPoint(_type)
    print(" ".join(pts))
    return pts

if __name__ == "__main__":
    name1 = "air_temp" # will only return 1 point
    name2 = "temp"     # will return more than 1 point

    NameTest(name1)
    NameTest2(name2)

    type1 = "https://brickschema.org/schema/Brick#Air_Temperature_Sensor"

    TypeTest(type1)