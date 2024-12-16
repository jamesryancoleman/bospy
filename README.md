# bospy
python wrappers for accessing bos services

# `get`
`get(key:str)` takes 1 bos point key and returns a response object containing the 
value.

Usage:
``` python
# get_example.py
key = GetPointByName('my-first-point')
resp = Get(key)
print(resp.Value)
```
Output:
``` shell
$ python get_example.py
21.0
```

# `set`
`set(key:str, value:str)` takes 1 bos point key and 1 value and returns a response object confirming whether the operation succeeded.

Usage:
``` python
# set_example.py
key = GetPointByName('my-first-point')
resp = Set(key, 23)
if resp.Ok:
    print('success')
else:
    print('failed to write', key)
```
Output:
``` shell
$ python set_example.py
success
```
