#coding: utf-8
import os
import mistune
in_name = 'pandas_select.md'
with open(in_name, 'r') as fi:
    data = fi.read()
out = "<head><meta charset='utf-8'></head>"
out += mistune.markdown(data)
with open(os.path.splitext(in_name)[0]+'.html', 'w') as fo:
    fo.write(out)

