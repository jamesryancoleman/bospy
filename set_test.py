from bos import *

def SetTest(bosPtUri:str, value:str):
    ok = Set(bosPtUri, value)
    if ok:
        print(bosPtUri, "<-", value, "(ok)")
    else:
        print(bosPtUri, "<-", value, "(SetError)")

def SetMultipleTest(keys:list[str], values:list[Any]):
    R = Set(keys, values)
    for r in R:
        bosPtUri = r.Key
        valueStr = r.ValueStr # drivers are not required to provide this in response
        if r.Ok:
            print(bosPtUri, "<-", valueStr, "(ok)")
        else:
            print(bosPtUri, "<-", valueStr, "(SetError)")

if __name__ == "__main__":
    print("sysmod address: ", SYSMOD_ADDR)
    print("devctrl address:", DEVCTRL_ADDR)
    
    test1_url = "bos://localhost/dev/1/pts/1"
    SetTest(test1_url, 420)

    test2_url = "bos://localhost/dev/1/pts/2"
    test3_url = "bos://localhost/dev/1/pts/4"
    test4_url = "bos://localhost/dev/1/pts/5"
    SetMultipleTest(
        [test2_url, test3_url, test4_url],
        [18, 80, True],
        )
    
    SetMultipleTest(
         [test2_url, test3_url], 
         20
    )