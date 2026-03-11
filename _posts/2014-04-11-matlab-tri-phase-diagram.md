---
layout: post
title: "已知平衡数据利用Matlab作三元相图"
date: 2014-04-11
categories: [matlab]
---

需准备：

平衡线数据，连接线数据

1.作直角三角形相图

```
%limitline.csv 三列数据依次为平衡线上各点S,B,A的质量分数
%tieline.csv 六列数据依次为连接线上两点的S,B,A的质量分数
MLine = csvread('limitline.csv');
TLine = csvread('tieline.csv');
MLine = MLine ./100;
TLine = TLine ./100;
X = 0:0.01:1;
Y = interp1(MLine(:,1),MLine(:,3),X,'cubic');

plot([0,1],[1,0]);hold on;
plot(X,Y),axis([0 1 0 1]),axis equal,axis square

pointNumber = size(TLine);

for k = 1:pointNumber(1)
plot([TLine(k,1),TLine(k,4)],[TLine(k,3),TLine(k,6)])
end
```

 

2.作等边三角形相图

```
%limitline.csv 三列数据依次为平衡线上各点S,B,A的质量分数
%tieline.csv 六列数据依次为连接线上两点的S,B,A的质量分数
MLine = csvread('limitline.csv');
TLine = csvread('tieline.csv');
MLine = MLine ./100;
TLine = TLine ./100;
X = 0:0.01:1;
Y = interp1(MLine(:,1)+0.5*MLine(:,3),MLine(:,3)*sqrt(3)/2,X,'cubic');

plot([0,0.5],[0,sqrt(3)/2]);hold on;
plot([1,0.5],[0,sqrt(3)/2]);hold on;
plot(X,Y),axis([0 1 0 1]),axis equal,axis square

pointNumber = size(TLine);

for k = 1:pointNumber(1)
plot([TLine(k,1)+0.5*TLine(k,3),TLine(k,4)+0.5*TLine(k,6)]，[TLine(k,3)*sqrt(3)/2,TLine(k,6)*sqrt(3)/2])
end
```
