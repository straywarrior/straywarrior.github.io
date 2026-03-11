---
layout: post
title: "解决VMware NAT service服务无法启动或服务消失的问题"
date: 2015-05-27
categories: 
  - "computersoftware"
---

今日使用VMware中的Windows 7虚拟机（NAT模式）发现没有网络，网卡显示“网络电缆已拔出”，检查之后发现宿主机的VMware NAT service服务没有启动，手动启动弹出错误提示“1067：进程意外终止”。

由于昨日刚升级宿主机的系统，猜想可能由于某些原因破坏了某些服务的依赖文件，如果是这样可能必须重装VMware才能解决。经过一些尝试之后，找到了不需要重装VMware的解决方法：

打开VMware的虚拟网络编辑器，选择“还原默认设置”，这时它会自动删除所有的VMware网络服务和虚拟网卡并且重新安装服务。如果操作完之后VMware NAT service消失了，就再进行一次“还原默认设置”，应该能解决问题。

还原默认设置之后，VMware NAT的子网IP和DHCP设置会发生变化，如果之前有IP相关的设置（比如端口转发），则使用虚拟网络编辑器重新设置子网的IP段即可。
