---
title: Kotlin面向对象_继承与对象
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-11 11:39:43
tags: 
sticky: 
---

# 面向对象

- [面向对象](#面向对象)
  - [继承](#继承)
    - [open关键字](#open关键字)
    - [类型检测与转换](#类型检测与转换)
    - [智能类型转换](#智能类型转换)
    - [Any超类](#any超类)
  - [对象](#对象)
    - [Object关键字](#object关键字)
    - [对象声明](#对象声明)
    - [对象表达式](#对象表达式)
    - [伴生对象](#伴生对象)
    - [嵌套类](#嵌套类)
    - [数据类](#数据类)
    - [copy关键字](#copy关键字)
    - [结构声明](#结构声明)
    - [运算符重载](#运算符重载)
    - [枚举类](#枚举类)
    - [枚举类定义函数](#枚举类定义函数)
    - [代数数据类型](#代数数据类型)
    - [密封类](#密封类)

## 继承

### open关键字
类默认都是封闭的，要让某个类开放继承，必须使用open关键字修饰它。

```kotlin
open class Product(val name: String) {
    fun desc() = "Product: $name"
    open fun load() = "Nothing"
}

class LuxuryProduct : Product("Luxury") {
    // 重写方法
    override fun load() = "LuxuryProduct loading..."
}

fun main() {
    val p:Product = LuxuryProduct()
    println(p.load()) // LuxuryProduct loading...
}
```
### 类型检测与转换

使用`is`进行类型检测
使用`as`进行类型转换
```kt
import java.io.File

open class Product(val name: String) {
    fun desc() = "Product: $name"
    open fun load() = "Nothing"
}

class LuxuryProduct : Product("Luxury") {
    override fun load() = "LuxuryProduct loading..."
    fun special() = "LuxuryProduct special function"
}

fun main() {
    val p: Product = LuxuryProduct()
    println(p.load())
    // 类型检测
    println(p is Product) // true
    println(p is LuxuryProduct) // true
    println(p is File) // false

    if (p is LuxuryProduct) {
        // 类型转换
        println((p as LuxuryProduct).special()) // LuxuryProduct special function
    }
}
```
### 智能类型转换

Kotlin编译器很聪明，只要能确定any is 父类条件检查属实，它就会将any当做子类类型对待，因此，编译器允许你不经类型转换直接使用。

```kt
println((p as LuxuryProduct).special())
p.special() // 再次调用无需转换
```

### Any超类

类似Java里的Object，Kotlin所有类的共同超类为Any
```kt
println(p is Any) // true
```

## 对象

### Object关键字

使用object关键字，你可以定义一个只能产生一个实例的类-单例

使用object关键字有三种方式

- 对象声明
- 对象表达式
- 伴生对象

### 对象声明

对象声明有利于组织代码和管理状态，尤其是管理整个应用运行生命周期内的某些一致性状态。

```kt
object ApplicationConfig {
    init {
        println("ApplicationConfig is loading...")
    }

    fun doSomething() {
        println("do something...")
    }
}

fun main() {
    // 单例模式 类名=对象名
    ApplicationConfig.doSomething()
    println(ApplicationConfig) // ApplicationConfig@52cc8049
    println(ApplicationConfig) //ApplicationConfig@52cc8049
}
```

### 对象表达式

有时候你不一定非要定义一个新的命名类不可，也许你需要某个现有类的一种变体实例，但只需用一次就行了，对于这种用完就丢的类实例，连命名都可以省了。

这个匿名类依然遵循object关键字的一个规则，即一旦实例化，该匿名类只能有唯一一个实例存在。


```kt
open class Player {
    open fun load() = "loading something..."
}

fun main() {
    // 对象表达式
    val p = object : Player() {
        override fun load(): String = "anonymous class load..."
    }
    println(p.load())
}
```

### 伴生对象

使用companion修饰符，将对象伴生在类上，一个类只能有一个伴生对象。

```kt
import java.io.File

open class ConfigMap {
    companion object {
        private const val PATH = "E://demo.txt"
        fun load() = File(PATH).readBytes()
    }
}

fun main() {
    ConfigMap.load()
}
```

### 嵌套类

如果一个类只对另一个类有用，那么将其嵌入到该类中并使这两个类保持在一起是合乎逻辑的，可以使用嵌套类。


```kt
class Play {
    class Equipment(var name: String) {
        fun show() = println("equipment: $name")
    }

    fun battle() {
        Equipment("sharp knife").show()
    }
}

fun main() {
    // 直接调用
    Play.Equipment("M416").show() // equipment: M416
}
```

### 数据类

数据类，是专门设计用来存储数据的类

- 数据类提供了`toString`的个性化实现
- `==`符号默认情况下，比较对象就是比较它们的引用值，数据类提供了`equals`和`hashCode`的个性化实现

使用数据类
```kt
data class Coordinate(var x: Int, var y: Int) {
    val isInBounds = x > 0 && y > 0
}

fun main() {
    println(Coordinate(10, 20))
    println(Coordinate(x = 10, y = 20) == Coordinate(x = 10, y = 20))
}
// Coordinate(x=10, y=20)
// true
```
使用普通类
```kt
class Coordinate(var x: Int, var y: Int) {
    val isInBounds = x > 0 && y > 0
}

fun main() {
    println(Coordinate(10, 20))
    println(Coordinate(x = 10, y = 20) == Coordinate(x = 10, y = 20))
}
// Coordinate@52cc8049
// false
```

正是因为上述这些特性，你才倾向于用数据类来表示存储数据的简单对象，对于那些经常需要比较、复制或打印自身内容的类，数据类尤其适合它们。然而，一个类要成为数据类，也要符合一定条件。总结下来，主要有三个方面：

- 数据类必须有至少带一个参数的主构造函数
- 数据类主构造函数的参数必须是val或var
- 数据类不能使用abstract、open、sealed和inner修饰符


### copy关键字
data还提供了复制对象的方法copy。

但是，copy时不会执行次构造函数里的语句，所以次构造函数里的赋值不会被copy到新对象。
```kt
data class Student(var name: String, val age: Int) {
    var score = 10
    private val bobby = "music"
    var subject: String

    init {
        println("initializing subject")
        subject = "math"
    }

    constructor(_name: String) : this(_name, 10) {
        println("constructor")
        score = 20
    }

    override fun toString(): String {
        return "Student(name='$name', age=$age, score=$score, bobby='$bobby', subject='$subject')"
    }
}

fun main() {
    val s = Student("John")
    val copy = s.copy("Alice")
    println(s)
    println(copy)
}
// initializing subject
// constructor
// initializing subject
// Student(name='John', age=10, score=20, bobby='music', subject='math')
// Student(name='Alice', age=10, score=10, bobby='music', subject='math')
```
### 结构声明

解构声明的后台实现就是声明component1、component2等若干个组件函数，让每个函数负责管理你想返回的一个属性数据。

普通类
```kt
class PlayerScore(val exp: Int, val level: Int) {
    // 需要组件函数
    operator fun component1() = exp
    operator fun component2() = level
}

fun main() {
    val (x, y) = PlayerScore(10, 20)
    println("$x,$y") // 10,20
```
如果你定义一个数据类，它会自动为所有定义在主构造函数的属性添加对应的组件函数。

```kt
data class PlayerScore(val exp: Int, val level: Int) {}

fun main() {
    val (x, y) = PlayerScore(10, 20)
    println("$x,$y") // 10,20
}
```
### 运算符重载

如果要将内置运算符应用在自定义类身上，你必须重写运算符函数，告诉编译器该如何操作自定义类。

```kotlin
data class Coordinate(var x: Int, var y: Int) {
    val isInBounds = x > 0 && y > 0
    // 重载加法运算符
    operator fun plus(other: Coordinate) = Coordinate(x + other.x, y + other.y)
}

fun main() {
    val p1 = Coordinate(10, 20)
    val p2 = Coordinate(20, 10)
    val p3 = p1 + p2
    println(p3) // Coordinate(x=30, y=30)
}
```
常见操作符
| 操作符 | 函数名     | 作用                                                    |
| ------ | ---------- | ------------------------------------------------------- |
| +      | plus       | 把一个对象添加到另一个对象里                            |
| +=     | plusAssign | 把一个对象添加到另一个对象里，然后将结果赋值给第一个对象 |
| ==     | equals     | 如果两个对象相等，则返回true，否则返回false             |
| >      | compareTo  | 如果左边的对象大于右边的对象，则返回true，否则返回false |
| [ ]    | get        | 返回集合中指定位置的元素                                |
| ..     | rangeTo    | 创建一个range对象                                       |
| in     | contains   | 如果对象包含在集合里，则返回true                        |

### 枚举类 

枚举类,用来定义常量集合的一种特殊类。

```kotlin
enum class Direction {
    EAST,
    WEST,
    SOUTH,
    NORTH
}

fun main() {
    println(Direction.EAST) // EAST
    println(Direction.EAST is Direction) // true
}
```

### 枚举类定义函数

```kotlin
enum class Direction(private val coordinate: Coordinate) {
    // 实例
    EAST(Coordinate(1, 0)),
    WEST(Coordinate(-1, 0)),
    SOUTH(Coordinate(0, -1)),
    NORTH(Coordinate(0, 1));

    fun updateCoordinate(playerCoordinate: Coordinate) =
        Coordinate(playerCoordinate.x + coordinate.x, playerCoordinate.y + coordinate.y)
}

fun main() {
    println(Direction.EAST.updateCoordinate(Coordinate(10, 20)))
}
// Coordinate(x=11, y=20)
```
### 代数数据类型

可以用来表示一组子类型的闭集,枚举类就是一种简单的ADT。

```kt
enum class LicenseStatus {
    UNQUALIFIED,
    LEARNING,
    QUALIFIED;
}

class Driver(var status: LicenseStatus) {
    fun checkLicense(): String {
        return when (status) {
            LicenseStatus.UNQUALIFIED -> "没资格"
            LicenseStatus.LEARNING -> "正在学"
            LicenseStatus.QUALIFIED -> "有资格"
        }
    }
}

fun main() {
    println(Driver(LicenseStatus.QUALIFIED).checkLicense())
}
```

### 密封类 

对于更复杂的ADT，你可以使用Kotlin的密封类(sealed class）来实现更复杂的定义，密封类可以用来定义一个类似于枚举类的ADT，但你可以更灵活地控制某个子类型。

密封类可以有若干个子类，要继承密封类，这些子类必须和它定义在同一个文件里。

```kt
sealed class LicenseStatus {
    // 没有属性，所以用单例模式
    object UnQualified : LicenseStatus()
    object Learning : LicenseStatus()
    // 每次id不一样，所以使用类
    class Qualified(val licenseID: String) : LicenseStatus()
}

class Driver(var status: LicenseStatus) {
    fun checkLicense(): String {
        return when (status) {
            is LicenseStatus.UnQualified -> "没资格"
            is LicenseStatus.Learning -> "正在学"
            is LicenseStatus.Qualified -> "有资格，驾驶证编号：${(this.status as LicenseStatus.Qualified).licenseID}"
        }
    }
}

fun main() {
    val status = LicenseStatus.Qualified("2225211")
    val driver = Driver(status)
    println(driver.checkLicense())
    // 有资格，驾驶证编号：2225211
}
```