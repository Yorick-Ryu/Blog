---
title: Kotlin接口与抽象类
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-12 10:18:07
tags: 
sticky: 
---

## 接口

- [接口](#接口)
  - [接口定义](#接口定义)
  - [默认实现](#默认实现)
- [抽象类](#抽象类)

### 接口定义

Kotlin规定所有的接口属性和函数实现都要使用override关键字，接口中定义的函数并不需要open关键字修饰，他们默认就是open的。

```kotlin
interface Movable {
    var maxSpeed: Int
    var wheels: Int

    fun move(movable: Movable): String
}

class Car(_name: String, override var wheels: Int = 4) : Movable{
    override var maxSpeed: Int
        get() = TODO("Not yet implemented")
        set(value) {}

    override fun move(movable: Movable): String {
        TODO("Not yet implemented")
    }
}
```

### 默认实现

可以在接口里提供默认属性的getter方法和函数实现。

```kotlin
interface Movable {
    var maxSpeed: Int
        get() = (1..500).shuffled().last()
        set(value) {}
    var wheels: Int

    fun move(movable: Movable): String
}

class Car(_name: String, override var wheels: Int = 4) : Movable {
    override var maxSpeed: Int
        // 使用默认方法
        get() = super.maxSpeed
        set(value) {}

    override fun move(movable: Movable): String {
        TODO("Not yet implemented")
    }
}
```

## 抽象类

要定义一个抽象类，你需要在定义之前加上abstract关键字，除了具体的函数实现，抽象类也可以包含抽象函数—只有定义，没有函数实现。

```kotlin
abstract class Gun(val range: Int) {
    protected fun doSomething() {
        println("doSomething")
    }

    abstract fun pullTrigger(): String
}

class M416(val price: Int) : Gun(range = 600) {
    override fun pullTrigger(): String {
        TODO("Not yet implemented")
    }
}
```