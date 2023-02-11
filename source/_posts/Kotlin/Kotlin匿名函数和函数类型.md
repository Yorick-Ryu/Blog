---
title: Kotlin匿名函数和函数类型
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-05 11:04:38
tags: 
sticky: 
---

## 匿名函数和函数类型

- [匿名函数和函数类型](#匿名函数和函数类型)
  - [匿名函数](#匿名函数)
    - [函数类型与隐式返回](#函数类型与隐式返回)
    - [函数参数](#函数参数)
    - [it关键字](#it关键字)
  - [类型推断](#类型推断)
  - [什么是lambda](#什么是lambda)
  - [定义参数是函数的函数](#定义参数是函数的函数)
  - [函数內联](#函数內联)
  - [函数引用](#函数引用)
  - [函数类型作为返回值类型](#函数类型作为返回值类型)
  - [lambda与闭包](#lambda与闭包)
  - [lambda与内部匿名类](#lambda与内部匿名类)

### 匿名函数

定义时不取名字的函数，我们称之为匿名函数，匿名函数通常整体传递给其他函数，或者从其他函数返回。

匿名函数对Kotlin来说很重要，有了它，我们能够根据需要制定特殊规则，轻松定制标准库里的内置函数。

```Kotlin
fun main() {
    val total = "MISSSSSSSYOU".count()
    val count = "MISSSSSSSYOU".count({ letter ->
        letter == 'S'
    })
    println(total)
    println(count)
}
```

#### 函数类型与隐式返回

匿名函数也有类型，可以直接赋值给函数类型变量。

匿名函数一般不需要return，会隐式或自动返回函数体最后一行语句的结果。

```Kotlin
// 定义变量，类型为返回值为String的匿名函数
val blessingFun:()->String = {
    val holiday = "National Day"
    // 自动返回函数体最后一行语句的结果
    "Happy $holiday"
}
// 也可用先声明，后赋值
val blessingFun:()->String
blessingFun = {
    val holiday = "National Day"
    "Happy $holiday"
}
```

#### 函数参数

匿名函数需要带参数时，参数的类型放在匿名函数的参数定义中，参数名(形参)放在函数定义中。

```Kotlin
//               参数类型   返回值类型  参数名(形参)
val blessingFun: (String) -> String = { name ->
    val holiday = "New Year"
    "$name,Happy $holiday!"
}
println(blessingFun("Yorick"))
// 输出
// Yorick,Happy New Year!
```
#### it关键字

定义只有一个参数的匿名函数时，可以用`it`关键字表示参数名。
```Kotlin
val blessingFun: (String) -> String = {
    val holiday = "New Year"
    // it关键字表示参数名
    "$it,Happy $holiday"
}
println(blessingFun("Yorick"))
// 输出
// Yorick,Happy New Year!
```

### 类型推断

定义变量时，如果已把匿名函数作为变量赋值，就不需要显式指明变量类型。
```Kotlin
val blessingFun = {
    val holiday = "National Day"
    "Happy $holiday"
}
println(blessingFun())
// 输出
// Happy National Day
```
当匿名函数有参数时，也可以省略变量类型，但是在匿名函数內要定义参数类型。

- 不省略变量类型
```Kotlin
val blessingFun:(String,Int)->String={name,year->
    val holiday = "New Year"
    "$name,Happy $holiday $year!"
}
println(blessingFun("Yorick",2022))
// 输出
// Yorick,Happy New Year 2022!
```
- 省略变量类型
```Kotlin
val blessingFun = { name: String, year: Int ->
    val holiday = "New Year"
    "$name,Happy $holiday $year!"
}
println(blessingFun("Yorick",2022))
// 输出
// Yorick,Happy New Year 2022!
```

### 什么是lambda

我们将匿名函数称为lambda，将它的定义称为lambda表达式，它返回的数据称为lambda结果。

### 定义参数是函数的函数

函数的参数是另一个函数

```Kotlin
fun main() {
    val getRefreshWords = { name: String, sec: Int ->
        "${name}还有${sec}秒刷新！"
    }
    showOnBoard("主宰", getRefreshWords)
}

fun showOnBoard(name: String, getRefreshWords: (String, Int) -> String) {
    val sec = (1..60).shuffled().last()
    println(getRefreshWords(name, sec))
}
// 输出示例
// 主宰还有18秒刷新！
```
可怕的是，它还有省略写法！

如果一个函数的lambda参数排在最后，或者是唯一的参数，那么括住lambda值参的一对圆括号就可以稍等。
```Kotlin
fun main() {
    showOnBoard("主宰") { name: String, sec: Int ->
        "${name}还有${sec}秒刷新！"
    }
}

private fun showOnBoard(name: String, getRefreshWords: (String, Int) -> String) {
    val sec = (1..60).shuffled().last()
    println(getRefreshWords(name, sec))
}
// 输出示例
// 主宰还有18秒刷新！
```
### 函数內联

lambda使用方便灵活，但是灵活是有代价的。
在JVM上，你定义的lambda会以对象的实例形式存在，JVM会为所有同lambda打交道的变量分配内存，这就产生了内存开销，这会带来严重的性能问题。幸运的是，kotlin有一种优化机制叫内联，有了内联，JVM就不需要使用lambda对象实例了，因而避免了变量内存分配。哪里需要使用lambda，编译器就会将函数体复制粘贴到哪里。

没有使用内联的Kotlin代码
```Kotlin
fun main() {
    val getRefreshWords = { name: String, sec: Int ->
        "${name}还有${sec}秒刷新！"
    }
    showOnBoard("主宰", getRefreshWords)
}

private fun showOnBoard(name: String, getRefreshWords: (String, Int) -> String) {
    val sec = (1..60).shuffled().last()
    println(getRefreshWords(name, sec))
}
```
反编译成Java的部分代码
```java
public final class AnonymousFunc2Kt {
   public static final void main() {
      Function2 getRefreshWords = (Function2)null.INSTANCE;
      showOnBoard("主宰", getRefreshWords);
   }

   // $FF: synthetic method
   public static void main(String[] var0) {
      main();
   }

   private static final void showOnBoard(String name, Function2 getRefreshWords) {
      byte var3 = 1;
      int sec = ((Number)CollectionsKt.last(CollectionsKt.shuffled((Iterable)(new IntRange(var3, 60))))).intValue();
      Object var4 = getRefreshWords.invoke(name, sec);
      System.out.println(var4);
   }
}
```
我们发现main函数里只有两行代码，需要调用实例化后的lambda函数才能运行。

在函数showOnBoard的private后加入inline
```Kotlin
...
private inline fun showOnBoard(name: String, getRefreshWords: (String, Int) -> String)
...
```
此时反编译后的Java代码的主方法：
```java
public static final void main() {
    Function2 getRefreshWords = (Function2)null.INSTANCE;
    String name$iv = "主宰";
    int $i$f$showOnBoard = false;
    byte var3 = 1;
    int sec$iv = ((Number)CollectionsKt.last(CollectionsKt.shuffled((Iterable)(new IntRange(var3, 60))))).intValue();
    Object var5 = getRefreshWords.invoke(name$iv, sec$iv);
    System.out.println(var5);
}
```
我们发现主方法多了很多，这是因为他复制了lambda函数体里的代码，直接运行，不再去实例化lambda函数。

但是，使用lambda递归函数无法内联，因为会导致复制粘贴无限循环，编译会发出警告。

例如，这里的递归函数就不能使用内联。
```kotlin
fun main() {
    add(1, 2, show)
}

var sum = 0
val show: (Int) -> (String) = {
    println(it)
    it.toString()
}

fun add(num1: Int, num2: Int, show: (Int) -> (String)) {
    sum = num1 + num2
    if (sum < 100) {
        show(sum)
        // 递归
        add(num2, sum, show)
    }
}
```

### 函数引用

要把函数作为参数传给其他函数使用，除了传lambda表达式，kotlin还提供了其他方法，传递函数引用，函数引用可以把一个具名函数转换成一个值参，可以使用lambda表达式的地方，都可以使用函数引用。
```Kotlin
fun main() {
    // ::表示把一个方法当做一个参数，传递到另一个方法中进行使用，通俗的来讲就是引用一个方法。
    showOnBoard("主宰", ::getRefreshWords)
}

fun getRefreshWords(name: String, sec: Int): String {
    return "${name}还有${sec}秒刷新！"
}

private inline fun showOnBoard(name: String, getRefreshWords: (String, Int) -> String) {
    val sec = (1..60).shuffled().last()
    println(getRefreshWords(name, sec))
}
```

### 函数类型作为返回值类型

```Kotlin
fun main() {
    val getRefreshWords = configRefreshWords()
    println(getRefreshWords("主宰"))
}

fun configRefreshWords(): (String) -> String {
    val sec = (1..60).shuffled().last()
    return { name: String ->
        "${name}还有${sec}秒刷新！"
    }
}
// 输出示例
// 主宰还54有秒刷新！
```

### lambda与闭包

闭包：能够读取其他函数内部变量的函数

在Kotlin中，匿名函数能修改并引用定义在自己的作用域之外的变量。lambda就是匿名函数，所以Kotlin中的lambda就是闭包。


### lambda与内部匿名类

我们知道Kotlin可以把函数作为另一个函数的参数，那如何用Java实现呢？

这就要使用Java里的接口和内部类
```java
import java.util.Random;

public class JavaAnonymousClass {
    public static void main(String[] args) {
        showOnBoard("主宰", new MyRefreshWords());
    }

    public interface RefreshWords {
        String getRefreshWords(String name, int sec);
    }

    public static void showOnBoard(String name, RefreshWords refreshWords) {
        int sec = new Random().nextInt(60);
        System.out.println(refreshWords.getRefreshWords(name, sec));
    }

    static class MyRefreshWords implements RefreshWords {
        @Override
        public String getRefreshWords(String name, int sec) {
            return name + "还有" + sec + "秒刷新！";
        }
    }
}
```
或者使用匿名内部类
```java
import java.util.Random;

public class JavaAnonymousClass {
    public static void main(String[] args) {
        showOnBoard("主宰", new RefreshWords() {
            @Override
            public String getRefreshWords(String name, int sec) {
                return name + "还有" + sec + "秒刷新！";
            }
        });
    }

    public interface RefreshWords {
        String getRefreshWords(String name, int sec);
    }

    public static void showOnBoard(String name, RefreshWords refreshWords) {
        int sec = new Random().nextInt(60);
        System.out.println(refreshWords.getRefreshWords(name, sec));
    }
}
```
Java8 以后支持lambda表达式，那么main方法可以写成：
```java
public static void main(String[] args) {
    showOnBoard("主宰", (name, sec) -> name + "还有" + sec + "秒刷新！");
}
```
可以看出，还是kotlin的简洁，函数类型可以让开发者少写模式代码，写出更灵活的代码。