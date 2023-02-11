---
title: Kotlin变量、常量与数据类型
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-04 18:08:40
tags: 
sticky: 
---

## 变量、常量与数据类型
- [变量、常量与数据类型](#变量常量与数据类型)
  - [声明变量](#声明变量)
  - [内置数据类型](#内置数据类型)
  - [类型推断](#类型推断)
  - [编译时常量](#编译时常量)
  - [Kotlin的引用类型与基本数据类型](#kotlin的引用类型与基本数据类型)

### 声明变量

```kotlin
       var        max   :    Int      =     5;
// 变量定义关键字 变量名  : 类型定义 赋值运算符 赋值;
```
声明可变变量关键字：`var`
声明只读变量关键字：`val`

### 内置数据类型

|类型|描述|示例|
|---|---|---|
|String|字符串|"Hello World"|
|Char|单字符|'A'|
|Boolean|true false|true false|
|Int|整数|5|
|Double|小数|3.14|
|List|元素集合|1,8,10 "Jack","rose","Jack"|
|Set|无重复元素的集合|"Jack","Jason","Jacky"|
|Map|键值对集合|"small" to 5, "medium" to 8, "large" to 9|

### 类型推断

允许省略类型定义，如：
```kotlin
var name = "Yorick"; 
```
### 编译时常量

只读变量并非绝对只读。

编译时常量只能在函数之外定义，因为编译时常量必须在编译时赋值，而函数都是在运行时才调用，函数内的变量也是在运行时赋值，编译时常量要在这些变量赋值前就已存在。

编译时常量只能是常见的基本数据类型：String、Int、Double、Float、Long、Short、Byte、Char、Boolean。

### Kotlin的引用类型与基本数据类型

Java有两种数据类型：引用类型与基本数据类型。

Kotlin只提供引用类型这一种数据类型，出于更高性能的需要，Kotlin编译器会在Java字节码中改用基本数据类型。
