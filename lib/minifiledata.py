#
#
# minifiledata.py

import base64
import grp
import json
import os
import pathlib
import pwd


class MiniFileData:
    def __init__(self, encs=None):
        d = self._loads(encs) if encs != None else {}

        self.data = d.get("data", "")
        self.name = d.get("name", None)
        self.path = d.get("path", None)

    def __repr__(self):
        return self._dumps()

    def _dumps(self):
        if type(self.data) == bytes:
            dtype = "b"
            data = base64.b64encode(self.data).decode("utf-8")
        else:
            dtype = "t"
            data = self.data

        return json.dumps(
            {
                "data": data,
                "dtype": dtype,
                "name": self.name,
                "path": self.path,
            }
        )

    def _loads(self, s):
        d = json.loads(s)
        if d.get("dtype", "t") == "b":
            d["data"] = base64.b64decode(d["data"].encode("utf-8"))
        return d

    def load(self, path, dtype="t"):
        p = pathlib.Path(path)
        if not p.exists():
            raise Exception("file not found")

        self.data = p.read_text() if dtype == "t" else p.read_bytes()
        self.path = str(p.resolve())
        self.name = p.name

    def save(self, path, mode=None, owner=None, group=None):
        try:
            owner = owner if owner != None else -1
            group = group if group != None else -1
            uid = owner if type(owner) == int else pwd.getpwnam(owner).pw_uid
            gid = group if type(group) == int else grp.getgrnam(group).gr_gid
        except:
            raise Exception("bad owner and/or group")

        p = pathlib.Path(path)
        p.touch()

        if (uid, gid) != (-1, -1):
            os.chown(path, uid, gid)

        if mode != None:
            p.chmod(mode)

        if type(self.data) == str:
            p.write_text(self.data)
        else:
            p.write_bytes(self.data)
