---
layout: post
title: "Be careful with return-value optimization of C++ compilers"
date: 2018-01-26
categories: 
  - "corcpp"
  - "programminglanguage"
---

### Side Effect of Return-value Optimization

This "bug" is caused by return-value optimization and affects both GCC and Microsoft C/C++ Compiler. Assume that we have codes like following:

```
#include <cstdio>
class Complex {
public:
    Complex() : Complex(0.0, 0.0) {}
    Complex(double a, double b) : a(a), b(b) {}
    Complex(const Complex & x) : a(x.a), b(x.b) {
        dummy = 1.f;
    }
    Complex operator * (const Complex & x) {
        return Complex(a * x.a, b * x.b);
    }

    double a, b;
    double dummy;
};

int main() {
    Complex z1(-1, 2);
    Complex z2(3, 5);
    Complex z3 = z1 * z2;
    Complex z4 = z3;
    printf("%f %f %f\n", z3.a, z3.b, z3.dummy);
    printf("%f %f %f\n", z4.a, z4.b, z4.dummy);
    return 0;
}

```

Compile the code with g++ main.cpp -O0 -g -std=c++11. Run the program and the output result is like following:

```
-3.000000 10.000000 0.000000
-3.000000 10.000000 1.000000

```

We do declare the constructors and so the copy control of the class should be handled well by ourselves. At line 20 and line 21, there are two \= assignment symbol and they should call the same copy constructor at line 6 (not copy assignment function, which we do not declare at all). However, the result of z3 is incorrect.

Though we turn off the optimization by \-O0, the compiler still does return-value optimization. By dump the assembly using objdump -d a.out, we can discern that the copy constructor is only called once. The return value of operator \*(const Complex &) is seen as the new instance directly. Until the instance is explicitly copied again, the copy constructor is called.

So, we compile the code with g++ main.cpp -O0 -g -std=c++11 -fno-elide-constructors and run the program again. Now the output result seems to meet our expectation:

```
-3.000000 10.000000 1.000000
-3.000000 10.000000 1.000000

```

### A Further Look at the Return-Value

We can add a global counter into the copy constructor Complex(const Complex & x), just like this:

```
int g_copyctor_count = 0;
class Complex {
    Complex(const Complex & x) : a(x.a), b(x.b) {
        ++g_copyctor_count;
        dummy = 1.f;
    }
};

```

Print the counter at the end of the program and what do we get? 2? No, it's 3. By inspecting the assembly code, we can find that there is another copy construction in operator \*(const Complex &). In the code above, we just construct an object in the function body and it can not be passed directly outside the function, as it should be destroyed when it go out of the function scope. The compiler implicitly creates another temporary object to pass it outside. So we can conclude that the return-value optimization is so necessary that compilers enable it by default even if we do not enable any optimization explicitly.
