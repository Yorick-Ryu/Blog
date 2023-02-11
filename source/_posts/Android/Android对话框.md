---
title: Android对话框
tags:
  - dialog
index_img: /img/default.png
categories:
  - Android
date: 2022-11-29 19:02:56
sticky:
---

# 对话框

- [对话框](#对话框)
  - [提醒对话框AlertDialog](#提醒对话框alertdialog)
  - [日期对话框DatePickerDialog](#日期对话框datepickerdialog)
  - [时间对话框TimePickerDialog](#时间对话框timepickerdialog)


## 提醒对话框AlertDialog


AlertDialog名为提醒对话框，它是Android中最常用的对话框，可以完成常见的交互操作，例如提示、确认、选择等功能。由于
AlertDialog没有公开的构造方法，因此必须借助建造器`AlertDialog.Builder`才能完成参数设置，`AlertDialog.Builder`的常用方法说明如下。

- setIcon：设置对话框的标题图标。
- setTitle：设置对话框的标题文本。
- setMessage：设置对话框的内容文本。
- setPositiveButton：设置肯定按钮的信息，包括按钮文本和点击监听器。
- setNegativeButton：设置否定按钮的信息，包括按钮文本和点击监听器。
- setNeutralButton：设置中性按钮的信息，包括按钮文本和点击监听器，该方法比较少用。

通过`AlertDialog.Builder`设置完对话框参数，还需调用建造器的create方法才能生成对话框实例。最后调用对话框实例的show方法，在页面上弹出提醒对话框。

使用MD3风格的对话框

```kotlin
MaterialAlertDialogBuilder(context)
        .setTitle(resources.getString(R.string.title))
        .setMessage(resources.getString(R.string.supporting_text))
        .setNeutralButton(resources.getString(R.string.cancel)) { dialog, which ->
            // Respond to neutral button press
        }
        .setNegativeButton(resources.getString(R.string.decline)) { dialog, which ->
            // Respond to negative button press
        }
        .setPositiveButton(resources.getString(R.string.accept)) { dialog, which ->
            // Respond to positive button press
        }
        .show()
```

[material-components-android/Dialog.md at master · material-components/material-components-android (github.com)](https://github.com/material-components/material-components-android/blob/master/docs/components/Dialog.md)


## 日期对话框DatePickerDialog

虽然EditText提供了`inputType="date"`的日期输入，但是很少有人会手工输入完整日期，况且EditText还不支持"年 ** 月 ** 日"这样的中文日期，所以系统提供了专门的日期选择器DatePicker，供用户选择具体的年月日。不过，DatePicker并非弹窗模式而是在当前页面占据一块区域，并且不会自动关闭。按习惯来说，日期控件应该弹出对话框，选择完日期就要自动关闭对话框。因此，很少直接在界面上显示DatePicker，而是利用已经封装好的日期选择对话框DatePickerDialog。

DatePickerDialog相当于在AlertDialog上装载了DatePicker，编码时只需调用构造方法设置当前的年、月、日，然后调用show方法即可弹出日期对话框。日期选择事件则由监听器OnDateSetListener负责响应，在该监听器的onDateSet方法中，开发者获取用户选择的具体日期，再做后续处理。特别注意onDateSet的月份参数，它的起始值不是1而是0。也就是说，一月份对应的参数值为0，十二月份对应的参数值为11，中间月份的数值以此类推。


示例：

日期选择器DatePicker

新建控件

```xml
<DatePicker
    android:id="@+id/dp_date"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:calendarViewShown="false"
    android:datePickerMode="spinner" />
```

`android:datePickerMode`属性可以选择模式。

新建按钮点击事件为：

```java
String desc = String.format("您选择的日期是%d年%d月%d日", dpDate.getYear(), dpDate.getMonth() + 1, dpDate.getDayOfMonth());
tvDate.setText(desc);
```

日期对话框DatePickerDialog

```java
Calendar calendar = Calendar.getInstance();
DatePickerDialog dialog = new DatePickerDialog(this, this, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH));
dialog.show();
```

## 时间对话框TimePickerDialog

时间选择器TimePicker可以让用户选择具体的小时和分钟。

TimePickerDialog 的用法类似 DatePickerDialog。
