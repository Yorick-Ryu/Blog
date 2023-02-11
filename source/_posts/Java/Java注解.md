---
title: Java注解
index_img: /img/default.png
categories: 
  - Java
date: 2022-04-30 10:33:57
tags: 
  - 注解
  - Annotation
sticky: 
---

# Java注解

- [Java注解](#java注解)
    - [注解概述](#注解概述)
    - [基本的Annotation](#基本的annotation)
    - [自定义Annotation](#自定义annotation)
    - [提取Annotation信息](#提取annotation信息)
    - [JDK的元Annotation](#jdk的元annotation)

### 注解概述

Annotation其实就是代码里的特殊标记，这些标记可以在编译，类加载，运行时被读取，并执行相应的处理。通过使用Annotation，程序员可以在不改变原有逻辑的情况下，在源文件中嵌入一些补充信息。
Annotation可以像修饰符一样被使用，可用于修饰包，类，构造器，方法，成员变量，参数，局部变量的声明，这些信息被保存在Annotation的`name = value`对中。

### 基本的Annotation

使用Annotation时要在其前面增加@符号，并把该Annotation当成一个修饰符使用，用于修饰它支持的程序元素。  

三个基本的Annotation:
- @Override:限定重写父类方法，该注释只能用于方法。
- @Deprecated:用于表示某个程序元素(类，方法等)已过时
- @SuppressWarnings:抑制编译器警告。

实例：
```java
public class TestAnnotation {
    @SuppressWarnings("unused")
    public static void main(String[] args) {

        A a = new A();
        a.method2();

        String str = "abc";
    }
}

class A{
    void method1(){}

    @Deprecated
    void method2(){}
}

class B extends A{

    @Override
    void method1(){}
}
```

### 自定义Annotation
定义新的Annotation类型使用`@interface`关键字。
Annotation的成员变量在Annotation定义中以无参数方法的形式来声明，其方法名和返回值定义了该成员的名字和类型（类似接口方法声明）。
可以在定义Annotation的成员变量时为其指定初始值，指定成员变量的初始值可使用default关键字。
没有成员定义的Annotation称为标记；包含成员变量的Annotation称为元数据Annotation。

实例：

定义注解HelloAnnotation
```java
public @interface HelloAnnotation {
    //指定成员变量的初始值可使用default关键字
    public String name() default "";
}
```
使用注解HelloAnnotation
```java
@HelloAnnotation()//用了default，可空
class A{
    @HelloAnnotation(name = "method")
    void method1(){}
}
```
### 提取Annotation信息

反射

### JDK的元Annotation
JDK的元Annotation用于修饰其他Annotation定义

@Retention:只能用于修饰一个Annotation定义，用于指定该Annotation可以保留多长时间，@Rentention包含一个RetentionPolicy类型的成员变量，使用@Rentention时必须为该value成员变量指定值:
- RetentionPolicy.CLASS:编译器将把注释记录在class文件中.当运行Java程序时，JVM不会保留注释。这是默认值
- RetentionPolicy.RUNTIME:编译器将把注释记录在class文件中，当运行Java程序时，JVM会保留注释。程序可以通过反射获取该注释（常用）
- RetentionPolicy.SOURCE:编译器直接丢弃这种策略的注释

@Target：用于修饰Annotation定义，用于指定被修饰的Annotation能用于修饰哪些程序元素。@Target也包含一个名为value的成员变量。
```java
//限定此注解只能修饰方法和类
@Target(value = {ElementType.METHOD,ElementType.TYPE})
public @interface HelloAnnotation {
    public String name() default "";
}
```
@Documented:用于指定被该元Annotation修饰的Annotation类将被javadoc工具提取成文档。
@Inherited:被它修饰的Annotation将具有继承性。如果某个类使用了被@Inherited修饰的Annotation，则其子类将自动具有该注释


