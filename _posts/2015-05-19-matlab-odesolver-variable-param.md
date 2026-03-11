---
layout: post
title: "Matlab求解变参数常微分方程组"
date: 2015-05-19
categories: 
  - "matlab"
---

以下代码在Matlab R2010a运行通过。

待求解函数示例：

```
function dx = r1( t, x, k )
    dx = -k*x;
end
```

k为可变参数。

求解主程序：

```
sol = ode45(@r1, [0,10], 1, [], 1)
deval(sol, [2], 1)
```

如上所示，在调用ODE solver时，格式为 solver(odefun, \[t0 tfinal\], y0, options, args...) 其中 args... 为可变参数，将被转发至待求解的方程中。

Matlab的自带帮助中并没有明确说明ODE solver支持这样的调用形式，不过这样的调用形式是符合Matlab函数定义的习惯的。上例中，ode45函数的最后一个参数(args...)为1，该参数被转发至待求解的方程中作为参数k。

上述求解过程使用了 deval() 来返回t=2时的结果，此函数的第一个实参是sol，是一个structure，要让ODE solver返回该类型，则ODE solver必须采用函数句柄的方式输入待求解的函数，若使用inline函数将无法返回该structure而仅返回积分区间。关于该structure的具体定义可查看Matlab帮助。
