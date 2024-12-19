# bospy
python wrappers for accessing bos services.

The basic operating principle of `bospy` is that points are accessed via "pointers". You get a pointer by using a function like `NameToPoint` and pass the output to a function like `get` or `set`.

making a query and you get or set a value using that pointer. The pointers are the uri strings of the point stored in the `sysmod`. 

## `Get`
`Get(points)` takes one or more point uris and returns values for each uri passed.

Getting a single point by name:
``` python
pt = NameToPoint('BLDG3.AHU2.RM1.TEMP')
value = Get(pt)
print(value)
```
Output:
``` shell
$ python get_example.py
21.0
```
Getting multiple values by location:
```python
pts = GetPointByLocation('ROOM_1')
resp = Get(pts)
for k, v in resp.items()
    name = GetPointName(k)
    print(name, v)
```
Output
``` bash
$ python get_multiple_example.py
BLDG3.AHU2.RM1.TEMP 22.5
BLDG3.AHU2.RM1.SETPOINT 21.0
BLDG3.AHU2.RM1.DAMPER_POS 85.0
```

## `Set`
`Set(points, values)` takes 1 or more point uris and an equal number of values. You may also pass a single value to be written to all provides 

Usage:
``` python
pt = GetPointByName('BLDG3.AHU2.RM1.SETPOINT')
ok = Set(pt, 23)
if ok:
    print('success')
else:
    print('failed to write', key)
```
Output:
``` bash
$ python set_example.py
success
```
## `get_multiple` and `set_multiple`
These work the same way as `get` and `set` but you pass a list of points to specify what points to read or write. To `set_multiple` points you can either pass 1 value that will be written to all points or a list of values the same length as the list of points. 

`get_multiple` usage:


`set_multiple` usage:
```python
pts = GetPointByType('brick:Air_Temperature_Setpoint')
resp = set_multiple(pts, 25) # degress celsius
```