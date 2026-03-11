---
layout: post
title: "WPF实现透明窗体和自动全屏"
date: 2015-05-01
categories: 
  - "c-wpf"
---

最近突发奇想准备基于C#（客户端）和Python（服务器端）写一个桌面弹幕程序，因此需要实现透明窗体和自动全屏，做法如下：

在主视图的<Window>标签内编辑如下：

```
<Window x:Class="AppName.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Height="auto" Width="auto" 
        Background="{x:Null}" WindowStyle="None" AllowsTransparency="True"
>
```

在主视图的初始化函数之后加入

```
public MainWindow()
{
    InitializeComponent();
    this.Width = System.Windows.SystemParameters.PrimaryScreenWidth;
    this.Height = System.Windows.SystemParameters.PrimaryScreenHeight;
}
```

即可实现。
