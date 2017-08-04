#!/usr/bin/env python
import sys,sardonyx

filename = sys.argv[1]
contents = open(filename).read()
contents = contents.replace("\n","")
print(sardonyx.run(contents))
