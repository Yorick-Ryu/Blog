---
title: Java常用类
index_img: /img/default.png
categories: 
  - Java
date: 2022-05-05 17:12:59
tags: 
  - String
  - 字符串
sticky: 
---

# Java常用类

- [Java常用类](#java常用类)
    - [String类](#string类)
      - [不可变性](#不可变性)
      - [字符串缓冲池](#字符串缓冲池)
      - [字符串常用方法](#字符串常用方法)
    - [StringBuffer、StringBuilder类](#stringbufferstringbuilder类)
    - [Date类 \& DateFormat类](#date类--dateformat类)
    - [Random、Math](#randommath)

### String类

#### 不可变性
实例一：
String是不可变的字符序列
```java
@Test
public void Test(){
    String str = "www.yorick.com";
    String newStr = str.replace('m','n');
    System.out.println(str);
    System.out.println(newStr);
}
```
实例二：
对比person对象和str，体会字符串的不可变性
```java
@Test
public void testPassRef() {
    Person person = new Person("ABC",12);
    System.out.println(person);
    changePerson(person);
    System.out.println(person);
    String str = "abcd";
    changeString(str);
    System.out.println(str);
}
public void changePerson(Person person) {
    person.setName("Yorick");
}
public void changeString(String str) {
    str.replace('a', 'b');
}
/*out：
Person{name='ABC', age=12}
Person{name='Yorick', age=12}
abcd
*/
```
#### 字符串缓冲池
关于字符串缓冲池:直接通过`=`为字符串赋值，会先在缓冲池中查找有没有一样的字符串，
如果有就把那个引用赋给字符串变量，否则，会创建一个新的字符串，并把对应的字符串放入到缓冲池中。
```java
@Test
public void testNewString() {
    
    String str1 = "Hello Yorick";
    String str2 = "Hello Yorick";
    System.out.println(str1 == str2);//true
    System.out.println(str1.hashCode());//-911844285
    System.out.println(str2.hashCode());//-911844285

    String str3 = new String("abcde");
    String str4 = new String("abcde");
    System.out.println(str3 == str4);//false
}
```
#### 字符串常用方法
1. trim():去除前后空格
```java
@Test
public void testTrim() {
    String str = "   Yorick   ";
    System.out.println("--" + str + "--");
    System.out.println("--" + str.trim() + "--");
    //--Yorick--
}
```
2. 求子字符串的方法:
subString(fromIndex)：从fromIndex开始，包含fromIndex，且 String的字索引从0开始
subString(fromIndex, toIndex)：[fromIndex,toIndex)
```java
@Test
public void testSubString() {
    String str = "https://www.yorick.com/index.jsp?name=Yorick";
    String str1 = str.substring(8);
    System.out.println(str1);//www.yorick.com/index.jsp?name=Yorick
    String str2 = str.substring(12, 18);
    System.out.println(str2);//yorick
}
```
3. indexOf:求指定字符的索引
```java
@Test
public void testIndexOf() {
    String str = "https://www.yorick.com/index.jsp?name=Yorick";
    int beginIndex = str.indexOf('/');
    int endIndex = str.lastIndexOf('/');
    System.out.println(beginIndex);//6
    System.out.println(endIndex);//22
    System.out.println(str.substring(beginIndex + 2, endIndex));
    //www.yorick.com
}
```
4. split(String regex):把字符串拆分成字符串数组
```java
@Test
public void testSplit() {
    String str = "a-b-c-d-e-f-g";
    String[] values = str.split("-");
    for (String s : values) {
        System.out.print(s);//abcdefg
    }
}
```
5. equals():比较字符串内容是否相等必须使用该方法,而不能直接使用"=="
6. charAt():用于返回指定索引处的字符。索引范围为从 0 到 length() - 1
7. 练习：
给定一个字符串,如：acmfnz
经过运算求每个字符都向后串一位的字符串：bdngoa
若某个字符已经是z，则返回到最开始的a

```java
@Test
public void testTransforString() {
    String str = "acmfnz123uidqweidg''dasd2qedq>e23,";
    System.out.println(str);
    for (int i = 0; i < str.length(); i++) {
        char ch = str.charAt(i);
        //System.out.print(ch);
        if (ch >= 'a' && ch <= 'z') {
            if (ch == 'z'){
                ch = 'a';
            }else {
                ch = (char) (ch + 1);
            }
        } else if (ch >= 'A' && ch <= 'Z') {
            if (ch == 'Z'){
                ch = 'A';
            }else {
                ch = (char) (ch + 1);
            }
        }
        System.out.print(ch);
    }
}
```
### StringBuffer、StringBuilder类
StringBuilder和StringBuffer非常类似，均代表可变的字符序列，而且方法也一样
String：不可变字符序列
StringBuilder：可变字符序列、效率高、线程不安全（推荐使用）
StringBuffer：可变字符序列、效率低、线程安全（多线程情况下使用）
```java
import org.junit.Test;

public class StringBufferTest {

    // append()方法：把字符串加入到字符串序列的后面
    // 注意：append() 方法的返回值还是当前的StringBuffer对象，可以使用方法的连缀。
    @Test
    public void testAppend() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("<html>")
                .append("<body>")
                .append("</body>")
                .append("</html>");

        System.out.println(stringBuilder);
    }

    @Test
    public void testStringBuilder() {
        StringBuffer stringBuffer = new StringBuffer("abcde");
        System.out.println(stringBuffer);

        stringBuffer.replace(1, 3, "mvp");
        System.out.println(stringBuffer);
    }
}
```

### Date类 & DateFormat类
Date()封装了时期和时间
DateFormat:把日期对象格式化为一个字符串或者把一个字符串转为一个 Date对象
实例：
```java
import org.junit.Test;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DateFormatTest {

    //Date()封装了时期和时间
    @Test
    public void testDate() {
        Date date = new Date();
        System.out.println(date);
    }

    //DateFormat:把日期对象格式化为一个字符串&把一个字符串转为一个 Date对象
    //1.DateFormat:是一个抽象类.抽象类获取对象的方式;
    //1)．创建其子类对象
    //2). 有的抽象类中提供了静态工厂方法来获取抽象类的实例。
    @Test
    public void testDateFormat() throws ParseException {
        DateFormat dateFormat = DateFormat.getDateTimeInstance(DateFormat.LONG, DateFormat.SHORT);

        Date date = new Date();
        String dateStr = dateFormat.format(date);
        System.out.println(dateStr);

        dateStr = "2022年5月7日 上午11:46";
        Date date1 = dateFormat.parse(dateStr);
        System.out.println(date1);
    }

    @Test
    public void testSimpleDateFormat() throws ParseException {
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");

        Date date = new Date();
        System.out.println(dateFormat.format(date));

        String dateStr = "2012-12-12 12:12:12";
        Date date1 = dateFormat.parse(dateStr);
        System.out.println(date1);
    }
}
```
### Random、Math
Random中封装了随机相关的方法:返回随机的基本数据类型的值。
Math中封装了常用的数学方法。
实例：
```java
import org.junit.Test;
//静态导入，导入指定类的静态属性和静态方法
import static java.lang.Math.*;
import java.util.Random;

public class RandomTest {

    // Random中封装了随机相关的方法:返回随机的基本数据类型的值
    @Test
    public void testRandom() {
        Random random = new Random();

        System.out.println(random.nextInt());
        System.out.println(random.nextInt(10));//10以内
    }

    // Math中封装了常用的数学方法
    @Test
    public void testMath() {
        //System.out.println(Math.sin(Math.PI/6));
        //静态导入后效果
        System.out.println(sin(PI/6));
    }
}
```

