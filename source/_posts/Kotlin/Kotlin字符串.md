---
title: Kotlin字符串
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-07 15:11:48
tags: 
  - String
  - 字符串
sticky: 
---

## 字符串

[TOC]

### 字符串截取

#### substring

substring函数支持IntRange类型（表示一个整数范围的类型）的参数，until创建的范围不包括上限值。

```kotlin
const val NAME = "Jerry Smith"
fun main() {
    val index = NAME.indexOf(" ")
    // Java方式
    var str = NAME.substring(0, index)
    println(str)
    // Kotlin方式
    str = NAME.substring(0 until index)
    println(str)
}
// 输出
// Jerry
// Jerry
```

#### split

split函数返回的是List集合数据，List集合又支持解构语法特性，它允许你在一个表达式里给多个变量赋值，解构常用来简化变量的赋值。
```kotlin
const val NAMES = "Jerry,Morty,Yorick"
fun main() {
    val data = NAMES.split(",")
    // data[0]

    // 结构语法
    val (origin, dest, proxy) = NAMES.split(",")
    println("$origin $dest $proxy")
}
// 输出
// Jerry Morty Yorick
```

### 字符串操作

replace 字符串替换
```kotlin
fun main() {
    val str = "The People's Republic of China"
    val reStr = str.replace(Regex("[anxious]")) {
        when (it.value) {
            "a" -> "6"
            "n" -> "3"
            "x" -> "2"
            "i" -> "5"
            "o" -> "4"
            "u" -> "0"
            "s" -> "7"
            else -> it.value
        }
    }
    println(str)
    println(reStr)
}
// 输出
// The People's Republic of China
// The Pe4ple'7 Rep0bl5c 4f Ch536
```

### 字符串比较

在Kotlin中，用`==`检查两个字符串中的字符是否匹配，用`===`检查两个变量是否指向内存堆上同一对象。而在Java中`==`做引用比较（是否为同一对象），做内容比较时用`equals`方法。


```kotlin
fun main() {
    val str1 = "Yorick"
    val str2 = "Yorick"
    println(str1==str2)
    println(str1===str2)
}
// 输出
// true
// true
```

```kotlin
fun main() {
    val str1 = "Yorick"
    val str2 = "yorick".capitalize()
    println(str1 == str2)
    println(str1 === str2)
}
```

### Unicode

### 遍历字符

forEach

```kotlin
fun main() {
    val str1 = "Yorick"
    val str2 = "yorick".capitalize()
    println(str1 == str2)
    println(str1 === str2)
    str1.forEach {
        print("$it * ")
    }
}
// 输出
// Y * o * r * i * c * k * 
```

### 格式化字符串

[在 Kotlin 中格式化字符串 | D栈 - Delft Stack](https://www.delftstack.com/zh/howto/kotlin/kotlin-string-format/)