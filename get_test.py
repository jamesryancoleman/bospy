from bos import *

def GetTest(bosPtUri:str):
    value = Get(bosPtUri)
    print(bosPtUri, "->", value, "({})".format(type(value)))
    
def GetMultipleTest(bosPtUris:list[str]):
    R = GetMutiple(bosPtUris)
    for key, value in R.items():
        print(key, "->", value, "({})".format(type(value)))

if __name__ == "__main__":
    print("sysmod address: ", SYSMOD_ADDR)
    print("devctrl address:", DEVCTRL_ADDR)
    
    test1_url = "bos://localhost/dev/1/pts/1"
    GetTest(test1_url)

    test2_url = "bos://localhost/dev/1/pts/2"
    test3_url = "bos://localhost/dev/1/pts/4"
    test4_url = "bos://localhost/dev/1/pts/5"

    GetMultipleTest([test2_url, test3_url, test4_url])
    