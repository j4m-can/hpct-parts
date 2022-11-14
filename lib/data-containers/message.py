#
#
# message.py

import base64
import json
import secrets


class Message:
    def __init__(self, encs=None):
        d = self._loads(encs) if encs != None else {}

        self.bdata = d.get("bdata", None)
        self.comment = d.get("comment", None)
        self.dst = d.get("dst", None)
        self.dtype = d.get("dtype", None)
        self.nonce = d.get("nonce", None)
        self.src = d.get("src", None)
        self.tag = d.get("tag", None)
        self.tdata = d.get("tdata", None)

    def __repr__(self):
        return self._dumps()

    def _dumps(self):
        bdata = self.bdata
        if bdata != None:
            bdata = base64.b64encode(bdata).decode("utf-8")

        return json.dumps(
            {
                "bdata": bdata,
                "comment": self.comment,
                "dst": self.dst,
                "dtype": self.dtype,
                "nonce": self.nonce,
                "src": self.src,
                "tag": self.tag,
                "tdata": self.tdata,
            }
        )

    def _loads(self, encs):
        d = json.loads(encs)
        bdata = d.get("bdata", None)
        if bdata != None:
            d["bdata"] = base64.b64decode(bdata.encode("utf-8"))
        return d

    def set_nonce(self):
        self.nonce = secrets.token_urlsafe()
