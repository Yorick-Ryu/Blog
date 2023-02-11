---
title: Kotlin空安全与异常
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-07 15:06:55
tags:
  - 异常
  - Exception
sticky: 
---

## null安全与异常

- [null安全与异常](#null安全与异常)
  - [可空性](#可空性)
  - [null安全](#null安全)
    - [安全调用操作符](#安全调用操作符)
    - [使用带let的安全调用](#使用带let的安全调用)
    - [使用!!.操作符](#使用操作符)
    - [使用if判断null值](#使用if判断null值)
    - [使用空合并表达式](#使用空合并表达式)
  - [异常](#异常)
  - [先决条件函数](#先决条件函数)

Koltin受不了Java里常见的空指针异常，所以做出了改良。Kotlin更多地把运行时可能会出现的null问题，以编译错误的方式，提前在代码编译期强迫我们重视起来。

### 可空性

对于null值问题，Kotlin反其道而行之，除非另有规定，变量不可为null值，这样一来，运行时崩溃从根源上得到解决。
```kotlin
// 编译无法通过
fun main() {
    var str = "Hi,Yorick!"
    str = null
}
```
如果我偏要赋null值呢？
```kotlin
fun main() {
    var str:String? = "Hi,Yorick!"
    str = null
}
```

<!-- ### Kotlin的null类型 ### 编译时间与运行时间 -->

### null安全

Kotlin区分可空类型和非可空类型，所以，你要一个可空类型变量运行，而它又可能不存在，对于这种潜在危险，编译器时刻警惕着。为了应对这种风险，Kotlin不允许你在可空类型值上调用函数，除非你主动接手安全管理。

#### 安全调用操作符

直接调用空类型的方法，编译器会报错
```Kotlin
fun main() {
    var str:String? = "Hi,Yorick!"
    str = null
    // 下面会报错
    println(str.length)
}
```
但是使用安全调用操作符`?.`，就可有避免，`?.`的作用为调用者非空才执行。
```Kotlin
fun main() {
    var str:String? = "Hi,Yorick!"
    str = null
    println(str?.length)
}
```

#### 使用带let的安全调用

安全调用允许在可空类型上调用函数，但是如果还想做点额外的事，比如创建新值，或判断不为null就调用其他函数，怎么办?

可以使用带let函数的安全调用操作符。你可以在任何类型上调用let函数，它的主要作用是让你在指定的作用域内定义一个或多个变量。
```java
fun main() {
    var str: String? = "hi,Yorick!"
    str = str?.let {
        // 非空白的字符串
        if (it.isNotBlank()) {
            it.capitalize()
        } else {
            "Hi,Yorick!"
        }
    }
    println(str)
}
// 输出
// Hi,Yorick!
```

#### 使用!!.操作符

`!!.`非空断言操作符，强制执行方法，会抛出空指针异常。
```kotlin
fun main() {
    var str: String? = "hi,Yorick!"
    str = null
    println(str!!.capitalize())
}
```

#### 使用if判断null值
这里就是传统Java的使用if判断null值，可以比较一下，Kotlin用一个`?`就解决了。
```kotlin
fun main() {
    var str: String? = "hi,Yorick!"
    if (str != null) {
        str = str.capitalize()
    } else {
        println("为空")
    }
    println(str)
}
```
我们可以使用if判断，但是相比之下安全调用操作符用起来更灵活，代码也更简洁，我们可以用安全操作符进行多个函数的链式调用。

```kotlin
fun main() {
    var str: String? = "hi,Yorick."
    str = str?.capitalize().plus("Have a nice day!")
    println(str)
}
// 输出
// Hi,Yorick.Have a nice day!
```
如果第一个`?.`方法的调用者为空，那么后面的方法都不会被调用。
#### 使用空合并表达式

`?:`操作符的意思是，如果左边的求值结果为null，就使用右边的结果值。

```kotlin
fun main() {
    var str: String? = "hi,Yorick."
    str = null
    println(str ?: "yeah!")
}
// 输出
// yeah!
```
空合并操作符也可以和let函数一起使用来代替if/else语句。
```kotlin
fun main() {
    var str: String? = "hi,Yorick."
    str = str?.let { it.capitalize() } ?: "yeah!"
    println(str)
}
```

### 异常

异常处理：
```kotlin
fun main() {
    val number: Int? = null
    try {
        number!!.plus(1)
    } catch (e: KotlinNullPointerException) {
        println(e)
    }
}
```
自定义异常：
```kotlin
import java.lang.IllegalArgumentException

fun main() {
    val number: Int? = null
    try {
        checkOperation(number)
        number!!.plus(1)
    } catch (e: KotlinNullPointerException) {
        println(e)
    }
}

fun checkOperation(number: Int?) {
    number ?: throw UnskilledException()
}

// 自定义异常
class UnskilledException : IllegalArgumentException("操作不当")
```

### 先决条件函数

Kotlin标准库提供了一些便利函数，使用这些内置函数，你可以抛出带自定义信息的异常，这些便利函数叫做先决条件函数，你可以用它定义先决条件，条件必须满足目标代码才能执行。

```kotlin
// 在上面代码的基础上修改
fun checkOperation(number: Int?) {
    checkNotNull(number) { "Something is Null!" }
}
```

| 函数           | 描述                                                                          |
| -------------- | ----------------------------------------------------------------------------- |
| checkNotNull   | 如果参数为null，则抛出IllegalStateException异常，否则返回非null值              |
| require        | 如果参数为false，则抛出IllegalArgumentException异常                           |
| requireNotNull | 如果参数为null，则抛出IllegalStateException异常，否则返回非null值              |
| error          | 如果参数为null，则抛出IllegalStateException异常并输出错误信息，否则返回非null值 |
| assert         | 如果参数为false，则抛出AssertError异常，并打上断言编译器标记                  |

<!-- ### 已检查异常和未检查异常 ### 可空性如何保证 -->