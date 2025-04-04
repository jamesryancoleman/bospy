import bospy.run as run

test_token = "000000000000"

def TestInferType():
    cases = ["123", "0.0", "FALSE", "google.com"]
    answers = [int, float, bool, str]

    results = []
    for i, s in enumerate(cases):
        typed_str = run.InferType(s)
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

    resp = run.Return(*args, **kwargs)
    print(resp)

def TestLoadInput():
    """ demonstrates how to load output from a previous node or instance of a flow.
    """
    test_cases = {
        "$3": "baz",
        "$2": "bar",
        "$1": "foo",
        "alice": "bob",
    }

    args, kwargs = run.LoadInput(test_cases)
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
        m = run.positionRe.match(k)
        if m is not None:
            positional_dict[int(m.group('position'))] = v
        else:
            print("'{}' did not match the positional argument pattern".format(k))
        

    args = [None] * len(positional_dict)
    for i, v in positional_dict.items():
        args[i-1] = v
    
    print("the ordered positional arguments are: {}".format(args))

def TestGet():
    keys = ["global:occupied",
            "global:weekday_occupied_start",
            "global:weekday_occupied_end",
            "OUTPUT/times_accessed",
            "an_invalid_token",
            ]
    results = run.Get(keys)
    for k, v in results.items():
        print(k, v)

if __name__ == "__main__":
    # bospy.run.Run("random-get", "other-arg", envVars={"ENVVAR": "hello"}, anotherVar="hello again")
    # bospy.run.kwargs['txn_id'] = 0
    # bospy.run.kwargs['session_token'] = '000000000000'
    # print( bospy.run.kwargs.get('txn_id'), bospy.run.kwargs.get('session_token'))
    # resp = bospy.run.Return("hello", True, 10, 100.1, name="James", age=30)
    # print(resp.ErrorMsg, resp.Error)
    TestInferType()
    TestMatchPositional()
    TestReturnValues()
    TestLoadInput()
    TestGet()



