---
title: Python复习
tags:
  - 复习
  - 课程笔记
index_img: /img/default.png
categories:
  - Python
date: 2023-02-13 14:17:46
sticky:
---

- [Python复习](#python复习)
  - [语法基础](#语法基础)
    - [标识符和关键字](#标识符和关键字)
      - [标识符](#标识符)
      - [关键字](#关键字)
    - [变量和数据类型](#变量和数据类型)
      - [数据类型](#数据类型)
      - [变量](#变量)
    - [字符串](#字符串)
      - [格式化](#格式化)
      - [索引(下标)](#索引下标)
      - [切片(顾头不顾尾)](#切片顾头不顾尾)
      - [跳取](#跳取)
      - [首字母大写](#首字母大写)
      - [全部大写](#全部大写)
      - [全部小写](#全部小写)
      - [大小写互换](#大小写互换)
      - [标题化](#标题化)
      - [查找](#查找)
      - [删除字符串前后的空格/字符](#删除字符串前后的空格字符)
      - [计算某字符/字符串的个数](#计算某字符字符串的个数)
      - [分割字符串](#分割字符串)
      - [替换字符串](#替换字符串)
      - [字符串拼接](#字符串拼接)
    - [运算符](#运算符)
    - [列表(list)](#列表list)
      - [插入元素](#插入元素)
      - [删除元素](#删除元素)
      - [排序](#排序)
      - [列表推导式](#列表推导式)
    - [元组(tuple)](#元组tuple)
    - [字典(dict)](#字典dict)
      - [增加元素](#增加元素)
      - [访问键和值](#访问键和值)
    - [集合(set)](#集合set)
      - [创建set](#创建set)
      - [添加元素](#添加元素)
      - [删除元素](#删除元素-1)
  - [函数](#函数)
    - [匿名函数](#匿名函数)
  - [文件读写](#文件读写)
      - [读文件](#读文件)
      - [写文件](#写文件)
    - [异常](#异常)


# Python复习

一种解释型动态语言，语法简洁优雅但是性能低。

## 语法基础

### 标识符和关键字

#### 标识符

1. 区分大小写

2. 关键字不能作为标识符。

3. 标识符首位可以用下画线“_”但是**不可以是数字**。

4. 除去首字母，其他位可以使用下画线“_”，数字和字母。

5. 不能使用内置函数作为标识符。

#### 关键字

```python
>>> import keyword
>>> keyword.kwlist
['False', 'None', 'True', '__peg_parser__', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
```

| 1        | 2    | 3     | 4      | 5        | 6        | 7     | 8     | 9      | 10    |
| -------- | ---- | ----- | ------ | -------- | -------- | ----- | ----- | ------ | ----- |
| False    | None | True  | and    | assert   | as       | async | await | break  | class |
| continue | def  | elif  | else   | except   | finally' | for   | from  | global | if    |
| import   | in   | is    | lambda | nonlocal | not      | or    | pass  | raise  | try   |
| while    | with | yield |        |          |          |       |       |        |       |

### 变量和数据类型

#### 数据类型

- 整数 ，允许在数字中间以`_`分隔`10_000_000_000`=`10000000000`

- 浮点数，运算可能会有四舍五入的误差

- 字符串，`""`和`''`等价，常用转义：

  ```txt
  \'表示单引号
  \"表示双引号
  \n表示换行
  \t表示制表符
  \\表示的\
  %%表示一个%
  ```
  
  `r''`表示`''`内部的字符串默认不转义
  
  用`'''...'''`的格式表示多行内容

- 布尔值：`True` or `False` 

  使用或`or`且`and`非`and`运算

- 空值：None

#### 变量

- 变量可以是任意数据类型。

- 变量本身类型不固定。

### 字符串

#### 格式化

1. 占位符

    ```py
    >>> 'Hi, %s, you have $%d.' % ('Yorick', 1000000)
    'Hi, Yorick, you have $1000000.'
    ```

    | 占位符 | 替换内容     |
    | :----- | :----------- |
    | %d     | 整数         |
    | %f     | 浮点数       |
    | %s     | 字符串       |
    | %x     | 十六进制整数 |

2. format()

    ```python
    >>> 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)
    'Hello, 小明, 成绩提升了 17.1%'
    ```

3. f-string

    ```python
    >>> r = 2.5
    >>> s = 3.14 * r ** 2
    >>> print(f'The area of a circle with radius {r} is {s:.2f}')
    The area of a circle with radius 2.5 is 19.62
    ```

#### 索引(下标)

```python
s = 'ABCDEFGHIJKLMN'
s1 = s[0]
print('s[0] = ' + s1)   #s[0] = A
print('s[3] = '+ s[3])  #s[3] = D
print('倒数第三个数为：' + s[-3])   #倒数第三个数为：L
print('最后一个数为：' + s[-1])     #最后一个数为：N
```

#### 切片(顾头不顾尾)

截取一部分字符串

```python
s = 'ABCDEFGHIJKLMN'
s2 = s[0:3]
print('s[0:3] = ' + s2)     
# s[0:3] = ABC

print('整个字符串如下：' + s[:])    
# 整个字符串如下：ABCDEFGHIJKLMN

print('整个字符串如下：' + s[0:])   
# 整个字符串如下：ABCDEFGHIJKLMN

print('前两个字符：' + s[:2])      
# 前两个字符：AB
```

#### 跳取

`s[首:尾:步长]`

```python
s3 = 'ABCDEFGHIJKLMN'
print(s3[0:6:2])    #ACE
print(s3[::2])      #ACEGIKM
print(s3[4:0:-1])   #倒着取:EDCB
print(s3[3::-1])    #DCBA
print(s3[-1::-1])   #NMLKJIHGFEDCBA
```

#### 首字母大写

`capitalize()`

```python
s = 'yorick'
s4_1 = s.capitalize()  #首字母大写
print(s4_1)   #Yorick
```

#### 全部大写

`upper()`

```python
s = 'yorick'
s4_2 = s.upper() #全部大写
print(s4_2)   #YORICK
```

#### 全部小写

`lower()`

```python
s = 'YoRick'
s4_3 = s.lower() #全部小写
print(s4_3)   #yorick
```

#### 大小写互换

`swapcase()`

```python
s = 'alexWUsir'
s4_4 = s.swapcase() #大小写互换
print(s4_4)   #ALEXwuSIR
```

#### 标题化

`title()`

非字母后的第一个字母将转换为大写字母

```python
str = "this is string example from yorick....wow!!!"
print (str.title())
# This Is String Example From Yorick....Wow!!!
s = "HAPPY BIRTHDAY"
print(s.title())
# Happy Birthday
```

#### 查找

`find()`通过元素找索引，找到返回索引，找不到返回`-1`
`index()`通过元素找索引，找到返回索引，找不到返回`error`

```python
str = "yorick"
res1 = str.find('c') 
print("str.find('c') =",res1)
# str.find('c') = 4
res2 = str.find('p')
print("str.find('p') =",res2)
# str.find('p') = -1
res3 = str.index('c')
print("str.index('c') =",res3)
# str.index('c') = 4
res4 = str.index('p')
print("str.index('p') =",res4)
# ValueError: substring not found
```

`if i in str:`

```python
print('----------------检验非法（敏感）字符-------------------')
s = 'gcu木木gckhb'
if '木木' in s:
    print('您的评论有敏感字符')
```

#### 删除字符串前后的空格/字符

```python
s = '  alexW%Usir  %2%  '
s9_1 = s.strip()   
# 删除字符串前后的空格

print(s9_1)   
#alexW%Usir  %2%

ss = '% alexW%Usir  %2%  %'
s9_2 = ss.strip('%')   
# 删除字符串前后的%

print(s9_2)  
# alexW%Usir  %2%　　
```

#### 计算某字符/字符串的个数

```python
s = 'alexaa wusirl'
s10 = s.count('a')
print('此字符串中有' + s10 + '个a')   
# 报错：TypeError: must be str, not int

print('此字符串中有' + str(s10) + '个a')    
# 此字符串中有3个a
```

#### 分割字符串

`split() : str -> list`

```python
s = 'alex wusir taibai'
s1 = 'ale:x wus:ir :taibai'
s11_1 = s.split()
print(s11_1)    #['alex', 'wusir', 'taibai']
s11_2 = s1.split(':')

print(s11_2)   #['ale', 'x wus', 'ir ', 'taibai']
```

#### 替换字符串

`replace()`

```python
s13_0 = '小明，哈喽你好，我是小明'
s13_1 = s13_0.replace('小明','')
s13_2 = s13_0.replace('小明','张三')
s13_3 = s13_0.replace('小明','张三',1)

print(s13_1)
# ，哈喽你好，我是
print(s13_2)
# 张三，哈喽你好，我是张三
print(s13_3)
# 张三，哈喽你好，我是小明
```

#### 字符串拼接

使用`,`拼接，会用空格分隔

使用`+`拼接，不会用空格分隔

```python
str1 = "hello"
str2 = "yorick"
print(str1,str2)
# hello yorick
print(str1+str2)
# helloyorick
```

### 运算符

条件判断

```python
if <条件判断1>:
    <执行1>
elif <条件判断2>:
    <执行2>
elif <条件判断3>:
    <执行3>
else:
    <执行4>
```

### 列表(list)

有序

`classmates = ['Michael', 'Bob', 'Tracy']`

#### 插入元素

追加元素到末尾

```python
classmates.append('Adam')
classmates.append('Adam')
print(classmates)
# ['Michael', 'Bob', 'Tracy', 'Adam']
```

插入到指定的位置

```python
classmates.insert(1, 'Jack')
print(classmates)
# ['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']
```

#### 删除元素

删除list末尾的元素，用`pop()`方法：

```python
classmates.pop()
print(classmates)
['Michael', 'Jack', 'Bob', 'Tracy']
```

要删除指定位置的元素，用`pop(i)`方法，其中`i`是索引位置：

```python
classmates.pop(1)
print(classmates)
['Michael', 'Bob', 'Tracy']
```

#### 排序

`sort()`

```python
s = [93,95,86,98,99,99,89,100,100,97]
print("原列表：",s)
s.sort()
print("升序：",s)
s.sort(reverse=True)
print("降序：",s)
# 原列表： [93, 95, 86, 98, 99, 99, 89, 100, 100, 97]
# 升序： [86, 89, 93, 95, 97, 98, 99, 99, 100, 100]
# 降序： [100, 100, 99, 99, 98, 97, 95, 93, 89, 86]
```

#### 列表推导式

效率>普通for循环

`[表达式 for 迭代变量 in 可迭代对象 [if 条件表达式] ]`

```python
a_range = range(10)
# 对a_range执行for表达式
a_list = [x * x for x in a_range]
# a_list集合包含10个元素
print(a_list)
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

```python
 '''
语法一：
    exp1：在for循环中，如果x的值满足条件表达式condition(即条件表达式成立)，返回exp1；条件表达式不成立则不返回
    x：for循环中变量
    data：一个序列（比如：列表/元组/字符串等）
    condition：条件表达式
'''
[exp1 for x in data if condition]
'''
语法二：
    exp1：在for循环中，如果x的值满足条件表达式condition(即条件表达式成立)，返回exp1；条件表达式不成立则返回exp2
    condition：条件表达式
    exp2：在for循环中，如果x的值满足条件表达式condition(即条件表达式成立)，返回exp1；条件表达式不成立则返回exp2
    x：for循环中变量
    data：个序列（比如：列表/元组/字符串等）
'''
[exp1 if condition else exp2 for x in data]
```

 示例：获取 0 ~ 20 的所有偶数并且乘以 10，并返回所有计算之后的结果

```python
list1 = [x*10 for x in range(0,21) if x%2 == 0] 
print(list1)
print(type(list1))
'''
输出结果：
[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
<class 'list'>
'''
```

 将 0 ~ 20 的偶数乘以 10 ，奇数乘以 100 ，并返回所有计算之后的结果。

```py
list2 = [x*10 if x%2 == 0 else x*100 for x in range(0,21) ]
print(list2)
print(type(list2))
'''
输出结果：
[0, 100, 20, 300, 40, 500, 60, 700, 80, 900, 100, 1100, 120, 1300, 140, 1500, 160, 1700, 180, 1900, 200]
<class 'list'>
'''
```

### 元组(tuple)

有序，tuple和list非常类似，但是tuple一旦初始化就不能修改。没有append()，insert()这样的方法。其他获取元素的方法和list一样。

`classmates = ('Michael', 'Bob', 'Tracy')`

### 字典(dict)

键值对形式存储数据，键不可重复（相同键会重写值）。

```python
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Michael']) # 95
print(d.get('Michael')) # 95
```

也可以这样创建字典

```python
thisdict = dict(name = "John", age = 36, country = "Norway")
print(thisdict)
```

#### 增加元素

```python
d['Yorick'] = 99
print(d)
# {'Michael': 95, 'Bob': 75, 'Tracy': 85, 'Yorick': 99}
```

#### 访问键和值

`d.keys()`

```python
>>> d = {'a': 10, 'b': 20, 'c': 30}
>>> d
{'a': 10, 'b': 20, 'c': 30}

>>> list(d.keys())
['a', 'b', 'c']
```

`d.values()`

```python
>>> d = {'a': 10, 'b': 20, 'c': 30}
>>> d
{'a': 10, 'b': 20, 'c': 30}

>>> list(d.values())
[10, 20, 30]
```

删除元素

```python
d.pop('Bob')
print(d)
# {'Michael': 95, 'Tracy': 85, 'Yorick': 99}
```

### 集合(set)

set和dict类似，也是一组key的集合，但不存储value。在set中，没有重复的key。

#### 创建set

要创建一个set，需要提供一个list作为输入集合：

```python
s = set([1, 1, 2, 2, 3, 3])
print(s)
# {1, 2, 3}
```

#### 添加元素

`s.add()`

#### 删除元素

`s.remove(key)`

## 函数

### 匿名函数

```python
L = list(filter(lambda n: n % 2 == 1, range(1, 20)))
print(L)
# [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
```

## 文件读写

#### 读文件

hello.txt

```
Hello World
```

```python
f = open(r'C:\Users\yurui\Desktop\test\py\hello.txt','r')
content = f.read()
print(content)
f.close()
# Hello World
```

使用with，自动调用`close()`

```python
with open(r'C:\Users\yurui\Desktop\test\py\hello.txt','r') as f:
    content = f.read()
    print(content)
    
# Hello World
```

要读取非UTF-8编码的文本文件，需要给`open()`函数传入`encoding`参数，例如，读取GBK编码的文件：

```python
f = open(r'C:\Users\yurui\Desktop\test\py\hello.txt', 'r', encoding='gbk')
```

#### 写文件

写文件和读文件是一样的，唯一区别是调用`open()`函数时，传入标识符`'w'`或者`'wb'`表示写文本文件或写二进制文件：

```python
>>> f = open('/Users/michael/test.txt', 'w')
>>> f.write('Hello, world!')
>>> f.close()
```

```python
with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')
```

### 异常

[python 异常捕获方法总结](https://zhuanlan.zhihu.com/p/321408784)

```python
try:
    print('try...')
    r = 10 / int('2')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
else:
    print('no error!')
finally:
    print('finally...')
print('END')
```

