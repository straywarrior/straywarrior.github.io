---
layout: post
title: "使用批处理解决OS X系统修改文件后在Windows中无法访问的问题"
date: 2015-11-17
categories: 
  - "mswindows"
---

由于NTFS文件系统权限管理的原因，OS X系统下新建或修改的文件一般在Windows中会因没有权限而无法访问，使用批处理可以较为快速地获得对某一文件或文件夹的控制权限。

使用以下代码新建一个批处理文件，保存为takeown.bat

```
@echo off
setlocal enabledelayedexpansion

:start
set /p dir="Input the directory you want to take own: "
echo, "%dir%"
takeown /F %dir% /R
ICACLS %dir% /inheritance:e
ICACLS %dir% /reset /T

goto start

pause
```

使用管理员身份运行后，将需要处理的文件路径粘贴入程序即可。

takeown和ICACLS均为Windows自带的权限管理命令。由于ICACLS并不强制夺取所有者权限，因此使用takeown命令完成夺取所有者权限的操作后，再使用ICACLS将上层目录的访问权限继承至目标目录。
