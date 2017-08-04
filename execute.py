#!/usr/bin/env python
import sys,sardonyx

filename = sys.argv[1]
contents = open(filename).read()
lines = contents.split("\n")
if(lines[0].startswith("import ")):
    imports = lines[0].replace("import ","").split(",")
    contents = contents.replace(lines[0],"")
    for filename in imports:
        contents = open(filename).read() + contents
contents = contents.replace("\n","")
print(sardonyx.run(contents))
