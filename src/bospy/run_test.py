import bospy.run

if __name__ == "__main__":
    # bospy.run.Run("random-get", "other-arg", envVars={"ENVVAR": "hello"}, anotherVar="hello again")
    bospy.run.kwargs['txn_id'] = 0
    bospy.run.kwargs['session_token'] = '000000000000'
    print( bospy.run.kwargs.get('txn_id'), bospy.run.kwargs.get('session_token'))
    resp = bospy.run.Return("hello", True, 10, 100.1, name="James", age=30)
    print(resp.ErrorMsg, resp.Error)