---
layout: post
title: "OS X系统读写NTFS文件系统"
date: 2015-06-10
categories: 
  - "macos"
---

Mac OS X系统原生支持NTFS文件系统的读写，但是默认情况下只能使用“Read Only”模式，无法进行写操作。

OS X系统中，NTFS文件系统的磁盘是通过一个专用的mount\_ntfs命令挂载的，该命令存在于/sbin/目录下。该命令可以使用-o rw参数打开NTFS磁盘的写权限，因此可以使用一个Wrapper来自动挂载NTFS磁盘并打开写入权限。

打开终端，首先备份原来的mount\_ntfs命令，新建并打开一个新的文件。

```
sudo mv /sbin/mount_ntfs /sbin/mount_ntfs.orig
sudo vim /sbin/mount_ntfs
```

然后在该文件中输入以下内容，保存并退出。

```
#!/bin/bash
/sbin/mount_ntfs.orig -o rw,nobrowse "$@"
```

然后给该文件赋予执行权限：

```
sudo chmod 755 mount_ntfs
```

特别注意：命令中的“nobrowse”参数是必须的（如果省去了这个参数，OS X 10.10下实测不可行），否则NTFS磁盘挂载之后依然处于只读的模式。然而加上了“nobrowse”参数意味着磁盘不会自动出现在桌面上，也不会在Finder的侧边栏中出现。要访问这个磁盘，一个简便的方法是在终端中输入

```
open /Volumes
```

这时会打开一个新的Finder窗口，列出了所有磁盘，找到所挂载的NTFS磁盘就可以像一般的磁盘那样使用了。

\----------------------

2015-12-31更新：

OS X系统默认不开启NTFS的写入权限，大概一是因为NTFS属于微软的商业机密，二是因为OS X的文件系统和NTFS差别较大，兼容性和稳定性都有问题。在OS X和Windows上同时使用同一个NTFS磁盘最容易遇到的问题大概就是文件的安全权限不稳定，比如该[日志](/posts/getaccess-os-x-created-files-in-windows/ "使用批处理解决OS X系统修改文件后在Windows中无法访问的问题")提到的问题。

因此，我现在不太使用OS X写NTFS磁盘，对于一些经常需要在两个系统之间交换的数据使用一个FAT32格式的磁盘进行同步。
