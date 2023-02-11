---
title: Kotlin互操作性与可空性
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-15 16:09:08
tags: 
sticky: 
---

## 互操作性与可空性

- [互操作性与可空性](#互操作性与可空性)
  - [互操作性与可空性](#互操作性与可空性-1)
  - [类型映射](#类型映射)
  - [属性、异常与互操作](#属性异常与互操作)
    - [属性访问](#属性访问)
    - [Java调用Kotlin](#java调用kotlin)
      - [@file:JvmName("name")](#filejvmnamename)
      - [@JvmField](#jvmfield)
      - [@JvmOverloads](#jvmoverloads)
      - [伴生对象和@JvmStatic](#伴生对象和jvmstatic)
    - [@Throws](#throws)
  - [函数类型操作](#函数类型操作)

### 互操作性与可空性

Java世界里所有对象都可能是null，当一个Kotlin函数返回String类型值，你不能想当然地认为它的返回值就能符合Kotlin关于空值的规定。

新建Jhava类
```java
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Jhava {
    @NotNull
    public String utterGreeting() {
        return "HELLO";
    }

    @Nullable
    public String determineFriendshipLevel() {
        return null;
    }
}
```

### 类型映射

代码运行时，所有的映射类型都会重新映射回对应的Java类型。

```kt
val hitPoint = adversary.hitPoints
println(hitPoint.dec()) // 999
println(hitPoint.javaClass) // int
```

### 属性、异常与互操作

#### 属性访问

```java
public int getHitPoints() {
    System.out.println("-------getHitPoints-------");
    return hitPoints;
}

public void setHitPoints(int hitPoints) {
    System.out.println("-------setHitPoints-------");
    this.hitPoints = hitPoints;
}
```
不需要调用相关getter，setter方法，你可以使用`对象名.字段名`来获取或者设置一个Java类的字段值。实际上还是暗中调用了getter，setter方法。
```kt
adversary.hitPoints = 888
println(adversary.hitPoints)
// -------setHitPoints-------
// -------getHitPoints-------
// 888
```

#### Java调用Kotlin

##### @file:JvmName("name") 

Kotlin在类Hreo中定义方法
```kt
fun makeProclamation() = "Greetings,beast!"
```
Java在主方法中调用
```Java
public static void main(String[] args) {
    System.out.println(HeroKt.makeProclamation());
}
```
修改编译后Kotlin文件的名字，在文件首行加上
```kt
@file:JvmName("Hero") 
```
Java在调用就可以使用新名字
```Java
public static void main(String[] args) {
    System.out.println(Hero.makeProclamation());
}
```

##### @JvmField

正常使用Java获取或者修改Kotlin类的属性时，Kotlin会提供自动生成的getter，setter方法。

Kotlin类
```kt
class SpellsBook {
    val spells = listOf("Magic Wu Wu", "Lay on Hans")
}
```
Java在主方法中使用

```Java
SpellsBook spellsBook = new SpellsBook();
spellsBook.getSpells();
```

为Kotlin类的属性添加`@JvmField`注解，你就可以使用`对象名.字段名`来获取或者设置一个Java字段值
```kt
class SpellsBook {
    @JvmField
    val spells = listOf("Magic Wu Wu", "Lay on Hans")
}
```

```java
SpellsBook spellsBook = new SpellsBook();
List<String> list =  spellsBook.spells;
for (String s : list) {
    System.out.println(s);
}
// Magic Wu Wu
// Lay on Hans
```
##### @JvmOverloads

`@JvmOverloads`注解协助产生Kotlin函数的重载版本。设计一个可能会暴露给Java用户使用的API时，记得使用`@JvmOverloads`注解，这样，无论你是Kotlin开发者还是Java开发者，都会对这个API的可靠性感到满意。

```kt
fun handoverFood(leftHand: String = "berries", rightHand: String = "beef") {
    println("Emmmm... you hand over some delicious $leftHand and $rightHand")
}
```

在kt中调用没有参数个数问题，但是在Java中如果只填入一个参数，另一个想使用默认值，就会报错，为了解决这个问题，使用`@JvmOverloads`注解。
```kt
@JvmOverloads
fun handoverFood(leftHand: String = "berries", rightHand: String = "beef") {
    println("Emmmm... you hand over some delicious $leftHand and $rightHand")
}
```
在Java中调用不报错了
```java
Hero.handoverFood("apple");
```

##### 伴生对象和@JvmStatic

`@JvmField`注解还能用来以静态方式提供伴生对象里定义的值。
`@JvmStatic`注解的作用类似于`@JvmField`，允许你直接调用伴生对象里的函数。

Kotlin类定义伴生对象
```kt
class SpellsBook {
    @JvmField
    val spells = listOf("Magic Wu Wu", "Lay on Hans")
    companion object{
        @JvmField
        val MAX_SPELLS_COUNT = 10
        @JvmStatic
        fun getSpellsBookGreeting() = println("I am the greatest Magician")
    }
}
```
在Java中调用
```java
System.out.println(SpellsBook.MAX_SPELLS_COUNT); // 10
SpellsBook.getSpellsBookGreeting(); // I am the greatest Magician
```

#### @Throws

抛出一个需要检查的指定异常，Java和Kotlin有关异常检查的差异让`@Throws`注解给解决掉了，在编写供Java开发者调用的Kotlin API时，要考虑使用`@Throws`注解，这样，用户就知道怎么正确处理任何异常了。

在Java抛出的异常Kotlin不会强制提示在编译时处理，反之亦然。

（1）在Java类中抛出异常
```java
public void extendHandInFriendship() throws IOException{
    throw new IOException();
}
```
Kotlin中调用会抛出异常的类并没有报错，但是如果运行还是会报错
```kt
adversary.extendHandInFriendship() // 没有报错
```
---
（2）在Kotlin中抛出异常
```kt
fun acceptApology() {
    throw IOException()
}
```
Java中并没有强制编译时处理
```java
Hero.acceptApology();
```
尝试用try catch处理，却报错
```kt
try {
    Hero.acceptApology();
}catch (IOException e){ // 报错
    System.out.println("Caught!");
}
```
反编译成Java发现，原来Kotlin在编译时把IOException强制转换成了Throwable类型
```java
public static final void acceptApology() {
      throw (Throwable)(new IOException());
   }
```

在try catch将IOException改为Throwable发现报错消失

```kt
try {
    Hero.acceptApology();
}catch (Throwable e){ // 报错消失
    System.out.println("Caught!");
}
```
----
但是如果我们要正常处理IOException，而且强制编译时处理，就要给kt里抛出错误的方法加上`@Throws`注释。

```kt
@Throws(IOException::class)
fun acceptApology() {
    throw IOException()
}
```
此时java里try-catch不报错

### 函数类型操作

函数类型和匿名函数能提供高效的语法用于组件间的交互，是Kotlin编程语言里比较新颖的特性。他们简洁的语法因->操作符而实现，但Java8之前的JDK版本并并不支持lambda表达式。在Java里，Kotlin函数类型使用FunctionN这样的名字的接口来表示的，FunctionN中的N代表值参数目。这样的Function接口由23个，从Function0到Function22，每一个FunctionN都包含一个invoke函数，专用于调用函数类型函数，所以，在何时候需要调一个函数类型，都用它调用invoke。

在kt类中添加一个translator的函数类型
```kt
// 添加一个translator的函数类型，接收一个字符串
// 将其改为小写字母，再大写第一个字符，最后打印结果。
val translator = { utterance: String ->
    println(utterance.lowercase().capitalize())
}
```
在Java主方法中调用
```java
Function1<String, Unit> translator = Hero.getTranslator();
translator.invoke("HELLO"); // Hello
```

