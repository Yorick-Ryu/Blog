---
title: Kotlin拓展函数和拓展属性
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-13 17:25:57
tags: 
sticky: 
---

## 拓展函数

- [拓展函数](#拓展函数)
  - [定义拓展函数](#定义拓展函数)
  - [在超类上定义拓展函数](#在超类上定义拓展函数)
  - [泛型拓展函数](#泛型拓展函数)
- [拓展属性](#拓展属性)
  - [定义拓展属性](#定义拓展属性)
- [其他拓展特性](#其他拓展特性)
  - [可空类拓展](#可空类拓展)
  - [infix关键字](#infix关键字)
  - [Kotlin标准库中的扩展](#kotlin标准库中的扩展)
- [DSL](#dsl)
  - [apply函数详解](#apply函数详解)
  - [什么是DSL](#什么是dsl)

### 定义拓展函数

扩展可以在不直接修改类定义的情况下增加类功能，扩展可以用于自定义类，也可以用于比如List、String，以及Kotlin标准库里的其他类。和继承相似，扩展也能共享类行为，在你无法接触某个类定义，或者某个类没有使用open修饰符，导致你无法继承它时，扩展就是增加类功能的最好选择。

```kotlin
fun String.addExt(amount: Int = 1) = this + "!".repeat(amount)

fun main() {
    println("Hi,Yorick".addExt(6))
}
```
### 在超类上定义拓展函数

在超类上定义拓展函数，Any的所有子类都能使用该函数了

```kotlin
fun Any.easyPrint() = println(this)
// 作用范围为全局
fun main() {
    "test".easyPrint() // test
    15.easyPrint() // 15
}
```

但是如果想要支持链式调用，返回值就必须为String，这样的话其他类型就无法使用easyPrint。
```kotlin
// 给字符串添加拓展函数
fun String.addExt(amount: Int = 1) = this + "!".repeat(amount)

fun String.easyPrint():String {
    println(this)
    return this
}

fun main() {
//    15.easyPrint() // 此行报错
    "aaa".easyPrint().addExt(2).easyPrint()
}
// aaa
// aaa!!
```
要解决上面的问题，就要用到泛型拓展函数

### 泛型拓展函数

新的泛型扩展函数不仅可以支持任何类型的接收者，还保留了接收者的类型信息，使用泛型类型后，扩展函数能够支持更多类型的接收者，适用范围更广了。

```kt
// 给字符串添加拓展函数
fun String.addExt(amount: Int = 1) = this + "!".repeat(amount)

fun <T> T.easyPrint(): T {
    println(this)
    return this
}

fun main() {
    15.easyPrint() // 正常使用
    "aaa".easyPrint().addExt(2).easyPrint()
}
// 15
// aaa
// aaa!!
```

泛型扩展函数在Kotlin标准库里随处可见，例如let函数，let函数被定义成了泛型扩展函数，所以能支持任何类型，它接收一个lambda表达式，这个lambda表达式接收者T作为值参，返回的R-lambda表达式返回的任何新类型。
```kt
public inline fun <T, R> T.let(block: (T) -> R): R {
    return block(this)
}
```


## 拓展属性

### 定义拓展属性

除了给类添加功能扩展函数外，你还可以给类定义扩展属性，给String类添加一个扩展，这个扩展属性可以统计字符串里有多少个元音字母。

```kotlin
fun <T> T.easyPrint(): T {
    println(this)
    return this
}

// 统计元音字母
val String.numVowels
    get() = count { "aeiou".contains(it) }

fun main() {
    "The people's Republic of China".numVowels.easyPrint() // 10 
}

```
## 其他拓展特性

### 可空类拓展

你也可以定义扩展函数用于可空类型，在可空类型上定义扩展函数，你就可以且直接在扩展函数体内解决可能出现的空值问题。

```kotlin
fun String?.printWithDefault(default: String) = print(this ?: default)

fun main() {
    val nullableString: String? = null
    nullableString.printWithDefault("abc") // abc
}
```

### infix关键字

infix关键字适用于有**单个参数**的扩展和类函数，可以让你以更简洁的语法调用函数，如果一个函数定义使用了infix关键字，那么调用它时，接收者和函数之间的**点操作**以及**参数的一对括号**都可以不要。


```kotlin
infix fun String?.printWithDefault(default: String) = print(this ?: default)

fun main() {
    val nullableString: String? = null
    // 下面这行
    nullableString printWithDefault "abc"
}
```
常见与mapOf
```kotlin
mapOf("Jack" to 18) // 等价于 
"Jack".to(18)
```

新建包extension，定义方法：
```kotlin
package extension

fun <T> Iterable<T>.randomTake() = this.shuffled().first()
```

使用：
```kotlin
// 引入方法
import extension.randomTake

fun main() {
    val list = listOf("Yorick", "Morty", "Sandy")
    val set = setOf("Yorick", "Morty", "Sandy")

    println(list.randomTake()) // 示例输出 Yorick
    println(set.randomTake()) // 示例输出 Morty
}
```
也可以给引入的方法取别名
```kotlin
import extension.randomTake as rt

fun main() {
    val list = listOf("Yorick", "Morty", "Sandy")
    val set = setOf("Yorick", "Morty", "Sandy")
    println(list.rt())
    println(set.rt())
}
```

### Kotlin标准库中的扩展

Kotlin标准库提供的很多功能都是通过扩展函数和扩展属性来实现的，包含类扩展的标准库文件通常都是以类名加s后缀来命名的，例如`Sequences.kt`，`Ranges.kt`，`Maps.kt`。

## DSL

### apply函数详解

apply函数时如何做到支持接收者对象的隐式调用的？

```kotlin
public inline fun <T> T.apply(block: T.() -> Unit): T {
    block()
    return this
}
```
**为什么传入泛型的拓展函数？** `T.() -> Unit`

因为拓展函数里自带了this的隐式调用，比如addExt()函数
```kotlin
import java.io.File

fun String.addExt() = "*".repeat(this.count())

public inline fun <T> T.apply(block: T.() -> Unit): T {
    block()
    return this
}

fun main() {
    val file = File("xxx").apply {
        setReadable(true)
    }
}
```

**为什么是泛型的拓展函数？**

如果不用泛型怎么写？
```kotlin
public inline fun File.apply(block: File.() -> Unit): File {
    block()
    return this
}

fun main() {
    val file = File("xxx").apply {
        setReadable(true)
    }
}
```
但是这样apply就只能用于File类型。

**分解调用，加深理解**
```kotlin
public inline fun File.apply(block: File.() -> Unit): File {
    block()
    return this
}

fun main() {
    var file = File("xxx").apply {
        setReadable(true)
    }

    // 将上面代码分解一下
    // 定义拓展函数
    fun File.ext() = setReadable(true)
    // 给block复制
    val block = File::ext
    // 传入apply函数
    file =  File("xx").apply { block }
}
```

### 什么是DSL

使用这样的编程范式，就可以写出业界知名的`领域特定语言`(DSL)，一种API编程范式，暴露接收者的函数和特性，以便于使用你定义的lambda表达式来读取和配置它们。
