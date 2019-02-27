#!/usr/bin/env python
#

import sys

name_dict = {}
for line in sys.stdin:
    fields = line.rstrip('\n').split('|')
    query = fields[0]
    name = fields[1]
    try:
        imp = int(fields[2])
        clk = int(fields[3])
        long_clk = int(fields[4])
    except:
        continue

    if name not in name_dict:
        name_dict[name] = [imp, [(query, name, imp, clk, long_clk)]]
        continue

    cur_value = name_dict[name]
    total_imp = cur_value[0] + imp
    cur_meta_list = name_dict[name][1]
    cur_meta_list.append((query, name, imp, clk, long_clk))
    name_dict[name] = [total_imp, cur_meta_list]

name_meta_list = sorted(name_dict.iteritems(), key = lambda item:item[1][0], reverse = True)
for item in name_meta_list:
    meta_list = item[1][1]
    meta_list.sort(key = lambda it:it[2], reverse = True)
    for meta in meta_list:
        print '|'.join(['%s' % item_meta for item_meta in meta])
