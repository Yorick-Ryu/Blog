---
title: Kotlin标准库函数
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-08 10:43:04
tags: 
sticky: 
---

## 标准库函数

- [标准库函数](#标准库函数)
  - [apply](#apply)
  - [let](#let)
  - [run](#run)
  - [with](#with)
  - [also](#also)
  - [takeIf](#takeif)
  - [takeUnless](#takeunless)

### apply

apply函数可看作一个配置函数，你可以传入一个接收者，然后调用一系列配置以便它使用，如果提供lambda给apply函数执行，它会返回配置好的接收者。

```kotlin
fun main() {
    // 配置一个File实例
    val file1 = File("E://demo.txt")
    file1.setReadable(true)
    file1.setWritable(true)
    file1.setExecutable(false)
    // 使用apply
    val file2 = File("E://demo.txt").apply {
        // 这里可以省略this
        // 所有操作默认接收者为file2
        // 这也叫隐式调用
        setReadable(true)
        setWritable(true)
        setExecutable(false)
    }
}
```
### let
和上面apply差不多，但是会返回lambda函数的最后一行的结果，并赋值给接收者，但是不支持隐式调用。
```kotlin
fun main() {
    // 求集合第一个元素的平方
    val res = listOf(8, 6, 9).first().let {
        it * it
    }
    println(res)
    // 不用let
    val firstElement = listOf(8, 6, 9).first()
    val res2 = firstElement * firstElement
    println(res2)
}
```
配合安全操作符使用。
```kotlin
fun main() {
    println(formatGreeting(null)) // What's your name?
    println(formatGreeting("Yorick")) // Hello! Yorick.
    println(formatGreeting1(null)) // What's your name?
    println(formatGreeting1("Yorick")) // Hello! Yorick.
}
// 使用let进行链式调用
fun formatGreeting(guestName: String?): String {
    return guestName?.let {
        "Hello! $it."
    } ?: "What's your name?"
}
// 传统方式
fun formatGreeting1(guestName: String?): String {
    return if (guestName != null) {
        "Hello! $guestName."
    } else {
        "What's your name?"
    }
}
```
### run

结合了let和apply，可以像let一样返回lambda最后一行结果，同时可以像apply一样隐式调用。

```kotlin
// 判断文件是否包含某字符
fun main() {
    val file = File("E://demo.txt")
    val res = file.run {
        readText().contains("demo")
    }
    println(res) // true
}
```

另外，run也能用来执行函数引用

```kotlin
fun main() {
    //::表示把一个方法当做一个参数，传递到另一个方法中进行使用，通俗的来讲就是引用一个方法。
    "The People's Republic of China"
        .run(::isLong)
        .run(::showMessage)
        .run(::println)
}

fun isLong(str: String) = str.length >= 10

fun showMessage(isLong: Boolean): String {
    return if (isLong) {
        "String is too long!"
    } else {
        "OK!"
    }
}
// 输出
// String is too long!
```

### with

with函数是run的变体，他们的功能行为是一样的，但with的调用方式不同，调用with时需要值参作为其第一个参数传入。


```kt
fun main() {
    // 使用run
    val res1 = "The People's Republic of China".run {
        length > 10
    }
    println(res1)
    // 使用with
    val res2 = with("The People's Republic of China") {
        length > 10
    }
    println(res2)
}
// 输出
// true
// true
```

### also

和let相似，把接收者传给lambda，但是返回的是原始对象，常用于链式调用。

```kt
fun main() {
    val fileContents: List<String>
    File("E://demo.txt")
        .also {
            println(it.name)
        }.also {
            fileContents = it.readLines()
        }
    println(fileContents)
}
// 输出示例
// demo.txt
// [demo, demo, hhhh, edited by Yorick, 2022年9月8日11点32分]
```

### takeIf

类似if，判断接收者是否满足lambda的表达式，满足返回接收者，不满足则返回null。
```kt
fun main() {
    val res = File("E://demo.txt")
        .takeIf { it.exists() && it.canRead() }
        ?.readText()
    println(res)
}
// 输出文件内容
```

### takeUnless

takeIf的否定，false才返回对象，true返回null

```kotlin
fun main() {
    val res = File("E://demo.txt")
        .takeUnless { it.isHidden }
        ?.readText()
    println(res)
}
```