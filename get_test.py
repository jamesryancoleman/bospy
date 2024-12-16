from bos import *

def GetTest(bosPtUri:str):
    r = Get(bosPtUri)
    value = r.Value
    print(bosPtUri, "->", value, "({})".format(type(value)))
    
def GetMultipleTest(bosPtUris:list[str]):
    R = GetMutiple(bosPtUris)
    for r in R:
        key = r.Key
        value = r.Value
        print(key, "->", value, "({})".format(type(value)))

if __name__ == "__main__":
    print("sysmod address: ", SYSMOD_ADDR)
    print("devctrl address:", DEVCTRL_ADDR)
    
    test1_url = "bos://localhost/bos/dev/1/pts/1"
    GetTest(test1_url)

    test2_url = "bos://localhost/bos/dev/1/pts/2"
    test3_url = "bos://localhost/bos/dev/1/pts/4"
    test4_url = "bos://localhost/bos/dev/1/pts/5"

    GetMultipleTest([test2_url, test3_url, test4_url])
    