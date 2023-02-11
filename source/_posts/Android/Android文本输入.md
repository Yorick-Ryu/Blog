---
title: Android文本输入
tags:
  - view
  - 控件
  - textview
index_img: /img/default.png
categories:
  - Android
date: 2022-11-29 18:54:43
sticky:
---

# 文本输入

- [文本输入](#文本输入)
  - [编辑框EditText](#编辑框edittext)
  - [焦点变更监听器](#焦点变更监听器)
  - [文本变化监听器](#文本变化监听器)
  - [TextInputEditText](#textinputedittext)

## 编辑框EditText

编辑框EditText用于接收软键盘输入的文字，例如用户名、密码、评价内容等，它由文本视图派生而来，除了TextView已有的各种属性和方法，EditText还支持下列XML属性。

- inputType:指定输入的文本类型。输入类型的取值说明见表，若同时使用多种文本类型，则可使用竖线"|"把多种文本类型拼接起来。
- maxLength:指定文本允许输入的最大长度。
- hint:指定提示文本的内容。
- textColorHint:指定提示文本的颜色。

| 输入类型       | 说明                                                       |
| -------------- | ---------------------------------------------------------- |
| text           | 文本                                                       |
| textPassword   | 文本密码。显示时用圆点"·"代替                              |
| number         | 整型数                                                     |
| numberSigned   | 带符号的数字。允许在开头带负号"- "                         |
| numberDecimal  | 带小数点的数字                                             |
| numberPassword | 数字密码。显示时用圆点"·"代替                              |
| datetime       | 时间日期格式。除了数字外，还允许输入横线、斜杆、空格、冒号 |
| date           | 日期格式。除了数字外，还允许输入横线"-"和斜杆"/"           |
| time           | 时间格式。除了数字外，还允许输入冒号":"                    |

## 焦点变更监听器

编辑框点击两次后才会触发点击事件，因为第一次点击只触发焦点变更事件，第二次点击才触发点击事件。

若要判断是否切换编辑框输入，应当监听焦点变更事件，而非监听点击事件。

调用编辑框对象的setOnFocusChangeListener方法，即可在光标切换之时（获得光标和失去光标）触发焦点变更事件。

应用：用于限制文本长度

## 文本变化监听器

调用编辑框对象的addTextChangedListener方法即可注册文本监听器。

文本监听器的接口名称为TextWatcher，该接口提供了3个监控方法，具体说明如下。

- beforeTextChanged：在文本改变之前触发。
- onTextChanged：在文本改变过程中触发。 
- afterTextChanged：在文本改变之后触发。

应用：监听文本位数自动关闭软键盘

## TextInputEditText

TextInputEditText是遵循Material Design设计的文本输入框。

```xml
<com.google.android.material.textfield.TextInputLayout
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    app:endIconDrawable="@drawable/ic_baseline_clear_24" 这里可以修改end图标的样式
    app:endIconMode="clear_text" 这里可以修改end图标的模式
    app:layout_constraintBottom_toBottomOf="parent"
    app:layout_constraintEnd_toEndOf="parent"
    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintTop_toTopOf="@+id/guideline2">

    <com.google.android.material.textfield.TextInputEditText
        android:layout_width="match_parent"
        android:layout_height="56dp"
        android:hint="Text" />
</com.google.android.material.textfield.TextInputLayout>
```