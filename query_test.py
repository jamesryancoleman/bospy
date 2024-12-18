from bos_utils import *
from bos import *

simple_output = True

def NameTest(name:str):
    pt = NameToPoint(name)
    if simple_output:
        pt = SimplifyPoint(pt)
    print("== point(s) named {} ==".format(name))
    print("\t", pt)
    return pt
    
def NameTest2(name:str):
    pts = NameToPoint(name, multiple_matches=True)
    if simple_output:
        pts = SimplifyPoint(pts)
    print("== point(s) named {} ==".format(name))
    print("\t", " ".join(pts))
    return pts

def PointNameTest(pt:str):
    name = PointToName(pt)
    if simple_output:
        pt = SimplifyPoint(pt)
    print("== Name of {} ==".format(pt))
    print("\t", name)
    return name

def TypeTest(_type:str):
    pts = TypeToPoint(_type)
    if simple_output:
        pts = SimplifyPoint(pts)
        _type = SimplifyBrickType(_type)
    print("== point(s) typed {} ==".format(_type))
    print("\t", " ".join(pts))
    return pts

def LocationTest(location:str):
    pts = LocationToPoint(location)
    if simple_output:
        pts = SimplifyPoint(pts)
    print("== point(s) located in '{}' ==".format(location))
    print("\t", " ".join(pts))
    return pts

def QueryTest(_type:str=None, location:str=None):
    if _type == "" and location == "":
        print("error: must provide type or location")
        return
    pt = QueryPoints(_type, location)
    if simple_output:
        pt = SimplifyPoint(pt)
        _type = SimplifyBrickType(_type)
    print("== point(s) located in '{}' with type {} ==".format(location, _type))
    print("\t", pt)
    return pt

if __name__ == "__main__":
    name1 = "air_temp" # will only return 1 point
    name2 = "temp"     # will return more than 1 point

    NameTest(name1)
    NameTest2(name2)

    ptUri1 = "bos://localhost/dev/1/pts/3"
    PointNameTest(ptUri1)

    type1 = "https://brickschema.org/schema/Brick#Air_Temperature_Sensor"
    TypeTest(type1)

    location1 = "SouthSt"
    LocationTest(location1)

    location2 = "lab"
    QueryTest(type1, location2)