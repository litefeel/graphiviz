# graphiviz
[![Build Status](https://travis-ci.org/litefeel/graphiviz.svg?branch=master)](https://travis-ci.org/litefeel/graphiviz)

generate graphiviz dot language from text or json

### 使用方法

~~~
>graphiviz.py -h
usage: graphiviz.py [options] <file>

generate graphiviz dot language from text or json

positional arguments:
  file                  input filename

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        output filename
  -f {auto,txt,json}, --format {auto,txt,json}
                        input file format (default: auto)
  -F {gv,json,auto}, --outformat {gv,json,auto}
                        output file format (default: auto)
~~~


#### 文件格式

- txt : 请看 [data.txt](https://github.com/litefeel/graphiviz/blob/master/test/data.txt)
- json: 请看 [data.json](https://github.com/litefeel/graphiviz/blob/master/test/data.json)
- gv:   请看 [data.gv](https://github.com/litefeel/graphiviz/blob/master/test/data.gv)


#### 如何可视化关系图

- 在线工具: <http://www.webgraphviz.com/>
- 客户端工具: <http://www.graphviz.org/>
