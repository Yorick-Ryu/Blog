---
title: Android相对布局（RelativeLayout）
categories:
  - Android
date: 2022-11-28 19:23:16
tags: layout
index_img: /img/default.png
---

# 相对布局(RelativeLayout)

相对布局的下级视图位置由其他视图决定。用于确定下级视图位置的参照物分两种：

- 与该视图自身平级的视图；
- 该视图的上级视图(也就是它归属的`RelativeLayout`)

如果不设定下级视图的参照物，那么下级视图默认显示在`RelativeLayout`内部的左上角。

## 相对位置取值

| 相对位置的属性取值       | 相对位置说明                     |
| ------------------------ | -------------------------------- |
| layout_toLeftOf          | 当前视图在指定视图的左边         |
| layout_toRightOf         | 当前视图在指定视图的右边         |
| layout_above             | 当前视图在指定视图的上方         |
| layout_below             | 当前视图在指定视图的下方         |
| layout_alignLeft         | 当前视图与指定视图的左侧对齐     |
| layout_alignRight        | 当前视图与指定视图的右侧对齐     |
| layout_alignTop          | 当前视图与指定视图的顶部对齐     |
| layout_alignBottom       | 当前视图与指定视图的底部对齐     |
| layout_centerlnParent    | 当前视图在上级视图中间           |
| layout_centerHorizontal  | 当前视图在上级视图的水平方向居中 |
| layout_centerVertical    | 当前视图在上级视图的垂直方向居中 |
| layout_alignParentLeft   | 当前视图与上级视图的左侧对齐     |
| layout_alignParentRight  | 当前视图与上级视图的右侧对齐     |
| layout_alignParentTop    | 当前视图与上级视图的顶部对齐     |
| layout_alignParentBottom | 当前视图与上级视图的底部对齐     |

