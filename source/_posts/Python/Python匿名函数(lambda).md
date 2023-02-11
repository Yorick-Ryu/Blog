---
title: Python匿名函数(lambda)
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-18 16:00:49
tags: 
  - lambda
sticky: 
---

# Python lambda表达式（匿名函数）

参考链接：
- [Python lambda表达式（匿名函数）及用法](http://c.biancheng.net/view/2262.html)
- [匿名函数](https://www.liaoxuefeng.com/wiki/1016959663602400/1017451447842528)

语法格式：
```py
name = lambda [list] : 表达式
```
其中，定义 lambda 表达式，必须使用 lambda 关键字；[list] 作为可选参数，等同于定义函数是指定的参数列表；name 为该表达式的名称。
转换成普通函数的形式:
```py
def name(list):
    return 表达式
```
实例：
```py
fun = lambda x: x * x
print(fun(5))
# 25
```
相当于：
```py
def fun(x):
    return x * x
print(fun(5))
# 25