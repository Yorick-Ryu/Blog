---
title: Python可变参数与关键字参数
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-14 20:16:02
tags: 
sticky: 
---

# 可变参数和关键字参数 
Variable Parameter & Keyword Argument 

参考：
- [简书](https://www.jianshu.com/p/98f7e34845b5)
- [廖大](https://www.liaoxuefeng.com/wiki/1016959663602400/1017261630425888)

### 可变参数：

实例：

```py
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
```
定义函数`cala()`，`*numbers`即为可变参数，在函数内部，参数`numbers`接收到的是一个`tuple`（元组），因此，函数代码完全不变。但是，调用该函数时，可以传入任意个参数，包括0个：
```py
calc(1,2)
# 5
calc()
# 0
```

把`list`或`tuple`的元素变成可变参数传进去：

```py
nums = [1, 2, 3]
calc(*nums)
# 14
```

### 关键字参数
实例：
```py
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
```

函数`person`除了必选参数`name`和`age`外，还接受关键字参数`kw`：
```py
person('Adam', 35, gender='M', job='Engineer')
# name: Adam age: 35 other: {'gender': 'M', 'job': 'Engineer'}
```
另外`person()`也接受`dict`类型参数：
```py
extra = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, city=extra['city'], job=extra['job'])
# name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
```
简化：
```py
extra = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, **extra)
# name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
