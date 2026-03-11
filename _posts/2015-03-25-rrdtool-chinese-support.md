---
layout: post
title: "让rrdtool 1.3.x支持中文字体"
date: 2015-03-25
categories: 
  - "linux"
---

系统环境：CentOS 6.6

rrdtool版本：1.3.8 - 1.4.7均验证可用

rrdtool默认不支持中文编码，在网上查询了很多方法都说需要重新编译rrdtool，但是rrdtool的编译安装极其繁琐，需要各种依赖库，而搭建的CentOS环境里几乎是一片空白，想要搭个编译环境甚是麻烦。实际上方法很简单，下载一个TrueType字体文件（例如SIMHEI.TTF），移入/usr/share/fonts文件夹，再执行命令

```
$sudo fc-cache -fv
```

再用rrdtool作图时加上\[**\-n**|**\--font** _FONTTAG_**:**_size_\[**:**_font_\]\]选项即可：

FONTTAG是TITLE、LEGEND等图的元素标签。

如果rrdtool是配合cacti使用的，进入cacti的设置，在Settings-Path里设定Default Font即可。

之前一直想用msyh.ttf（微软雅黑字体）却都不能成功，换了一个字体就成功了。
