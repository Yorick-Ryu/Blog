---
title: Python__name__属性
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-15 22:04:14
tags: 
sticky: 
---

# python的__name__方法

`__name__`属性是Python的一个内置属性，记录了一个字符串。
若是在当前文件，`__name__` 的值是`__main__`。
若该文件被别的文件当模块导入(import)，`__name__`是模块名。
所以用下面的语句判断该文件的执行者，pass通常用测试代码替换掉。
```py
if __name__ == '__main__':
    pass
```
