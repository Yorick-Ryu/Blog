---
title: Android线性布局（LinearLayout）
categories:
  - Android
date: 2022-11-28 19:18:47
tags: layout
index_img: /img/default.png
---

# 线性布局(LinearLayout)

## 线性布局的排列方式

线性布局内部的各视图有两种排列方式:

- `orientation`属性值为`horizontal`时，内部视图在水平方向从左往右排列。
- `orientation`属性值为`vertical`时，内部视图在垂直方向从上往下排列。
- 如果不指定`orientation`属性，则`LinearLayout`默认水平方向排列。

## 线性布局的权重

线性布局的权重概念，指的是线性布局的下级视图各自拥有多大比例的宽高。

权重属性名叫`layout_weight`，但该属性不在`LinearLayout`节点设置，而在线性布局的直接下级视图设置，表示该下级视图占据的宽高比例。
- `layout_width`填`0dp`时，`layout_weight`表示水平方向的宽度比例。
- `layout_height`填`0dp`时，`layout_weight`表示垂直方向的高度比例。
