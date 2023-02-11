---
title: Kotlin函数式编程
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-14 19:12:10
tags: 
sticky: 
---

## 函数式编程

- [函数式编程](#函数式编程)
  - [什么是函数式编程](#什么是函数式编程)
  - [函数类别](#函数类别)
  - [变换transform](#变换transform)
    - [map](#map)
    - [flatMap](#flatmap)
  - [过滤filter](#过滤filter)
    - [filter](#filter)
    - [找素数](#找素数)
  - [合并combine](#合并combine)
    - [zip](#zip)
    - [fold](#fold)
  - [为什么要使用函数式编程](#为什么要使用函数式编程)
  - [序列](#序列)
    - [generateSequence](#generatesequence)
    - [使用序列查找素数](#使用序列查找素数)

### 什么是函数式编程

我们一直在学习面向对象编程范式，另一个较知名的编程范式是诞生于20世纪50年，基于抽象数学的入演算发展而来的函数式编程，尽管函数式编程语言更常用在学术而非商业软件领域，但它的一些原则适用于任何编程语言。函数式编程范式主要依赖于高阶函数（以函数为参数或返回函数）返回的数据，这些高阶函数专用于处理各种集合，可方便地联合多个同类函数构建链式操作以创建复杂的计算行为。Kotlin支持多种编程范式，所以你可以混用面向对象编程和函数式编程范式来解决手头的问题。


### 函数类别

一个函数式应用通常由三大类函数构成:变换transform、过滤filter、合并combine。每类函数都针对集合数据类型设计，目标是产生一个最终结果。函数式编程用到的函数生来都是可组合的，也就是说，你可以组合多个简单函数来构建复杂的计算行为。

### 变换transform

变换是函数式编程的第一大类函数，变换函数会遍历集合内容，用一个以值参形式传入的变换器函数，变换每一个元素，然后返回包含已修改元素的集合给链上的其他函数。

最常用的两个变换函数是map和flatMap。

#### map

map返回的集合中的元素个数和输入集合必须一样，不过，返回的新集合里的元素可以是不同类型的。

```kt
fun main() {
    val animals = listOf("zebra", "giraffe", "elephant", "rat")
    val babies = animals
        .map { animals -> "A little $animals" }
        .map { baby -> "$baby,with the cutest little tail ever!" }
    println(animals) // [zebra, giraffe, elephant, rat]
    println(babies) // [A little zebra,with the cutest little tail ever!, A little giraffe,with the cutest little tail ever!, A little elephant,with the cutest little tail ever!, A little rat,with the cutest little tail ever!]
    
    val animalsLength = animals.map { it.length }
    println(animalsLength) // [5, 7, 8, 3]
}
```

可以看到，原始集合没有被修改，map变换函数和你定义的变换器函数做完事情后，返回的是一个新集合，这样，变量就不用变来变去了。

**事实上，函数式编程范式支持的设计理念就是不可变数据的副本在链上的函数间传递。**

#### flatMap

flatMap函数操作一个集合的集合，将其中多个集合中的元素合并后返回一个包含所有元素的单一集合。

```kt
fun main() {
    val res = listOf(
        listOf(1, 2, 3),
        listOf(4, 5, 6)
    ).flatMap { it }
    println(res)
}
```

### 过滤filter

过滤是函数式编程的第二大类函数，过滤函数接受一个predicate函数，用它按给定条件检查接收者集合里的元素并给出true或false的判定。如果predicate函数返回true，受检元素就会添加到过滤函数返回的新集合里。如果predicate函数返回false，那么受检元素就被移出新集合。

```kt
fun main() {
    val res = listOf("Jack", "Jimmy", "Rose", "Tom")
        .filter { it.contains("J") }
    println(res) // [Jack, Jimmy]
}
```

#### filter

filter过滤函数接受一个predicate函数，在flatMap遍历它的输入集合中的所有元素时，filter函数会让predicate函数按过滤条件，将符合条件的元素都放入它返回的新集合里。最后，flatMap会把变换器函数返回的子集合合并在一个新集合里。


```kt
fun main() {
    val items = listOf(
        listOf("red apple", "green apple", "blue apple"),
        listOf("red fish", "blue fish"),
        listOf("yellow banana", "teal banana")
    )

    val redItems = items.flatMap { it.filter { it.contains("red") } }
    println(redItems) // [red apple, red fish]
}
```

#### 找素数

```kt
fun main() {
    val numbers = listOf(7, 4, 8, 4, 3, 22, 18, 11)
    // 找素数
    val primes = numbers.filter { number ->
        (2 until number).map { number % it }
            .none { it == 0 }
    }
    println(primes) // [7, 3, 11]
}
```

### 合并combine

合并是函数式编程的第三大类函数，合并函数能将不同的集合合并成一个新集合，这和接收者是包含集合的集合的flatMap函数不同。

#### zip

zip合并函数来合并两个集合,返回一个包含键值对的新集合。

```kt
fun main() {
    val names = listOf("Jack", "Jimmy", "Rose", "Tom")
    val ages = listOf(15, 21, 18, 22)

    val students = names.zip(ages)
    println(students) // [(Jack, 15), (Jimmy, 21), (Rose, 18), (Tom, 22)]
}
```

#### fold

另一个可以用来合并值的合并类函数是fold，这个合并函数接受一个初始累加器值，随后会根据匿名函数的结果更新。

```kt
fun main() {
    val foldedValue = listOf(1, 2, 3, 4).fold(0) { acc, number ->
        println("accVal: $acc")
        acc + number * 3
    }

    println("Final value:$foldedValue")
}
// accVal: 0
// accVal: 3
// accVal: 9
// accVal: 18
// Final value:30
```

### 为什么要使用函数式编程

乍看之下，实现同样的任务，Java版本和函数式版本的代码量差不多，但仔细分析一下，就能看出函数式版本的诸多优势。

- 累加变量(employeeShirtSizes)都是隐式定义的。
- 函数运算结果会自动赋值给累加变量，降低了代码出错的机会。
- 执行新任务的函数很容易添加到函数调用链上，因为他们都兼容lterable类型。

### 序列

List、Set、Map集合类型，这几个集合类型统称为及早集合(eager collection)这些集合的任何一个实例在创建后，它要包含的元素都会被加入并允许你访问。对应及早集合，Kotlin还有另外一类集合：惰性集合（lazy collection）类似于类的惰性初始化，惰性集合类型的性能表现优异，尤其是用于包含大量元素的集合时，因为集合元素是按需产生的。


Kotlin有个内置惰性集合类型叫序列(Sequence)，序列不会索引排序它的内容，也不记录元素数目，事实上，在使用一个序列时，序列里的值可能有无限多，因为某个数据源能产生无限多个元素。

#### generateSequence

针对某个序列，你可能会定义一个只要序列有新值产生就被调用一下的函数，这样的函数叫迭代器函数，要定义一个序列和它的迭代器，你可以使用Kotlin的序列构造函数generateSequence，generateSequence函数接受一个初始种子值作为序列的起步值，在用generateSequence定义的序列上调用一个函数时，generateSequence函数会调用你指定的迭代器函数，决定下一个要产生的值。

#### 使用序列查找素数

```kt
fun Int.isPrime(): Boolean {
    (2 until this).map {
        if (this % it == 0) {
            return false
        }
    }
    return true
}

fun main() {
    // 假定0-5000内，可以找到1000个素数，普通集合写法
    val toList = (1..5000).toList().filter { it.isPrime() }.take(1000)
    println(toList.size) // 670
    // 使用序列
    val oneThousandPrimes = generateSequence(2) { value ->
        value + 1
    }.filter { it.isPrime() }.take(1000)
    println(oneThousandPrimes.toList().size) // 1000
}
```