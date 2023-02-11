---
title: Android视图（View）
date: 2022-11-28 19:16:09
tags: view
categories:
- Android
index_img: /img/default.png
---

# 视图（View）

- [视图（View）](#视图view)
  - [设置视图的宽高](#设置视图的宽高)
    - [在xml代码中设置视图宽高](#在xml代码中设置视图宽高)
    - [在java代码中设置视图宽高](#在java代码中设置视图宽高)
    - [dp 转 px 工具类](#dp-转-px-工具类)
  - [设置视图的间距](#设置视图的间距)
  - [设置视图的对齐方式](#设置视图的对齐方式)

## 设置视图的宽高

设置视图的宽高有两种途径：

### 在xml代码中设置视图宽高

视图宽度通过属性`android:layout_width`表达，视图高度通过属性`android:layout_height`表达，宽高的取值主要有下列三种：
- match_parent：表示与上级视图保持一致。
- wrap_content：表示与内容自适应。
- 以dp为单位的具体尺寸。


### 在java代码中设置视图宽高

首先确保XML中的宽高属性值为`wrap_content`，接着打开该页面对应的Java代码，依序执行以下三个步骤：
- 调用控件对象的`getLayoutParams`方法，获取该控件的布局参数。
- 布局参数的`width`属性表示宽度，`height`属性表示高度，修改这两个属性值。
- 调用控件对象的`setLayoutParams`方法，填入修改后的布局参数使之生效。


```java
// 获取布局参数（含宽度和高度)
ViewGroup.LayoutParams params = tv.getLayoutParams();
// 修改布局参数中的宽度数值，注意默认px单位，所以要一个工具类将 dp 转换为 px
params.width = Utils.dip2px(this, 300);
// 设置布局参数（
tv.setLayoutParams(params);
```

### dp 转 px 工具类

```java
public class Utils {
    // 根据手机的分辨率从 dp 的单位转成为 px（像素）
    public static int dip2px(Context context, float dpValue) {
        // 获取当前手机的像素密度(1个dp对应几个px)
        float scale = context.getResources().getDisplayMetrics().density;
        // 四舍五入取整
        return (int) (dpValue * scale + 0.5f);
    }
}
```
context（上下文） 的妙用！

## 设置视图的间距

设置视图的间距有两种途径：

- 采用`layout_margin`属性，它指定了当前视图与周围平级视图之间的距离（外边距）。包括`layout_margin`、`layout_marginLeft`、`layout_marginTop`、`layout_marginRight`、`layout_marginBottom`
  
- 采用`padding`属性，它指定了当前视图与内部下级视图之间的距离（内边距）。包括`padding`、`paddingLeft`、`paddingTop`、`paddingRight`、`paddingBottom`

`margin`和`padding`属性适用于所有视图，附视图家族的依赖继承关系：

![视图家族的依赖继承关系](./img/view_relationship.png)

## 设置视图的对齐方式

设置视图的对齐方式有两种途径：

- 采用`layout_gravity`属性，它指定了当前视图相对于上级视图的对齐方式。
- 采用`gravity`属性，它指定了下级视图相对于当前视图的对齐方式。
`layout_gravity`与`gravity`的取值包括: `left`、`top`、`right`、`bottom`，还可以用竖线连接各取值，例如`left|top`表示即靠左又靠上，也就是朝左上角对齐。

[Android 中 marginLeft 和 marginStart 的区别](https://www.jianshu.com/p/d597d96d5167)

[goole官方解释](https://developer.android.com/about/versions/android-4.2.html#RTL)

