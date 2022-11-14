#
#
# blob.py

import base64
import grp
import hashlib
import json
import os
import pathlib
import pwd


class Blob:
    def __init__(self, encs=None):
        d = self._loads(encs) if encs != None else {}

        self.data = d.get("data", None)

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
            }
        )

    def _loads(self, encs):
        d = json.loads(encs)
        if d.get("dtype", "t") == "b":
            d["data"] = base64.b64decode(d["data"].encode("utf-8"))
        return d
