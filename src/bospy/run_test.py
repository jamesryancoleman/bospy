import bospy.run

if __name__ == "__main__":
    bospy.run.Run("random-get", "other-arg", envVars={"ENVVAR": "hello"}, anotherVar="hello again")