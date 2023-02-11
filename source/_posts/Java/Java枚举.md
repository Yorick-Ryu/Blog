---
title: Java枚举
index_img: /img/default.png
categories: 
  - Java
date: 2022-04-28 16:51:48
tags: 
  - 枚举
  - enum
sticky: 
---

# 枚举

- [枚举](#枚举)
    - [定义](#定义)
    - [自实现枚举类](#自实现枚举类)
    - [使用enum定义枚举类](#使用enum定义枚举类)
    - [实现接口的枚举类](#实现接口的枚举类)
    - [枚举类的方法](#枚举类的方法)

### 定义
枚举类概述:
在某些情况下，一个类的对象是有限而且固定的，例如季节类，只能有4个对象
手动实现枚举类∶
- `private`修饰构造器
- 属性使用`private final`修饰
- 把该类的所有实例都使用`public static final`来修饰
### 自实现枚举类
定义Season类
实例：
```java
public class Season {

    //1.因为枚举类的对象是有限个，所以不能在类的外部创建类的对象
    private Season(String name, String desc) {
        this.name = name;
        this.desc = desc;
    }

    //2.因为对象是固定的,所以属性是常量
    private final String name;
    private final String desc;

    //3.在类的内部创建对象，但需要在类的外部能访问到该对象，而且还不能更改
    public static final Season SPRING = new Season("春天", "春风又绿江南岸");
    public static final Season SUMMER = new Season("夏天", "映日荷花别样红");
    public static final Season AUTUMN = new Season("秋天", "秋水共长天一色");
    public static final Season WINTER = new Season("冬 天", "窗含西岭千秋雪");

    public String getName() {
        return name;
    }

    public String getDesc() {
        return desc;
    }

    @Override
    public String toString() {
        return "Season{" +
                "name='" + name + '\'' +
                ", desc='" + desc + '\'' +
                '}';
    }
}
```
测试:
```java
public class SeasonTest {
    public static void main(String[] args) {
        Season SPRING = Season.SPRING;
        System.out.println(SPRING);
    }
}
//输出：Season{name='春天', desc='春风又绿江南岸'}
```
### 使用enum定义枚举类
枚举类和普通类的区别:
- 使用enum定义的枚举类默认继承了java.lang.Enum类
- 枚举类的构造器只能使用private 访问控制符
- 枚举类的所有实例必须在枚举类中显式列出(,分隔;结尾).列出的实例系统会自动添加 public static final修饰
- 所有的枚举类都提供了一个values方法,该方法可以很方便地遍历所有的枚举值

若枚举只有一个成员，则可以作为一种单子模式的实现方式


实例：
```java
public enum Season2 {
    //必须在枚举类的第一行写出有哪些枚举值。
    SPRING("春天", "春风又绿江南岸"),
    SUMMER("夏天", "映日荷花别样红"),
    AUTUMN("秋天", "秋水共长天一色"),
    WINTER("冬天", "窗含西岭千秋雪");

    Season2(String name, String desc) {
        this.name = name;
        this.desc = desc;
    }

    public String getName() {
        return name;
    }

    public String getDesc() {
        return desc;
    }

    private final String name;
    private final String desc;
    
    @Override
    public String toString() {
        return "Season2{" +
                "name='" + name + '\'' +
                ", desc='" + desc + '\'' +
                '}';
    }
}
```
测试：
```java
System.out.println(Season2.SPRING);
//Season2{name='春天', desc='春风又绿江南岸'}
//所有的枚举类都提供了一个values方法,该方法可以很方便地遍历所有的枚举值
        for (Season2 s :Season2.values()){
            System.out.println(s);
        }
/*
Season2{name='春天', desc='春风又绿江南岸'}
Season2{name='夏天', desc='映日荷花别样红'}
Season2{name='秋天', desc='秋水共长天一色'}
Season2{name='冬天', desc='窗含西岭千秋雪'}
*/
```

### 实现接口的枚举类

和普通Java类一样枚举类可以实现一个或多个接口
若需要每个枚举值在调用实现的接口方法呈现出不同的行为方式,则可以让每个枚举值分别来实现该方法

实例：
定义TimeInfo接口
```java
public interface TimeInfo {
    public String getTimeInfo();
}
```
修改Season2类
```java
SPRING("春天", "春风又绿江南岸"){
        @Override
        public String getTimeInfo() {
            return "2-5";
        }
    },
    SUMMER("夏天", "映日荷花别样红") {
        @Override
        public String getTimeInfo() {
            return "5-8";
        }
    },
    AUTUMN("秋天", "秋水共长天一色") {
        @Override
        public String getTimeInfo() {
            return "8-11";
        }
    },
    WINTER("冬天", "窗含西岭千秋雪") {
        @Override
        public String getTimeInfo() {
            return "11-2";
        }
    };
```
测试：
```java
for (Season2 s :Season2.values()){
    System.out.println(s);
    System.out.println(s.getTimeInfo());
}
/*输出：
SPRING
2-5
SUMMER
5-8
AUTUMN
8-11
WINTER
11-2
*/
```

### 枚举类的方法

使用一个字符串获取对应的枚举类对象，可以使用valueof 方法
```java
Season2 s = Season2.valueOf(Season2.class,str);
System.out.println(s.getName());
```