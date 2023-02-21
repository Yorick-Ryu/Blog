---
title: Python类与对象
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-15 15:21:13
tags: 
  - OOP
sticky: 
---

# Python类与对象易忘点

[参考链接](https://www.liaoxuefeng.com/wiki/1016959663602400/1017496031185408)

**目录：**
- [Python类与对象易忘点](#python类与对象易忘点)
  - [`__init()__`方法](#__init__方法)
  - [使用元类，`type()`和`metaclass`](#使用元类type和metaclass)
    - [type()](#type)
    - [metaclass(元类)](#metaclass元类)

## `__init()__`方法
注意：**两个下划线**，类似Java的构造器函数

实例：
```py
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
```
注意：`__init()__`方法的第一个参数永远是`self`，表示创建的实例本身。  

有了`__init__`方法，在创建实例的时候，就不能传入空的参数了，必须传入与`__init__`方法匹配的参数，但`self`不需要传，Python解释器自己会把实例变量传进去：
```py
yorick = Student('Yorick',88)
yorick.name
# 'Yorick'
yorick.score
# 88
```

## 使用元类，`type()`和`metaclass`

动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的。

### type()

`type()`函数既可以返回一个对象的类型，又可以创建出新的类型，比如，我们可以通过`type()`函数创建出Hello类，而无需通过`class Hello(object)...`的定义：
```py
# 先定义类的方法
def fn(self, name='world'): 
    print('Hello, %s.' % name)
# 创建Hello class
Hello = type('Hello', (object,), dict(hello=fn))
# 创建类的实例
h = Hello()
# 调用实例的方法
h.hello()
# Hello, world.
h.hello('Yorick')
# Hello, Yorick.
```
### metaclass(元类)

先定义`metaclass`，就可以创建类，最后创建实例，可以把类看成是`metaclass`创建出来的“实例”

实例：
```py
# metaclass是类的模板，所以必须从`type`类型派生：
# 按照习惯，metaclass的类名总是以Metaclass结尾
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)
```
`__new__`方法接收到的参数依次是：
1. 当前准备创建的类的对象；
2. 类的名字；
3. 类继承的父类集合；
4. 类的方法集合。

有了ListMetaclass，我们在定义类的时候还要指示使用ListMetaclass来定制类，传入关键字参数metaclass：
```py
# 继承普通list类
class MyList(list, metaclass=ListMetaclass):
    pass
```
测试一下MyList是否可以调用add()方法：
```py
L = MyList()
L.add(1)
L
# [1]
```
实例：[编写ORM](./orm.md)