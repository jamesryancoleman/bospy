# bospy
python wrappers for accessing bos services. 

## `get`
`get(key:str)` takes a bos point key and returns a response object containing the 
value.

Usage:
``` python
# get_example.py
pt = GetPointByName('my-first-point')
value = Get(pt)
print(value)
```
Output:
``` shell
$ python get_example.py
21.0
```

## `set`
`set(key:str, value:str)` takes 1 bos point key and 1 value and returns a response object confirming whether the operation succeeded.

Usage:
``` python
# set_example.py
pt = GetPointByName('my-first-point')
ok = Set(pt, 23)
if ok:
    print('success')
else:
    print('failed to write', key)
```
Output:
``` shell
$ python set_example.py
success
```
