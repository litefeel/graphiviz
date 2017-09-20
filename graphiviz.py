#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# http://www.graphviz.org/
# http://www.webgraphviz.com/
# https://github.com/litefeel/graphiviz
# 
# generate graphiviz dot language from text or json
# 


import os, os.path
import json
import argparse

VERSION = '1.0'
ObjectHeads = ('+--- ', '\--- ')

def readfile(filename):
    with open(filename, encoding = 'utf-8') as f:
        return f.read()

def writefile(filename, data):
    with open(filename, mode='w', encoding = 'utf-8') as f:
        f.write(data)

def parse_tree(lines, map, i, strip_len):
    while i < len(lines):
        line = lines[i][strip_len:]

        if line.strip().startswith(ObjectHeads):
            key = line[len(ObjectHeads[0]):]
            childmap = map[key] = {}
            i = parse_tree(lines, childmap, i + 1, strip_len + len(ObjectHeads[0]))
        else:
            return i
    return i


def text2map(data):
    lines = data.splitlines()
    map = {}
    parse_tree(lines, map, 0, 0)
    return map

def file2map(filename, content_type):
    data = readfile(filename)
    if content_type == 'txt':
        return text2map(data)
    elif content_type == 'json':
        return json.loads(data)
    else:
        raise ValueError('inviald content type %s' % content_type, file=sys.stderr) 
    return None
    
# 使map平坦化
def flat_map(topmap, map, childs = None):
    for k, v in map.items():
        if childs is not None and k not in childs:
            childs.append(k)
        list = topmap[k] = topmap.get(k, [])
        flat_map(topmap, v, list)
    return topmap

"""生成关系图
"""
def gen_graphiviz(topmap):
    strs = ['digraph G {\n']
    Indent = '    "'
    for k, list in topmap.items():
        if list:
            for s in list:
                strs.extend((Indent, k, '" -> "', s, '";\n'))
        else:
            strs.extend((Indent, k, ';\n'))
    strs.append('}')
    return ''.join(strs)

# text file to json
def file2json(filename, content_type):
    map = file2map(filename, content_type)
    return json.dumps(map, indent = 4)

# file to graphviz
# @content_type str [txt, json]
def file2gv(filename, content_type):
    map = file2map(filename, content_type)
    map = flat_map({}, map)
    gv = gen_graphiviz(map)
    return gv

def detect_format(format, filename, exts, err):
    if format != 'auto':
        return format
    if filename:
        _, ext = os.path.splitext(filename)
        if ext in exts:
            return ext[1:]
    
    raise ValueError(err)

# -------------- main ----------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <file>',
        formatter_class=argparse.RawTextHelpFormatter,
        description="generate graphiviz dot language from text or json")

    parser.add_argument('-v', '--version', action='version',
        version='%(prog)s version ' + VERSION)

    parser.add_argument('-o', '--output',
        help='output filename')

    parser.add_argument('-f', '--format',
        choices=['auto', 'txt', 'json'], default='auto',
        help='input file format (default: %(default)s)')

    parser.add_argument('-F', '--outformat',
        choices=['gv', 'json', 'auto'], default='gv',
        help='output file format (default: %(default)s)')

    parser.add_argument('file',
        help='input filename')
    
    args = parser.parse_args()


    input_format = detect_format(
        args.format, args.file,
        ('.txt', '.json'),
        'can not detect input file format')
    output_format = detect_format(
        args.outformat, args.output,
        ('.gv', '.json'),
        'can not detect input file format')
    
    if output_format == 'gv':
        data = file2gv(args.file, input_format)
    elif output_format == 'json':
        data = file2json(args.file, input_format)

    if args.output:
        writefile(args.output, data)
    else:
        print(data)
