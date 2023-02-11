---
title: Kotlin函数
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-05 09:53:57
tags: 
sticky: 
---

## Kotlin函数

- [Kotlin函数](#kotlin函数)
  - [函数头](#函数头)
  - [函数参数](#函数参数)
  - [Unit函数](#unit函数)
  - [Nothing类型](#nothing类型)
  - [反引号中的函数名](#反引号中的函数名)

### 函数头

```Kotlin
     private       fun        doSomething(age:Int, flag:Boolean) : String
// 可见行修饰符  函数声明关键字   函数名            函数参数          返回类型
```

### 函数参数 

（1）默认值参

如果不打算传入值参，可以预先给参数指定默认值

```Kotlin
fun fix(name: String, age: Int = 6) {
    println(name + age)
}
// 主函数
fun main() {
    fix("Yorick")
}
```

（2）具名函数参数

如果使用命名值参，就可以不用管值参的顺序

```Kotlin
fun main() {
    fix(age = 9, name = "Jerry")
}
```

### Unit函数

不是所有函数都有返回值，Kotlin中没有返回值的函数叫Unit函数，也就是说他们的返回类型是Unit。在Kotlin之前，函数不返回任何东西用void描述，意思是"没有返回类型，不会带来什么，忽略它"，也就是说如果函数不返回任何东西，就忽略类型。但是，void这种解决方案无法解释现代语言的一个重要特征，泛型。

```Kotlin
println(fix("Yorick"))
// 输出
// Yorick6
// kotlin.Unit
```

### Nothing类型

TODO函数的任务就是抛出异常，就是永远别指望它运行成功，返回Nothing类型

```Kotlin
TODO("nothing")
// 下面语句不会被执行
println("after nothing")
```
TODO函数本身就是返回一个异常
```kotlin
public inline fun TODO(reason: String): Nothing = throw NotImplementedError("An operation is not implemented: $reason")
```

### 反引号中的函数名

（1）可以给函数起奇怪的名字（小心被打死qaq）
```Kotlin
// 定义
fun `****Yorick is the best****`(name: String){
    println(name+"666")
}
// 调用
`****Yorick is the best****`("Yorick")
// 输出
// Yorick666
```
（2）由于Java和Kotlin可以相互调用，但是两者关键字不同，众所周知，关键字不能作为变量名或者标识符，所以有时候要加反引号。

- 新建MyJava类定义is静态方法
```Kotlin
public class MyJava {
    public static void is(){
        System.out.println("IS");
    }
}
```
- 在Kotlin中调用is方法
```Kotlin
fun main() {
    MyJava.`is`();
}
// 输出
IS
```