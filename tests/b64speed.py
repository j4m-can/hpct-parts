#! /usr/bin/env python3

import base64
import time

b = open("/boot/initrd.img", "rb").read()
print(f"{len(b)}")

print("...")
t0 = time.time()
s = base64.b64encode(b)
elapsed = time.time()-t0
print(f"{len(s)} {elapsed=}")

print("...")
t0 = time.time()
s = base64.b85encode(b)
elapsed = time.time()-t0
print(f"{len(s)} {elapsed=}")
