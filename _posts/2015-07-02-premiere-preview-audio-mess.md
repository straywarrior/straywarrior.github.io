---
layout: post
title: "解决Premiere文件预览音频流混乱/前后颠倒的问题"
date: 2015-07-02
categories: 
  - "adobe"
---

系统环境：Windows 8.1 Pro x64

软件版本：Premiere Pro CS6 (version 6.0.0)

今日使用Premiere发现一个奇怪的现象，某一个视频在预览窗口里预览以及放入序列之后都会有音频流混乱的现象，而该视频使用一般播放器均能正常播放，因此基本可以排除解码的问题。考虑到Premiere为了加快预览速度总是会在临时文件夹中缓存大量的源素材，猜想可能是某个缓存文件出现了问题。

本机的Premiere缓存目录地址被设置为在X:\\TEMP\\Adobe\\Media Cache Files\\，在其中找到了出问题的视频文件名字开头的一些文件，全部删除之后再次预览视频，Premiere重建了缓存并且恢复正常。

另附：

Premiere缓存目录的设置方式为：Edit->Preferences->Media，选择Media Cache Files 和Media Cache Database即可更改缓存的存储位置以及索引位置。
