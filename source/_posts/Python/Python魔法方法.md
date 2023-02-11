---
title: Python魔法方法
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-17 16:05:22
tags: 
sticky: 
---

# Python的魔法方法

目录：
- [Python的魔法方法](#python的魔法方法)
    - [构造方法`__new__`](#构造方法__new__)
    - [`__str__`和`__repr__`](#__str__和__repr__)
    - [`__getattr__`、`__setattr__`和`__delattr__`](#__getattr____setattr__和__delattr__)

参考链接：
- [Python魔法方法指南](https://url.cy/0wKANr)
- [Python常用魔术方法一览表](http://c.biancheng.net/view/7817.html)
- [Python 魔法方法](https://blog.csdn.net/yusuiyu/article/details/87945149)

Python中的魔法方法像是Java中的重载，Python中的魔法方法可以理解为：对类中的内置方法的重载，注意这里不是重写。

下面列出部分常用的方法：

### 构造方法`__new__`

[__init__方法](./__new__%E6%96%B9%E6%B3%95.md)

###  `__str__`和`__repr__`

`__str__`定义对类的实例调用`str()`时的行为。而`__repr__`定义对类的实例调用`repr()`的行为，这两者的区别就是`repr`面向开发者，`str`面向用户。定义类的输出的时候经常会使用这两个其中的魔法。

实例：
```py
class Apple(object):

    def __init__(self,name,weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return '{}:{}'.format(self.name,self.weight)

print(Apple('A','30g'))
# 输出；A:30g
```
这里可以看见`__str__`起作用了，但是如果我们在命令行里运行`Apple('A','30g')`的话，输出的可能是：
```py
<__main__.Apple object at 0x000001785036DEE0>
```
因为这里是`__repr__控制的`，修改Apple类，添加`__repr__ = __str__`则可以输出：
```py
A:30g
```
### `__getattr__`、`__setattr__`和`__delattr__`

`__getattr__`定义对象访问不存在的属性或方法时的行为(对象访问不存在的属性或者调用方法时调用)
`__setattr__`定义对属性或方法进行修改操作时的行为,在实例化的时候，会在`__init__`里初始化，对value的属性值进行了设置，这时候会调用`__setattr__`方法。
需要注意的地方是，在重写`__setattr__`方法的时候千万不要重复调用造成死循环。
`__delattr__`定义定义删除属性时的行为

实例：
可以参考[ORM框架](./orm.md)的`Model`类
```py
class Apple(object):
    def __init__(self, name, weight):
        print("进入__init__初始化对象属性")
        self.name = name
        self.weight = weight

    def __getattr__(self, attr):
        return "不存在{}属性".format(attr)

    def __setattr__(self, name, value):
        print("正在生成实例化对象的{}属性，值为{}".format(name, value))
        object.__setattr__(self, name, value)
        return "正在生成实例化对象的{}属性，值为{}".format(name, value)

    def __delattr__(self, attr: str) -> None:
        print("正在删除{}属性".format(attr))
        object.__delattr__(self, attr)


a = Apple("A", "30g")
print("a.name:",a.name)
print("a.weight",a.weight)
print(a.key)
del a.name
del a.weight
print(a.name,a.weight)
```
结果：
```py
进入__init__初始化对象属性
正在生成实例化对象的name属性，值为A
正在生成实例化对象的weight属性，值为30g
a.name: A
a.weight 30g
不存在key属性
正在删除name属性
正在删除weight属性
不存在name属性 不存在weight属性
```