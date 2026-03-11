---
layout: post
title: "Python 3使用Basemap导入ESRI信息的问题"
date: 2015-11-15
categories: 
  - "programminglanguage"
  - "python"
---

Basemap使用自带的shapefile.py处理ESRI的shapefile，但是Basemap自带的shapefile版本过低(1.1.x)，其中存在一个bug导致使用Python 3.x版本时无法正确处理Windows-1252编码的二进制文件。典型错误：

```
File "D:\Python34\lib\site-packages\mpl_toolkits\basemap\shapefile.py", line 58, in u
    return v.decode('utf-8')
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte
```

解决方法一：

使用pip安装pyshp (pip install pyshp )，或者手动下载最新版本的pyshp，并且将shapefile.py拷贝到Basemap的目录中(<python-install-prefix>\\lib\\site-packages\\mpl\_toolkits\\basemap )。

解决方法二：

按照一的方式使用pip安装pyshp，并且修改Basemap的源代码，将\_\_init\_\_.py中shapefile模块的import语句略作修改，不再使用相对路径的导入方式并删除Basemap目录中的shapefile.py。修改之前为

```
from . import shapefile as shp
from .shapefile import Reader
```

修改之后为

```
import shapefile as shp
from shapefile import Reader
```

使用方法二的一个好处是，使用pip更新pyshp后不需要再更新Basemap中的shapefile.py
