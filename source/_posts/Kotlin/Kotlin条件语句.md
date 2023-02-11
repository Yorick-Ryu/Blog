---
title: Kotlin条件语句
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-04 22:38:07
tags: 
sticky: 
---

## 条件语句

- [条件语句](#条件语句)
  - [if/else if表达式](#ifelse-if表达式)
  - [range表达式](#range表达式)
  - [when表达式](#when表达式)
  - [string模板](#string模板)

### if/else if表达式

同Java

### range表达式

in A..B，in关键字用来检查某个值是否在指定范围之内。

```kotlin
val age = 4
if (age in 0..3){
    println("婴幼儿")
}else{
    println("少儿")
}
```
否定：
```kotlin
if (age !in 0..3){
    println("少儿")
}
```

### when表达式

允许你编写条件式，在某个条件满足时，执行对应的代码。

只要代码包含else if分支，都建议改用when表达式。

类似switch case，但是更简洁。

```kotlin
val school = "小学"
val level = when(school){
    "学前班" -> "幼儿"
    "小学" -> "少儿"
    "中学" -> "青少年"
    else -> {
        println("未知")
    }
}
println(level)
```

### string模板

模板支持在字符串的引号内放入变量值。

还支持字符串里计算表达式的值并插入结果，添加在`${}`中的任何表达式，都会作为字符串的一部分求值。

```kotlin
fun main() {
    val origin = "Jack"
    val dest = "Rose"
    println("$origin love $dest")
    val flag = true
    println("Answer is: ${if (flag) "我愿意" else "对不起"}")
}
```
输出：
```kotlin
Jack love Rose
Answer is: 我愿意
```