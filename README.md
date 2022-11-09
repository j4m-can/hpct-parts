# Parts

This repository holds parts that can be used/reused.

## `FileData` (and `MiniFileData`)

`FileData` and `MiniFileData` both encapsulate functionality to load,
save, and share files. `FileData` provides meta-data in addition to
the file data while `MiniFileData` provides file data only. File data
is available in the type loaded (text or binary). When stringifying,
binary is converted to base64. The `_dumps()` method returns a
stringified json object with data and metadata. `_loads()` reverses
the stringification of the json object and returns a dictionary.

To load a text file (default is text, "t"):

```python
fd = FileData()
fd.load("/etc/hosts")
```

To load a binary file:

```python
fd = FileData()
fd.load("/boot/initrd.img", "b")
```

To save a file (the data type is taken from the encoded information):

```python
encs = "<filedata-encoded-string>"
fd = FileData(encs)
fd.save(fd.path)
```

The encoded (stringified json object) can be produced by:

```python
encs = fd._dumps()
```

or

```python
encs = str(fd)
```

The data type can be determined by:

```python
print(type(fd.data) == str and "t" or "b")
```

Using `FileData` metadata:

```python
fd = FileData()
fd.load("/etc/hosts")
print(fd.name, fd.path, fd.size, fd.mode, fd.uid, fd.gid, fd.user, fd.group)
```

```python
fd = FileData()
fd.load("/boot/vmlinuz", "b")
print(fd.name, fd.path, fd.size, fd.mode, fd.uid, fd.gid, fd.user, fd.group)
```

A round trip of load and save:

```python
fd = FileData()
fd.load("/etc/hosts")

encs = fd._dumps()
fd2 = FileData(encs)
fd2.save("/tmp/etc-hosts")
```

In a charm, working directly with an app data bucket (key is
`hosts-file`):

```python
class Server(CharmBase):

    def on_x_relation_created(self, event):
        if self.is_leader():
            fd = FileData()
            fd.load("/etc/hosts")

            appdata = event.relation.data[self.app]
            appdata.update({"hosts-file": fd._dumps()})
```

and to get from the data bucket and save:

```python
class Client(CharmBase):

    def on_x_relation_changed(self, event):
        appdata = event.relation.data[event.app]

        fd = FileData(appdata.get("hosts_file"))
        fd.save(fd.path, fd.mode, fd.owner, fd.group)
```
