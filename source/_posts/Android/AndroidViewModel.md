---
title: ViewModel
index_img: ./img/mvc.png
categories: 
  - Android
date: 2022-11-05 20:42:55
tags: 
  - Jetpack
  - ViewModel
  - Architecture
sticky: 
---

# ViewModel

[TOC]

## 介绍

[ViewModel  | Android Developers (google.cn)](https://developer.android.google.cn/reference/kotlin/androidx/lifecycle/ViewModel)

ViewModel is a class that is responsible for preparing and managing the data for an `Activity` or a `Fragment`. It also handles the communication of the Activity / Fragment with the rest of the application (e.g. calling the business logic classes).

![image-20221102170743112](./img/mvc.png)

ViewModel将数据从UI层抽象出来

![image-20221102190253813](./img/image-20221102190253813.png)

由ViewModel管理的数据独立于Activity的生命周期之外。

ViewModel与LiveData配合实现对数据的监听。

## 实现

1. 创建MyViewModel类，并声明需要存放的数据，由于将可变的 LiveData 暴露给外部是不安全的，因此常见的作法是将其转换为不可变的 LiveData 类型对外部进行提供；

   ```kotlin
   class MyViewModel : ViewModel() {
       private val _number = MutableLiveData<Int>()
       val number: LiveData<Int>
           get() = _number
       init {
           _number.value = 0
       }
   }
   ```

2. 在Activity实例化MyViewModel有两种方法

   - 在Activity中声明MyViewModel类，延迟加载

     ```kotlin
     private lateinit var myViewModel: MyViewModel
     ```
     在onCreate方法中实例化

     ```kotlin
     myViewModel = ViewModelProvider(this)[MyViewModel::class.java]
     ```
     
   - 懒加载，随用随加载

     ```kotlin
     private val myViewModel by lazy { ViewModelProvider(this)[MyViewModel::class.java] }
     ```

3. 若在Fragment中使用

   ```kotlin
   myViewModel = ViewModelProvider(requireActivity())[MyViewModel::class.java]
   ```

4. 使用MyViewModel中的成员变量

   ```kotlin
   textView.text = myViewModel.number.toString()
   ```

## ViewModelSavedState

![image-20221109170013398](./img/image-20221109170013398.png)

虽然`viewModel`要比`onSaveInstanceState`简单，但是`viewModel`只能在屏幕旋转和语言切换后（即配置变更时）的页面重建维持数据，当页面意外销毁时数据无法恢复（viewModel也会重建），而这点`onSaveInstanceState`可以做到。关于意外销毁，我们暂且理解成非配置变更引起的销毁重建，比如内存不足等场景。

[ViewModel 的已保存状态模块  | Android 开发者  | Android Developers (google.cn)](https://developer.android.google.cn/topic/libraries/architecture/viewmodel-savedstate?hl=zh-cn#kotlin)

### 使用SavedInstanceState保存数据

1. 在Activity重写`onSaveInstanceState()`方法，以键值对的形式保存数据

   ```kotlin
   private val key: String = "title"
   override fun onSaveInstanceState(outState: Bundle) {
       super.onSaveInstanceState(outState)
       outState.putString(key, textView.text.toString())
   }
   ```

2. 在`onCreate()`方法中获取数据

   ```kotlin
   override fun onCreate(savedInstanceState: Bundle?) {
       super.onCreate(savedInstanceState)
       setContentView(R.layout.activity_main)
       textView = findViewById(R.id.textView)
       button1 = findViewById(R.id.button)
       textView.text = savedInstanceState?.getString(key) ?: textView.text
       ...
   }
   ```

### 使用ViewModelSavedState保存数据

解决当进程被系统回收后，如何保存数据。

1. 在module的`build.gradle`引入依赖

   ```groovy
   dependencies {
       ...
       implementation 'androidx.lifecycle:lifecycle-extensions:2.2.0'
       ...
   }
   ```

2. 创建ViewModel

   ```kotlin
   package com.yorick.viewmodelsavedstate
   
   import androidx.lifecycle.MutableLiveData
   import androidx.lifecycle.SavedStateHandle
   import androidx.lifecycle.ViewModel
   
   class SavedStateViewModel(
       private var handle: SavedStateHandle
   ) : ViewModel() {
   
       private var number = MutableLiveData<Int>()
   
       init {
           number.value = 0
       }
   
       fun add() {
           getNumber().value = getNumber().value?.plus(1)
       }
   
       fun getNumber(): MutableLiveData<Int> {
           if (!handle.contains(MainActivity.KEY_NUMBER)) {
               handle.set(MainActivity.KEY_NUMBER, 0)
           }
           return handle.getLiveData(MainActivity.KEY_NUMBER)
       }
   }
   ```

3. 创建布局，包括一个`TextView`和一个`Button`

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <layout xmlns:android="http://schemas.android.com/apk/res/android"
       xmlns:app="http://schemas.android.com/apk/res-auto"
       xmlns:tools="http://schemas.android.com/tools">
   
       <data>
   
           <variable
               name="data"
               type="com.yorick.viewmodelsavedstate.SavedStateViewModel" />
       </data>
   
       <androidx.constraintlayout.widget.ConstraintLayout
           android:layout_width="match_parent"
           android:layout_height="match_parent"
           tools:context=".MainActivity">
   
           <TextView
               android:id="@+id/textView"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:text="@{data.number.toString()}"
               android:textSize="34sp"
               app:layout_constraintBottom_toBottomOf="parent"
               app:layout_constraintEnd_toEndOf="parent"
               app:layout_constraintStart_toStartOf="parent"
               app:layout_constraintTop_toTopOf="parent"
               app:layout_constraintVertical_bias="0.352" />
   
           <Button
               android:id="@+id/button"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:onClick="@{()->data.add()}"
               android:text="Button"
               app:layout_constraintBottom_toBottomOf="parent"
               app:layout_constraintEnd_toEndOf="parent"
               app:layout_constraintStart_toStartOf="parent"
               app:layout_constraintTop_toTopOf="parent"
               app:layout_constraintVertical_bias="0.653" />
       </androidx.constraintlayout.widget.ConstraintLayout>
   </layout>
   ```

4. 创建Activity

   ```kotlin
   package com.yorick.viewmodelsavedstate
   
   
   import androidx.appcompat.app.AppCompatActivity
   import android.os.Bundle
   import androidx.databinding.DataBindingUtil
   import androidx.lifecycle.SavedStateViewModelFactory
   import androidx.lifecycle.ViewModelProvider
   import com.yorick.viewmodelsavedstate.databinding.ActivityMainBinding
   
   class MainActivity : AppCompatActivity() {
   
       private val savedStateViewModel by lazy {
           ViewModelProvider(
               this,
               SavedStateViewModelFactory(application, this)
           )[SavedStateViewModel::class.java]
       }
   
       private val binding: ActivityMainBinding by lazy {
           DataBindingUtil.setContentView(this, R.layout.activity_main)
       }
   
       companion object {
           const val KEY_NUMBER = "KEY_NUMBER"
       }
   
       override fun onCreate(savedInstanceState: Bundle?) {
           super.onCreate(savedInstanceState)
           setContentView(R.layout.activity_main)
           binding.data = savedStateViewModel
           binding.lifecycleOwner = this
       }
   }
   ```

### 使用ViewModel&SharedPreference存储数据

[使用ViewModel和SharedPreference以键值对的形式存储数据](../../14_SharedPreferences.md)

