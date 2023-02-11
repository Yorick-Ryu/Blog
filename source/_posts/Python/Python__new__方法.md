---
title: Python__new__方法
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-15 21:52:32
tags: 
sticky: 
---

# python的__new__方法

### 什么是__new__方法

在Python中`__new__`方法与`__init__`方法类似，但是如果两个都存在那么`__new__`先执行。

`__new__`方法的返回值是

可以将类比作制造商，`__new__`方法就是前期的原材料购买环节，init方法就是在有原材料的基础上，加工，初始化商品环节。


实例：
```py
class Person(object):
  
    def __init__(self, name, age):
        self.name = name
        self.age = age
     
    def __new__(cls, name, age):
        if 0 < age < 150:
            return object.__new__(cls)
            # return super(Person, cls).__new__(cls)
        else:
            return None
  
    def __str__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.__dict__)
  
print(Person('Tom', 10))
print(Person('Mike', 200))
```
结果：
```py
Person({'age': 10, 'name': 'Tom'})
None # 注意此时__init()__没被执行
```
执行过程：

1. 当执行`Person('Tom',10)`时，实例化类，`name='Tom',age='10'`被当作参数带入`__new__`方法，参数cls表示需要实例化的类，即Person,这里由Python解析器自动提供.
2. `__new__`方法会返回Person类的一个实例，通常是其父类new出来的实例，或者直接是`object`的new出来的实例。
3. 然后利用这个实例来调用类的`__init__`方法，如果`__new__`方法返回`None`，则`__init__`方法不会被执行。

### 什么时候需要__new__

`__new__`方法主要是当你继承一些不可变的class时(比如int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。还有就是实现自定义的`metaclass`。

实例：
定义一个只能输出正数的整数类型:
```py
class PositiveInteger(int):
    def __new__(cls, value):
        return super(PositiveInteger, cls).__new__(cls, abs(value))

i = PositiveInteger(-3)
print(i)
# 输出：3
```