---
title: Android图像视图（ImageView）
index_img: /img/default.png
categories:
  - Android
date: 2022-11-29 18:14:23
tags: 
  - view
sticky:
---

# 图像视图(ImageView)

- [图像视图(ImageView)](#图像视图imageview)
  - [图像视图的缩放类型](#图像视图的缩放类型)
- [图像按钮(lmageButton)](#图像按钮lmagebutton)
  - [ImageButton的使用场合](#imagebutton的使用场合)
- [同时展示文本与图像](#同时展示文本与图像)

图像视图展示的图片通常位于`res/drawable***`目录，设置图像视图的显示图片有两种方式：

- 在XML文件中，通过属性`android:src`设置图片资源，属性值格式形如`@drawable/apple`。（apple为不含扩展名的图片名称）
- 在Java代码中，调用`setlmageResource`方法设置图片资源，方法参数格式形如`R.drawable.apple`。

## 图像视图的缩放类型

lmageView本身默认图片居中显示（`fitCenter`），若要改变图片的显示方式，可通过`scaleType`属性设定，该属性的取值说明如下：

| XML中的缩放类型 | ScaleType类中的缩放类型 | 说明                                                 |
| --------------- | ----------------------- | ---------------------------------------------------- |
| fitXY           | FIT_XY                  | 拉伸图片使其正好填满视图（图片可能被拉伸变形)        |
| fitStart        | FIT_START               | 保持宽高比例，拉伸图片使其位于视图上方或左侧         |
| fitCenter       | FIT_CENTER              | 保持宽高比例，拉伸图片使其位于视图中间               |
| fitEnd          | FIT_END                 | 保持宽高比例，拉伸图片使其位于视图下方或右侧         |
| center          | CENTER                  | 保持图片原尺寸，并使其位于视图中间                   |
| centerCrop      | CENTER_CROP             | 拉伸图片使其充满视图，并位于视图中间                 |
| centerlnside    | CENTER_INSIDE           | 保持宽高比例，缩小图片使之位于视图中间(只缩小不放大) |

java代码中设置图片缩放属性：
`iv_scale.setScaleType(ImageView.ScaleType.CENTER);`

很多情况下，可以注意到`centernside`和`center`的显示效果居然一模一样，这缘于它们的缩放规则设定。表面上`fitCenter`、`centerinside`、`center`三个类型都是居中显示，且均不越过图像视图的边界。它们之间的区别在于：`fitCenter`既允许缩小图片、也允许放大图片，`centerInside`只允许缩小图片、不允许放大图标，而center自始至终保持原始尺寸(既不允许缩小图片、也不允许放大图片)。因此，当图片尺寸大于视图宽高，`centerInside`与`fitCenter`都会缩小图片，此时它俩的显示效果相同；当图片尺寸小于视图宽高，`centernside`与`center`都保持图片大小不变，此时它俩的显示效果相同。

# 图像按钮(lmageButton)

`lmageButton`是显示图片的图像按钮，但它继承自`lmageView`，而非继承`Button`。
`lmageButton`和`Button`之间的区别有：

- `Button`既可显示文本也可显示图片，`lmageButton`只能显示图片不能显示文本。
- `lmageButton`上的图像可按比例缩放，而`Button`通过背景设置的图像会拉伸变形。
- `Button`只能靠背景显示一张图片，而`lmageButton`可分别在前景和背景显示图片，从而实现两张图片叠加的效果。

## ImageButton的使用场合

在某些场合，有的字符无法由输入法打出来，或者某些文字以特殊字体展示，就适合先切图再放到`ImageButton`。例如：开平方符号$\sqrt{n}$，等等。

`lmageButton`与`lmageView`之间的区别有：

- `lmageButton`有默认的按钮背景，`ImageView`默认无背景。
- `lmageButton`默认的缩放类型为`center`，而`ImageView`默认的缩放类型为`fitCenter`。

# 同时展示文本与图像

同时展示文本与图像的可能途径包括：

(1）利用`LinearLayout`对`ImageView`和`TextView`组合布局。
(2）通过按钮控件`Button`的`drawable***`属性设置文本周围的图标。

`drawableTop`:指定文字上方的图片。
`drawableBottom`:指定文字下方的图片。
`drawableLeft`:指定文字左边的图片。
`drawableRight`:指定文字右边的图片。
`drawablePadding`:指定图片与文字的间距。

[修改背景不起作用](https://www.bilibili.com/video/BV19U4y1R7zV?p=33&t=170.1)