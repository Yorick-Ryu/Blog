---
title: Kotlin数字类型
index_img: /img/default.png
categories: 
  - kotlin
date: 2022-09-08 10:16:31
tags: 
sticky: 
---

## 数字类型

- [数字类型](#数字类型)
  - [数字类型](#数字类型-1)
  - [安全转换函数](#安全转换函数)
  - [Double转Int](#double转int)
  - [Double类型格式化](#double类型格式化)

### 数字类型

和Java一样，Kotlin的数字类型都是有符号的，也就是说正负数都可以表示。

| 类型   | 位  | 最大值                 | 最小值               |
| ------ | --- | ---------------------- | -------------------- |
| Byte   | 8   | 127                    | -128                 |
| Short  | 16  | 32767                  | -32768               |
| Int    | 32  | 2147483647             | -2147483648          |
| Long   | 64  | 9223372036854775807    | -9223372036854775808 |
| Float  | 32  | 3.4028235E38           | 1.4E-45              |
| Double | 64  | 1.7976931348623157E308 | 4.9E-324             |

### 安全转换函数

Kotlin提供了`toDoubleOrNull`和`tolntOrNull`这样的安全转换函数，如果数值不能正确转换，与其触发异常不如干脆返回`null`值。

```kotlin
fun main() {
    val number: Int = "9.99".toInt()
    println(number)
}
// 抛异常
// NumberFormatException
```
使用安全转换函数
```kotlin
fun main() {
    val number: Int? = "9.99".toIntOrNull()
    println(number)
}
// 输出
// null
```

### Double转Int
```kotlin
fun main() {
    // 直接取小数点前，精度损失
    println(8.9999994522.toInt()) // 8
    // 四舍五入转换
    println(8.9999994522.roundToInt()) // 9
}
```

### Double类型格式化

```kotlin
fun main() {
    val s = "%.2f".format(8.9199994522)
    println(s) // 8.92
}
```