---
layout: post
title: "引起SSH no such user or key错误的不常见原因"
date: 2015-05-11
categories: 
  - "linux"
---

今天花了大半天的时间在Cent OS系统上搭建了一个GitLab，本来是傻瓜式的一键安装，可是却始终无法SSH登陆获取仓库，使用HTTP登陆则可以。

Git提示SSH错误，No such user or key。

尝试修改各种设置都无果，最终发现原因是我的SSH公钥在.ssh/authorized\_keys里写了两次，只要删掉其中一个就一切正常了。

为什么会被写两次呢？因为一开始我指定GitLab在Linux下使用的用户是git，之后我又修改了/etc/gitlab/gitlab.rb的设置，将它使用的用户变为了gitlab。然而gitlab-ctl reconfigure命令执行时存在问题，没有给/home/gitlab/.ssh赋予正确的用户权限。

此时我在Gitlab的网页端进行Profile管理时删除了我的SSH Key，然而由于gitlab用户并没有权限修改/home/gitlab/.ssh，导致authorized\_keys并未被修改，而网站数据库中的SSH Key已经被删除了（这里实际上也是一个事务操作上的Bug）。

之后我发现用户权限不正确并修改了文件权限。此时，我为了验证authorized\_keys可以被正常修改，就又从网页端添加了同一个key，导致这个key被写入了2次。
