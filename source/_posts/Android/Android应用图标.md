---
title: Android应用图标
index_img: /img/default.png
categories: 
  - Android
date: 2022-12-17 10:57:37
tags: 
  - Icon
sticky: 
---

# 应用图标

[自适应图标  | Android 开发者  | Android Developers (google.cn)](https://developer.android.google.cn/guide/practices/ui_guidelines/icon_design_adaptive?hl=zh-cn)

[Vector drawables overview  | Android Developers (google.cn)](https://developer.android.google.cn/develop/ui/views/graphics/vector-drawable-resources?hl=en)

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:tint="@color/color_ic_back" // 
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#96C8FF" // 填充颜色，切换夜间模式会变成此色
        android:pathData="
        M0,0
        L108,108
        H0
        V0
        H108
        V108
" />
</vector>
```