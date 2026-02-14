# import bospy.run as run
# from bospy.app import Key
import bospy.config as config
import bospy.app as app
import unittest
import os

test_token = "000000000000"

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.app_name = "thinker"

        orch_addr = config.get_orchestrator_addr()
        print(f'test will use orchestator address: {orch_addr}')
    
    def test_load_input(self):
        args, kwargs = app.load_input(app_name=self.app_name)
        print("args:", args)
        print("kwargs:", kwargs)

    def tearDown(self):
        # return super().tearDown()
        pass


class TestStoreLoad(unittest.TestCase):
    def setUp(self):
        orch_addr = config.get_orchestrator_addr()
        print(f'test will use orchestator address: {orch_addr}')

    def test_01_return(self):
        app.store_output("bos://localhost/dev/5/pts/14")
    
    def test_02_load_input(self):
        args, kwargs = app.load_input(ns='tmp')
        print("args:", args)
        print("kwargs:", kwargs)

    def tearDown(self):
        # return super().tearDown()
        pass


# class TestRun(unittest.TestCase):
#     def setUp(self):
#         orch_addr = config.get_orchestrator_addr()
#         print(f'test will use orchestator address: {orch_addr}')

#     def test_01_run(self):
#         .Run('thinker', envVars={
#             'lower_bound': 10,
#             'upper_bound': 100,
#             'minutes': 0.5
#         }, timeout=-1)


def TestInferType():
    cases = ["123", "0.0", "FALSE", "google.com"]
    answers = [int, float, bool, str]

    results = []
    for i, s in enumerate(cases):
        typed_str = app.inter_type(s)
        print("'{}' is instance of {}".format(s, type(typed_str)))
        assert isinstance(typed_str, answers[i])

def TestReturnValues():
    """ demonstrates how to return numbered arguments and keyword arguments
    """
    args = [
        "bos://localhost/dev/1/pts/1",
        "bos://localhost/dev/1/pts/2",
        "bos://localhost/dev/1/pts/3",
    ]
    kwargs = {
        "times_accessed": 11,
    }

    resp = app.Return(*args, **kwargs)
    print(resp)

def TestLoadInput():
    """ demonstrates how to load output from a previous node or instance of a flow.
    """
    args, kwargs = app.LoadInput()
    print("args:  ", args)
    print("kwargs:", kwargs)

def TestMatchPositional():
    test_cases = {
        "$3": "baz",
        "$2": "bar",
        "$1": "foo",
        "alice": "bob",
    }

    positional_dict:dict[int, str] = {}
    for k, v in test_cases.items():
        m = app.positionRe.match(k)
        if m is not None:
            positional_dict[int(m.group('position'))] = v
        else:
            print("'{}' did not match the positional argument pattern".format(k))
        

    args = [None] * len(positional_dict)
    for i, v in positional_dict.items():
        args[i-1] = v
    
    print("the ordered positional arguments are: {}".format(args))

def TestSet():
    pairs = {
        "global:occupied": True,
        "OUTPUT/count": 1,
        "tmp/process_value": ">9000",
    }
    resp = app.Set(pairs)
    if resp.Error > 0:
        print(resp.Error, resp.ErrorMsg)

def TestGet():
    keys = ["global:occupied",
            "OUTPUT/count",
            "an_invalid_token",
            ]
    results = app.Get(keys)
    for k, v in results.items():
        print(k, v)


def TestIncrementAndNegate():
    keys = ["global:occupied",
        "OUTPUT/count",
        "an_invalid_token",
        ]
    results = app.Get(keys)
    returnVals = {}
    for k, v in results.items():
        print(k, v)
        if isinstance(v, bool):
            v = bool(not v)
            returnVals[k] = v
        elif isinstance(v, int):
            v += 1
            returnVals[k] = v
        elif v is None:
            continue
        print(k, v)
    app.Return(**returnVals)

# def TestFormatKeyStr():
#     unformattedKeys = [
#         Key("OUTPUT", "$1"),
#         Key("a_runtime_var"),
#         Key("occupied", ns="global"),
#     ]

#     answers = [
#         "flows:0.0:OUTPUT/$1",
#         "flows:0.0:a_runtime_var",
#         "global:occupied"
#     ]

#     for i, k in enumerate(unformattedKeys):
#         print("{}: {} == {} ({})".format(i, k, answers[i], answers[i] == k.__str__()))

def TestDefaultSession():
    """ checks if the server has the default session active by calling app.Return with no values.
    The flow, node, txn, and token are manually coordinated with the server source code.
    """
    resp = app.Return()
    print(resp)

def TestReturn():
    resp = app.Return("bos://localhost/dev/1","bos://localhost/dev/2","bos://localhost/dev/3",
                      User="James")
    print(resp)

def TestParseKey():
    cases = [
        "flows:9.8:100:OUTPUT/count",
        "flows:9.8:OUTPUT/$1",
        "global:occupied",
    ]
    for c in cases:
        k = app.ParseKey(c)
        print(k)

if __name__ == "__main__":
    # app.CreateDefaultRWSession()
    # bospy.app.Run("random-get", "other-arg", envVars={"ENVVAR": "hello"}, anotherVar="hello again")
    # bospy.app.kwargs['txn_id'] = 0
    # bospy.app.kwargs['session_token'] = '000000000000'
    # print( bospy.app.kwargs.get('txn_id'), bospy.app.kwargs.get('session_token'))
    # resp = bospy.app.Return("hello", True, 10, 100.1, name="James", age=30)
    # print(resp.ErrorMsg, resp.Error)
    # TestInferType()
    # TestMatchPositional()
    # TestReturnValues()

    # TestGet()
    # TestFormatKeyStr()

    # TestDefaultSession()
    # TestReturn()
    # TestLoadInput()
    # TestParseKey()
    # TestGet()
    TestSet()
    for i in range(3):
        TestIncrementAndNegate()



