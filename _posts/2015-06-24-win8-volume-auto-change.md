---
layout: post
title: "Win8.1 音量自动变化"
date: 2015-06-24
categories: 
  - "mswindows"
---

系统环境：Windows 8.1 Pro Update 1

自从用了Windows 8 系统之后，听音乐时会感到有明显的音量变化，一直不明白是怎么回事。声卡驱动已经正确安装，音量设置也保持不变。

实际上这是Windows 8系统的一个特性，当系统检测到有通信活动时自动降低了系统音量，只是这个对通信活动的检测似乎有一点逻辑上的不足，导致了实际使用体验中的奇怪现象。

要关掉这个特性，只要右击通知栏里的音量图标，选择"播放设备"，把自动降低音量的设置禁用即可。

\---- English Version ---- Actually, I use English language setting and I don't know the exact Chinese translation of "Playback devices". Here is the English version of this blog.

System Environment: Windows 8.1 Pro Update 1

Since I started using Windows 8, I have encountered the problem more than once that the system sound volume changed automatically when I am listening to music. The driver of sound device has been installed correctly and the sound volume has been kept constant.

In fact, it's a feature of Windows 8. When Windows detects communications activity, it reduces the volumes of other sounds by 80%. However, the detection of communications activity seems not to be good enough, which causes the strange problem.

To disable this feature, we can right-click the sound volume icon in the tray area and select "Playback devices". Then we can select the option "Do Nothing" and disable this feature.
