---
title: Kotlin面向对象_定义类和初始化
index_img: ./img/init_order.png
categories: 
  - kotlin
date: 2022-09-10 16:22:35
tags: 
sticky: 
---

# 面向对象

- [面向对象](#面向对象)
  - [定义类](#定义类)
    - [定义类与field关键字](#定义类与field关键字)
    - [计算属性](#计算属性)
    - [防范竞态条件](#防范竞态条件)
  - [初始化](#初始化)
    - [主构造函数](#主构造函数)
    - [在主构造函数里定义属性](#在主构造函数里定义属性)
    - [次构造函数](#次构造函数)
    - [默认参数](#默认参数)
    - [初始化块](#初始化块)
    - [初始化顺序](#初始化顺序)
    - [延迟初始化](#延迟初始化)
    - [惰性初始化](#惰性初始化)
    - [初始化陷阱](#初始化陷阱)

## 定义类

### 定义类与field关键字

在Kotlin中，定义类的属性后会自动生成默认getter和setter方法（可变属性才有），使用形如`p.name`的方法获取或者修改对象属性时，本质是调用了自动生成的getter和setter方法，可以从反编译成java的代码中看出。

同时也会自动生成field关键字，来储存属性数据，只可以在重新getter和setter方法时使用。

```kt
// 定义类
class Player {
    var name = "yorick"
        get() = field.capitalize()
        set(value) {
            field = value.trim()
        }
}

fun main() {
    val p = Player()
    println(p.name)
    p.name = " Alex "
    println(p.name)
}
// 输出
// Yorick
// Alex
```
反编译成java的主方法的Player类
```java
public final class Player {
   @NotNull
   private String name = "yorick";

   @NotNull
   public final String getName() {
      return StringsKt.capitalize(this.name);
   }

   public final void setName(@NotNull String value) {
      Intrinsics.checkNotNullParameter(value, "value");
      this.name = StringsKt.trim((CharSequence)value).toString();
   }
}
```
反编译成java的主方法
```java
public static final void main() {
    Player p = new Player();
    String var1 = p.getName();
    System.out.println(var1);
    p.setName(" Alex ");
    var1 = p.getName();
    System.out.println(var1);
}
```

### 计算属性

计算属性是通过一个覆盖的get或set运算符来定义，这时field就不需要了。有点函数的意思。

```kt
class Player {
    val rolledValue
        get() = (1..6).shuffled().first()
}

fun main() {
    val p = Player()
    println(p.rolledValue)
}
// 示例输出
// 2
```

### 防范竞态条件

如果一个类属性既可空又可变，那么引用它之前你必须保证它非空，一个办法是用also标准函数。


```kt
class Player {
    var words: String? = "Hello"
    fun saySomething() {
        words?.also {
            println("Hello ${it.toUpperCase()}")
        }
    }
}

fun main() {
    val p = Player()
    p.saySomething()
}
// 输出
// Hello HELLO
```

## 初始化

### 主构造函数

我们在Player类的定义头中定义一个主构造函数，使用临时变量为Player的各个属性提供初始值，在Kotlin中，为便于识别，临时变量（包括仅引用一次的参数），通常都会以下划线开头的名字命名。

```kotlin
class Player(
    _name: String,
    _age: Int,
    _isNormal: Boolean
) {
    var name = _name
        get() = field.capitalize()
        private set(value) {
            field = value.trim()
        }
    var age = _age
    var isNormal = _isNormal
}

fun main() {
    val player = Player("Yorick", 22, true)
    println(player.name)
}
```
### 在主构造函数里定义属性

```kotlin
class Player(
    _name: String,
    var age: Int,
    var isNormal: Boolean
) {
    var name = _name	
        get() = field.capitalize()
        private set(value) {
            field = value.trim()
        }
}

fun main() {
    val player = Player("Yorick", 22, true)
    println(player.name)
}
```

### 次构造函数

我们可以定义多个此构造函数来配置不同的参数组合，同时初始化代码逻辑。
```kotlin
class Player(
    _name: String,
    var age: Int,
    var isNormal: Boolean
) {
    var name = _name
        get() = field.capitalize()
        private set(value) {
            field = value.trim()
        }
    // 次构造函数
    constructor(_name: String) : this(_name, age = 10, isNormal = true) {
        this.name = _name.uppercase()
    }
}

fun main() {
    val p1 = Player("Yorick", 22, true)
    println(p1.name)
    val p2 = Player("hobo")
    println("${p2.name} ${p2.age} ${p2.isNormal}")
}
// 输出
// Yorick
// HOBO 10 true
```

### 默认参数

定义构造函数时，可以给构造函数参数指定默认值，如果用户调用时不提供值参，就使用这个默认值。

```kotlin
class Player(
    _name: String,
    var age: Int = 20,
    var isNormal: Boolean
) {
    var name = _name
        get() = field.capitalize()
        private set(value) {
            field = value.trim()
        }

    constructor(_name: String) : this(_name, age = 10, isNormal = true) {
        this.name = _name.uppercase()
    }
}

fun main() {
    // 可以按顺序传参，指定参数名称就行
    val player = Player("Yorick", isNormal = true)
    println(player.age) // 20
}
```

### 初始化块

初始化块可以设置变量或值，以及执行有效性检查，如检查传给某构造函数的值是否有效，初始化块代码会在构造类实例时执行。在次构造函数执行之前就执行。

```kotlin
class Player(
    _name: String,
    var age: Int,
    var isNormal: Boolean
) {
    var name = _name
        get() = field.capitalize()
        private set(value) {
            field = value.trim()
        }

    constructor(_name: String) : this(_name, age = 10, isNormal = true) {
        this.name = _name.uppercase()
    }

    // 在实例化时执行
    init {
        require(age > 0) { "age must be positive" }
        require(name.isNotBlank()) { "player must have a name" }
    }
}
fun main() {
    val player = Player("", -1, true)
    // 异常 IllegalArgumentException
}
```

### 初始化顺序

- 主构造函数里声明的属性
- 类级别的属性赋值
- init初始化块里的属性赋值和函数调用
- 次构造函数里的属性赋值和函数调用

![init_order](./img/init_order.png)

### 延迟初始化

我们知道，一般来说，类的属性在初始化时不能为空，但有的时候我们不得不先让其为空，在使用之前赋值，然后再初始化使用。这时候就用到了延迟初始化。

使用lateinit关键字相当于做了一个约定：在用它之前负责初始化

注意：

- lateinit 对应使用var来声明属性
- lateinit 不可以修饰原始数据类型（byte，char，short ,int，long，float，double）


```kotlin
class BattlePlayer {
    // 在使用之前初始化
    lateinit var equipment:String
    fun ready(){
        equipment = "RPG"
    }
    fun battle(){
        println(equipment)
    }
}

fun main() {
    val player = BattlePlayer()
    player.ready() // 若注释掉此行，则异常 kotlin.UninitializedPropertyAccessException: lateinit property equipment has not been initialized
    player.battle()
}
```

为了保证安全，只要无法确认lateinit变量是否完成初始化，可以执行isInitialized检查

```kotlin
class BattlePlayer {
    // 在使用之前初始化
    lateinit var equipment: String
    fun ready() {
        equipment = "RPG"
    }

    fun battle() {
        if (::equipment.isInitialized) println(equipment)
    }
}

fun main() {
    val player = BattlePlayer()
    player.ready()
    player.battle()
}
```

### 惰性初始化

延迟初始化并不是推后初始化的唯一方式，你也可以暂时不初始化某个变量，直到首次使用它，这个叫作惰性初始化。

与lateinit的区别，惰性初始化是配置好的、自动执行的。而lateinit需要手动赋值。

```kotlin
class LazyPayer(_name: String) {
    var name = _name

    val config by lazy { loadConfig() }
    private fun loadConfig(): String {
        println("loading...")
        return "Config is ready!"
    }
}

fun main() {
    val player = LazyPayer("Jerry")
    Thread.sleep(3000)
    println(player.config) // 在执行此行时输出 loading... Config is ready!
}
```
对比正常初始化：
```kotlin
class LazyPayer(_name: String) {
    var name = _name

    val config = loadConfig()
    private fun loadConfig(): String {
        println("loading...")
        return "Config is ready!"
    }
}

fun main() {
    val player = LazyPayer("Jerry") // 输出 loading...
    println(player.config) // 输出 Config is ready!
}
```
### 初始化陷阱

（1）Kotlin的编译顺序
```kotlin
class InitPlayer() {
    init {
        val bloodBonus = blood.times(4)
    }
    val blood = 100
}
// 编译报错：Variable 'blood' must be initialized
```

编译报错：Variable 'blood' must be initialized

原因：Kotlin是自上而下编译代码，所以应该先声明类属性

修改后正常运行
```kotlin
class InitPlayer() {
    val blood = 100
    init {
        val bloodBonus = blood.times(4)
    }
}
```
（2）
```kotlin
class InitPlayer() {
    private val name: String
    private fun firstLetter() = name[0]

    init {
        println(firstLetter())
        name = "iKun"
    }
}

fun main() {
    InitPlayer()
}
// 运行时异常NullPointerException
```
原因：init块在类属性定义之后运行，类方法在调用时运行，但是类方法试图在类属性赋值前获取属性值，这必然导致空指针。


修改后正常运行
```kotlin
class InitPlayer() {
    private val name: String
    private fun firstLetter() = name[0]

    init {
        name = "iKun"
        println(firstLetter())

    }
}

fun main() {
    InitPlayer()
}
```

（3）
```kotlin
class InitPlayer(_name: String) {
    val playerName: String = initPlayerName()
    val name: String = _name
    private fun initPlayerName(): String = name
}

fun main() {
    val player = InitPlayer("Jimmy")
    println(player.playerName) // null
}
```
因为编译器看到所有属性都初始化了，所以代码编译没问题，但运行结果却是null，问题出在哪？

在用initPlayerName函数初始化playerName时，name属性还未完成初始化。

修改后正常运行
```kotlin
class InitPlayer(_name: String) {
    val name: String = _name
    val playerName: String = initPlayerName()
    private fun initPlayerName(): String = name
}
fun main() {
    val player = InitPlayer("Jimmy")
    println(player.playerName) // null
}
```

