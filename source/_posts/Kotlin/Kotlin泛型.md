---
title: Kotlin泛型
index_img: ./img/in_out.png
categories: 
  - kotlin
date: 2022-09-12 15:24:21
tags:
  - Generic
  - 泛型
sticky: 
---

## 泛型

- [泛型](#泛型)
  - [定义泛型类](#定义泛型类)
  - [泛型函数](#泛型函数)
  - [多泛型参数](#多泛型参数)
  - [泛型类型约束](#泛型类型约束)
  - [配合vararg关键字实现多参](#配合vararg关键字实现多参)
  - [out（协变）](#out协变)
  - [in（逆变）](#in逆变)
  - [为什么使用in\&out](#为什么使用inout)
  - [reified](#reified)

### 定义泛型类

泛型类的构造函数可以接受任何类型。

MagicBox类指定的泛型参数由放在一对`<>`里的字母T表示，T是个代表item类型的占位符。MagicBox类接受任何类型的item作为主构造函数值`(item: T)`，并将item值赋给同样是T类型的subject私有属性。


```kotlin
class MagicBox<T>(item: T) {
    private var subject: T = item
}

class Boy(val name: String, val age: Int)
class Dog(val weight: Int)

fun main() {
    val box1: MagicBox<Boy> = MagicBox(Boy("Yorick", 21))
    val box2: MagicBox<Dog> = MagicBox(Dog(20))
}
```

### 泛型函数

- 泛型参数也可以用于函数。

- 定义一个函数用于获取元素，当且仅当MagicBox可用时，才能获取元素。


```kotlin
class MagicBox<T>(item: T) {
    var available = false
    private var subject: T = item
    fun fetch(): T? {
        // 判断接收者是否满足lambda的表达式，满足返回接收者，不满足则返回null。
        return subject.takeIf { available }
    }
}

class Boy(val name: String, val age: Int)
class Dog(val weight: Int)

fun main() {
    val box1: MagicBox<Boy> = MagicBox(Boy("Yorick", 21))
    val box2: MagicBox<Dog> = MagicBox(Dog(20))
    box1.available = true
    box1.fetch()?.run {
        println("you find $name")
    }
}
```
### 多泛型参数

泛型函数或泛型类也可以有多个泛型参数

```kotlin
class MagicBox<T>(item: T) {
    var available = false
    private var subject: T = item
    fun fetch(): T? {
        // 判断接收者是否满足lambda的表达式，满足返回接收者，不满足则返回null。
        return subject.takeIf { available }
    }

    fun <R> fetch(subjectModFunc: (T) -> (R)): R? {
        return subjectModFunc(subject).takeIf { available }
    }
}

class Boy(val name: String, val age: Int)
class Man(val name: String, val age: Int)
class Dog(val weight: Int)

fun main() {
    val box1: MagicBox<Boy> = MagicBox(Boy("Yorick", 15))
    val box2: MagicBox<Dog> = MagicBox(Dog(20))
    box1.available = true
    box1.fetch()?.run {
        println("you find $name")
    }
    val man = box1.fetch {
        Man(it.name, it.age.plus(10))
    }
}
```

### 泛型类型约束

如果要确保MagicBox里面只能装指定类型的物品，如Human类型
怎么办？
```kotlin
// 这里用Human约束泛型类型
class MagicBox<T : Human>(item: T) {
    var available = false
    private var subject: T = item
    fun fetch(): T? {
        return subject.takeIf { available }
    }

    fun <R> fetch(subjectModFunc: (T) -> (R)): R? {
        return subjectModFunc(subject).takeIf { available }
    }
}

open class Human(val age: Int)
class Boy(val name: String, age: Int) : Human(age)
class Man(val name: String, age: Int) : Human(age)
class Dog(val weight: Int)

fun main() {
    val box1: MagicBox<Boy> = MagicBox(Boy("Yorick", 15))
//    val box2: MagicBox<Dog> = MagicBox(Dog(20))
    box1.available = true
    box1.fetch()?.run {
        println("you find $name")
    }
    val man = box1.fetch {
        Man(it.name, it.age.plus(10))
    }
}
```

### 配合vararg关键字实现多参

```kotlin
class MagicBox<T : Human>(vararg item: T) {
    var available = false
    private var subject: Array<out T> = item
    fun fetch(index: Int): T? {
        // 判断接收者是否满足lambda的表达式，满足返回接收者，不满足则返回null。
        return subject[index].takeIf { available }
    }

    fun <R> fetch(index: Int, subjectModFunc: (T) -> (R)): R? {
        return subjectModFunc(subject[index]).takeIf { available }
    }
}

open class Human(val age: Int)
class Boy(val name: String, age: Int) : Human(age)
class Man(val name: String, age: Int) : Human(age)

fun main() {
    val box1 = MagicBox(
        Boy("Jimmy", 16),
        Boy("Jack", 13),
        Boy("Morty", 14)
    )
    box1.available = true
    box1.fetch(1)?.run {
        println("you find $name") // Jack
    }
    box1.fetch(2) {
        Man(it.name, it.age.plus(10))
    }
}
```
想要使用`box1[1]`获取实例，那么就要进行运算符重载

在MagicBox类中添加
```kotlin
operator fun get(index: Int): T? = subject[index]?.takeIf { available }
```
调用
```kotlin
println(box1[1]?.name) // Jack
```

### out（协变）

out（协变），如果泛型类只将泛型类型作为函数的返回（输出），那么使用out，可以称之为生产类/接口，因为它主要是用来生产(produce)指定的泛型对象。

```kotlin
interface Production<out T> {
    fun product(): T
}

interface Consumer<in T> {
    fun consumer(item: T)
}

interface ProductionConsumer<T> {
    fun product(): T
    fun consumer(item: T)
}

open class Food
open class FastFood : Food()
class Burger : FastFood()

class FoodStore : Production<Food> {
    override fun product(): Food {
        println("Produce Food")
        return Food()
    }
}

class FastFoodStore : Production<FastFood> {
    override fun product(): FastFood {
        println("Produce FastFood")
        return FastFood()
    }
}

class BurgerStore : Production<Burger> {
    override fun product(): Burger {
        println("Produce Burger")
        return Burger()
    }
}

fun main() {
    // 子类泛型对象可以赋值给父类泛型对象
    val production1: Production<Food> = FoodStore()
    val production2: Production<Food> = FastFoodStore()
    val production3: Production<Food> = BurgerStore()
}
```
### in（逆变）

in（逆变），如果泛型类只将泛型类型作为函数的入参（输入），那么使用
in，可以称之为消费者类/接口，因为它主要是用来消费(consume)指定的泛型对象。

```kotlin
interface Production<out T> {
    fun product(): T
}

interface Consumer<in T> {
    fun consumer(item: T)
}

interface ProductionConsumer<T> {
    fun product(): T
    fun consumer(item: T)
}

open class Food
open class FastFood : Food()
class Burger : FastFood()

class EveryBody : Consumer<Food> {
    override fun consumer(item: Food) {
        println("Eat Food")
    }
}

class ModernPeople : Consumer<FastFood> {
    override fun consumer(item: FastFood) {
        println("Eat FastFood")
    }
}

class American : Consumer<Burger> {
    override fun consumer(item: Burger) {
        println("Eat Burger")
    }
}

fun main() {
    // 父类泛型对象可以赋值给子类泛型对象
    val consumer1: Consumer<Burger> = EveryBody()
    val consumer2: Consumer<Burger> = ModernPeople()
    val consumer3: Consumer<Burger> = American()
}
```

### 为什么使用in&out

父类泛型对象可以赋值给子类泛型对象，用in。
子类泛型对象可以赋值给父类泛型对象，用out。

![in&out](./img/in_out.png)

### reified

有时候，你可能想知道某个泛型参数具体是什么类型，reified关键字能帮你检查泛型参数类型。Kotlin不允许对泛型参数T做类型检查，因为泛型参数类型会被类型擦除，也就是说，T的类型信息在运行时是不可知的。

人话：配合内联使用，加了reified关键字，就可以使用is判断类型了。

```kotlin
class MagicBox<T : Human>(vararg item: T) {
    // 随机产生一个对象，如果不是指定类型的对象，就通过backup函数生成一个指定类型的对象
    inline fun <reified T> randomOrBackup(backup: () -> T): T {
        val items = listOf(
            Boy("Jack", 20),
            Man("Jimmy", 35)
        )
        val random = items.shuffled().first()
        // 这里进行类型判断
        return if (random is T) {
            random
        } else {
            backup()
        }
    }
}

open class Human(val age: Int)
class Boy(private val name: String, age: Int) : Human(age){
    override fun toString(): String {
        return "Boy(name='$name',age='$age')"
    }
}
class Man(private val name: String, age: Int) : Human(age){
    override fun toString(): String {
        return "Boy(name='$name',age='$age')"
    }
}
class Dog(val weight: Int)

fun main() {
    val box: MagicBox<Boy> = MagicBox()
    val subject = box.randomOrBackup {
        Boy("Jimmy", 21)
    }
    println(subject)
}

```