---
title: Python静态方法和动态方法
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-16 13:53:43
tags: 
  - OOP
sticky: 
---

# python的静态方法和动态方法

目录：
- [python的静态方法和动态方法](#python的静态方法和动态方法)
    - [实例方法](#实例方法)
    - [类方法](#类方法)
    - [静态方法](#静态方法)
    - [实例](#实例)

### 实例方法
定义：第一个参数必须是实例对象，该参数名一般约定为“self”，通过它来传递实例的属性和方法。  

调用：只能由实例对象调用。
### 类方法
定义：使用装饰器@classmethod。第一个参数必须是当前类对象，该参数名一般约定为“cls”，通过它来传递类的属性和方法。  

调用：实例对象和类对象都可以调用。
### 静态方法
定义：使用装饰器@staticmethod。参数随意，没有self和cls参数，但是方法体中不能使用类或实例的任何属性和方法。  

调用：实例对象和类对象都可以调用。

### 实例
```py
class Foo(object):
    # 定义了实例方法
    def test1(self):
        print("object:这里定义了实例方法")

    # 定义了类方法
    @classmethod
    def test2(clss):
        print("class：这里定义了类方法")

    # 定义了静态方法
    @staticmethod
    def test3():
        print("static：这里定义了静态方法")

if __name__ == '__main__':
    obj = Foo()
    
    obj.test1()
    
    Foo.test2()
    obj.test2()
    
    Foo.test3()
    obj.test3()
```
输出：
```py
object:这里定义了实例方法

class：这里定义了类方法
class：这里定义了类方法

static：这里定义了静态方法
static：这里定义了静态方法
```