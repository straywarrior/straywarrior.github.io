---
layout: post
title: "if(cin)和while(cin)的用法"
date: 2015-01-24
categories: 
  - "corcpp"
---

近日学习C++ Primer(5th Edition)过程中纠正了一直以来对cin用法的一个误区。

问题源于C++ Primer书的习题7.13：用istream构造函数重写7.1.1节中的Sales\_data类程序。

原书程序如下：

```
Sales_data total;
cout << "Please input ISBN, Units_sold, Price: " << endl;
if (read(cin, total)){
    cout << cin.fail() << endl;
    Sales_data trans;
    while(read(cin, trans)){
        if (total.isbn() == trans.isbn())
            total.combine(trans);
        else {
            print(cout,total) << endl;
            total = trans;
        }
        print(cout, total) << endl;
    }
}else{
    cerr << "No data?" << endl;
}
```

本人最初改写后的程序如下：

```
cout << "Please input ISBN, Units_sold, Price: " << endl;
if (cin){
    Sales_data total = Sales_data(cin); 
    while(cin){
        Sales_data trans = Sales_data(cin);
        if (total.isbn() == trans.isbn())
            total.combine(trans);
        else {
            print(cout,total) << endl;
            total = trans;
        }
        print(cout, total) << endl;
        cin.sync();
        cin.clear();
    }
}else{
    cerr << "No data?" << endl;
}
```

开始调试，在输入数据后出现问题，Ctrl+Z不能中断数据输入，即while循环始终执行。断点调试后发现if(cin)始终为真。

一种常用的未知个数数据的输入方式如下：

```
int i;
while(cin >> i)
{
    /*....*/
}
```

显然这种数据输入方式并不会碰到前面所说的问题。

这个问题实际上是对cin的理解造成的。cin本身是个stream类型，它如何转换为bool类型从而作为while()的条件进行判断呢？

从C++的头文件定义中可以找到，cin是来自于istream头文件，其类继承关系为ios\_base -> basic\_ios -> basic\_istream。而在基类ios\_base类(定义在xiosbase头文件)中，定义了两个重载函数。operator void \*() const和bool operator!() const。

```
operator void*() const  
{ return this->fail() ? 0 : (void*)this; } 
bool operator!() const  
{ return this->fail(); }
```

也就是说，当执行if(cin)时，先将cin执行(void \*)强制转换，再转换为bool类型，相当于while()中的判定最终隐式调用了(!cin.fail())，而这个fail()是指示cin的状态的。什么是cin的状态？实际上，cin有4个标志位，分别是badbit，failbit，eofbit，goodbit。其中，badbit，failbit任意一个被置位时，调用fail()将返回true，因此只有eofbit被置位时fail()返回false，!fail()将返回true。即使什么都不输入，cin也处于有效的状态（将cin置于有效状态即是是cin.clear()所做的事情），所以if(cin)总是成立。而对cin执行位移运算符>>时情况就完全不同了，因为输入缓冲区内没有数据，因此系统即要求用户从键盘输入数据，if(cin >> i)或while(cin >> i)在输入了数据之后才会判断执行。

因此，最终程序修改代码如下：

```
cout << "Please input ISBN, Units_sold, Price: " << endl;
Sales_data total = Sales_data(cin);
if (cin){
    Sales_data trans = Sales_data(cin);
    while(cin){
        if (total.isbn() == trans.isbn())
            total.combine(trans);
        else {
            print(cout,total) << endl;
            total = trans;
        }
        print(cout, total) << endl;
        Sales_data trans = Sales_data(cin);
    }
}else{
    cerr << "No data?" << endl;
}
```
