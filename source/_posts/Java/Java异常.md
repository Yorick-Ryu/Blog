---
title: Java异常
index_img: /img/default.png
categories: 
  - Java
date: 2022-04-23 21:47:23
tags: 
  - 异常
  - Exception
sticky: 
---

## Java异常

### 分类
1. Error：JVM系统内部错误、资源耗尽等严重情况

2. Exception：其它因编程错误或偶然的外在因素导致的—般性问题,具体又分为RuntimeException、IOExeption等例如：
- 空指针访问
- 试图读取不存在的文件
- 网络连接中断

### 常见异常
1. ArithmeticException 数学异常

2. ArrayIndexOutOfBoundsException 数组越界异常

3. ClassCastException 类型转换异常

4. NullPointerException 空指针异常

### Java异常处理机制
Java采用异常处理机制，将异常处理的程序代码集中在一起，与正常的程序代码分开，使得程序简洁，并易于维护。

Java采用**抓抛模型**，java程序运行过程将异常生成异常类对象并提交JVM，这个过程称之为**抛出(throw)异常**。  

如果一个方法内抛出异常，该异常会被抛到调用方法中。如果异常没有在调用方法中处理，它继续被抛给这个调用方法的调用者。这个过程将一直继续下去，直到异常被处理。这―过程称为**捕获(catch)异常**。

如果一个异常回到`main()`方法,并且`main()`也不处理，则程序运行终止。

异常处理是通过`try-catch-finally`语句实现的。

不论在`try-catch`代码块中是否发生了异常事件,`finally`块中的语句都会被执行。

用`finally`可以没有`catch`

#### 声明抛出异常

1. 在Java中使用`throws`关键字声明抛出异常。
2. `throws`方法抛出的异常可以是方法中出现的异常的类型或其父类类型。
3. `throws`可以声明抛出多个异常，多个异常使用`,`分割。
4. 运行时异常不需要使用`throws`关键字进行显式的抛出，而编译时异常一定要处理。
5. 重写方法不能抛出比被重写方法范围更大的异常类型

#### 人工抛出异常

创建一个异常类对象，在方法内部用`throw`关键字把异常类对象抛出去

例如：
```java
public static void test() {

        //1.创建一个异常类对象
        RuntimeException ex = new RuntimeException();

        //2.把异常类对象抛出去
        throw ex;
    }
```

#### 创建用户自定义异常类

1. 用户自定义异常类通常继承自RuntimeException（也可以继承Exception）
2. 自定义的异常类就是被人工抛出的

