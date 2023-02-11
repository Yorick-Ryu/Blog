---
title: Kotlin集合与数组
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-08 17:30:43
tags: 
  - Collection
  - Array
  - List
  - Set
  - Map
sticky: 
---

# Kotlin集合与数组

## List集合

### List的创建与元素获取

```kotlin
fun main() {
    // 创建List
    val list = listOf("Yorick", "Jerry", "Sandy")
    // 普通获取
    println(list[2])
    // 使用安全索引函数获取
    // getOrElse:没有则返回lambda表达式的结果
    println(list.getOrElse(3){"Nothing"})
    // getOrNull:没有则返回空
    println(list.getOrNull(3))
    // getOrNull配合合并操作符使用
    println(list.getOrNull(3)?:"Nothing")
}
```

### 可变列表

在Kotlin中，支持修改内容的列表叫可变列表，要创建可变列表，可以使用mutableListOf函数。List还支持使用toList和toMutableList函数动态实现只读列表和可变列表的相互转换。

```kt
fun main() {
    // 创建可变列表
    val mutableList = mutableListOf("Yorick", "Jerry", "Sandy")
    mutableList.add("Jack")
    mutableList.remove("Jerry")、
    // 相互转换
    listOf("Yorick", "Jerry", "Sandy").toMutableList()
    mutableList.toList()
}
```

### mutator函数

能修改可变列表的函数有个统一的名字：mutator函数

添加元素运算符与删除元素运算符

基于lambda表达式指定的条件删除元素


```kt
fun main() {
    // 创建可变列表
    val mutableList = mutableListOf("Yorick", "Jerry", "Sandy")
    mutableList += "Morty" // 相当于add
    mutableList -= "Sandy" // 相当于remove
    mutableList.removeIf{it.contains("o")} // 满足条件才移除
    println(mutableList)
}
```

### 集合遍历

- for in 遍历

- forEach 遍历

- forEachIndexed 遍历时要获取索引

```kt
fun main() {
    val list = listOf("Yorick", "Jerry", "Sandy")
    for (s in list) {
        println(s)
    }

    list.forEach {
        println(it)
    }

    list.forEachIndexed { index, item ->
        println("$index : $item")
    }
}
```

### 解构

```kt
fun main() {
    val list = listOf("Yorick", "Jerry", "Sandy")
    // 解构赋值
    val (origin,dest,proxy) = list
    println("$origin $dest $proxy")
}
```
当想跳过某个元素，则用下划线代替。
```kt
val (origin, _, proxy) = list
println("$origin $proxy")
// 输出
// Yorick Sandy
```

## Set集合

通过setOf创建set集合，使用elementAt函数读取集合中的元素。

### Set创建与元素获取

setOf：创建集合
elementAt：获取集合

```kt
fun main() {
    // 重复元素自动覆盖
    val set = setOf("Yorick", "Jerry", "Sandy","Yorick")
    println(set.elementAt(2)) // Sandy
}
```

### 可变集合

通过mutableSetOf创建可变的set集合

```kt
fun main() {
    val mutableSet = mutableSetOf("Yorick", "Jerry", "Sandy", "Yorick")
    mutableSet += "Morty"
    mutableSet.forEach {
        println(it)
    }
}
```

### 集合转换和快捷去重

```kt
fun main() {
    // 通过集合转换函数去重
    val list = listOf("Yorick", "Jerry", "Sandy", "Yorick")
        .toSet()
        .toList()
    println(list)
    // 快捷操作
    println(listOf("Yorick", "Jerry", "Sandy", "Yorick").distinct())
}
// 都输出
// [Yorick, Jerry, Sandy]
```

## 数组

Kotlin提供各种Array，虽然是引用类型，但可以编译成Java基本数据类型。


| 数组类型     | 创建函数       |
| ------------ | -------------- |
| lntArray     | intArrayOf     |
| DoubleArray  | doubleArrayOf  |
| LongArray    | longArrayOf    |
| ShortArray   | shortArrayOf   |
| ByteArray    | byteArrayOf    |
| FloatArray   | floatArrayOf   |
| BooleanArray | booleanArrayOf |
| Array        | arrayOf        |

```kt
fun main() {
    val intArrayOf = intArrayOf(1, 4, 2, 4, 6, 7)
    // list可以直接转换为array
    listOf(10, 20, 30).toIntArray()
    // 对象数组
    val arrayList = arrayListOf(File("xxx"), File("yyy"), File("zzz"))
}
```
## Map

### Map的创建
使用mapOf创建Map
```kt
fun main() {
    // 创建Map
    val map = mapOf("Yorick" to 21, "Lily" to 20, "Jerry" to 17)
    // 等价方式
    mapOf(Pair("Yorick", 21), Pair("Lily", 20))
}
```

### 读取Map的值

- `[]`取值运算符，读取键对应的值，如果键不存在就返回null
- `getValue`，读取键对应的值，如果键不存在就抛出异常
- `getOrElse`，读取键对应的值，或者使用匿名函数返回默认值
- `getOrDefault`，读取键对应的值，或者返回默认值

```kt
fun main() {
    val map = mapOf("Yorick" to 21, "Lily" to 20, "Jerry" to 17)
    println(map["Yorick"]) // 21
    println(map.getValue("Yorick")) // 21
    println(map.getOrElse("Rose") { "NOTHING" }) // NOTHING
    println(map.getOrDefault("Rose",0)) // 0
}
```

### Map的遍历

还是用forEach

```kt
fun main() {
    val map = mapOf("Yorick" to 21, "Lily" to 20, "Jerry" to 17)
    // 遍历Map
    map.forEach {
        println("${it.key} : ${it.value}")
    }
    map.forEach { (key: String, value: Int) ->
        println("$key : $value")
    }
}
// 都输出
// Yorick : 21
// Lily : 20
// Jerry : 17
```

### 可变Map

```kt
fun main() {
    val mutableMap = mutableMapOf("Yorick" to 21, "Lily" to 20, "Jerry" to 17)
    mutableMap += "Morty" to 16
    // 使用put增加
    mutableMap.put("Morty", 15)
    // 获取不到则放入
    mutableMap.getOrPut("kimmy") { 11 }
}
```

## Stack

使用kotlin实现Stack与LinkedList

[Kotlin中Stack与LinkedList的实现方法示例 - 腾讯云开发者社区-](https://cloud.tencent.com/developer/article/1741702)