---
title: Android_SeekBar
tags:
  - view
  - 控件
  - kotlin
index_img: /img/image-20221129173639697.png
categories:
  - Android
date: 2022-11-29 18:58:11
sticky:
---

# SeekBar

[TOC]

**参考：**

- [SeekBar  | Android Developers (google.cn)](https://developer.android.google.cn/reference/kotlin/android/widget/SeekBar?hl=en)
- [Kotlin 中的 SeekBar | 码农参考 (verytoolz.com)](https://verytoolz.com/blog/cf7594a53a/#:~:text=SeekBar)

## Seekbar介绍

Android seekBar 是progressBar 的修改版本，具有可拖动的拇指，用户可以在其中来回拖动拇指以设置当前进度值。我们可以在我们的安卓设备中使用控制栏，比如亮度控制、音量控制等。

它是重要的用户界面元素之一，它提供了在定义的范围内选择整数值的功能，例如 1 到 100。

通过在 SeekBar 中拖动拇指，我们可以来回滑动，在使用 `android:min` 和 `android:max` 属性定义的最小和最大整数值之间选择一个值。

使用`android:progress`定义初始值。

在控件列表中有两种SeekBar可供选择，一种是连续的，一种是离散的。

![image-20221129173639697](./img/image-20221129173639697.png)

## 使用SeekBar

以两个SeekBar数据同步为例。

1. 创建项目，打开`activity_main.xml`的Design界面，

2. 在Widgets列表中有两种SeekBar可供选择，一种是连续的，一种是离散的。根据需要选择不同的类型。这里我们都选上并约束布局。

   ![image-20221129173639697](./img/image-20221129173639697.png)

   - SeekBar连续

     ```xml
     <SeekBar
         android:id="@+id/seekBar2"
         android:layout_width="300dp"
         android:layout_height="40dp"
         android:max="100"
         android:progress="40"
         app:layout_constraintBottom_toBottomOf="parent"
         app:layout_constraintEnd_toEndOf="parent"
         app:layout_constraintHorizontal_bias="0.5"
         app:layout_constraintStart_toStartOf="parent"
         app:layout_constraintTop_toTopOf="parent"
         app:layout_constraintVertical_bias="0.8" />
     ```

   - SeekBar离散

     ```xml
     <SeekBar
         android:id="@+id/seekBar"
         style="@style/Widget.AppCompat.SeekBar.Discrete"
         android:layout_width="300dp"
         android:layout_height="40dp"
         android:max="10"
         android:progress="4"
         app:layout_constraintBottom_toBottomOf="parent"
         app:layout_constraintEnd_toEndOf="parent"
         app:layout_constraintStart_toStartOf="parent"
         app:layout_constraintTop_toTopOf="parent"
         app:layout_constraintVertical_bias="0.9" />
     ```

3. 在对应的Activity或者Fragment中绑定控件

   ```kotlin
   class MainActivity : AppCompatActivity() {
       lateinit var seekBar: SeekBar
       lateinit var seekBar2: SeekBar
       override fun onCreate(savedInstanceState: Bundle?) {
           super.onCreate(savedInstanceState)
           setContentView(R.layout.activity_main)
           seekBar = findViewById(R.id.seekBar)
           seekBar2 = findViewById(R.id.seekBar2)
       }
   }
   ```

4. 让两个控件的进度一致，在`onCreate`加入以下代码


   {% note warning %}
   注意默认的TODO要删掉
   {% endnote %}

   ```kotlin
   seekBar.progress = seekBar2.progress / 10
   
   seekBar.setOnSeekBarChangeListener(object : OnSeekBarChangeListener {
       override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
           seekBar2.progress = progress * 10 // 进度改变时触发
       }
       override fun onStartTrackingTouch(seekBar: SeekBar?) {
           // 开始拖动时触发
       }
       override fun onStopTrackingTouch(seekBar: SeekBar?) {
           // 结束拖动时触发
       }
   })
   
   seekBar2.setOnSeekBarChangeListener(object : OnSeekBarChangeListener {
       override fun onProgressChanged(seekBar1: SeekBar?, progress: Int, fromUser: Boolean) {
           seekBar.progress = progress / 10
       }
       override fun onStartTrackingTouch(seekBar: SeekBar?) {
       }
       override fun onStopTrackingTouch(seekBar: SeekBar?) {
       }
   })
   ```

5. `build`并运行，发现实现了两个SeekBar数据同步的效果。


