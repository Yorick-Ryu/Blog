---
title: LiveData
index_img: /img/android-jetpack.svg
categories: 
  - Android
date: 2022-11-05 20:42:55
tags: 
  - Jetpack
  - LiveData
  - Architecture
sticky: 
---

# LiveData

[LiveData  | Android Developers (google.cn)](https://developer.android.google.cn/reference/kotlin/androidx/lifecycle/LiveData)

[TOC]

## LiveData的定义

[`LiveData`](https://developer.android.google.cn/reference/androidx/lifecycle/LiveData) 是一种可观察的数据存储器类。与常规的可观察类不同，LiveData 具有[生命周期](https://so.csdn.net/so/search?q=生命周期&spm=1001.2101.3001.7020)感知能力，意指它遵循其他应用组件（如 Activity、Fragment 或 Service）的生命周期。这种感知能力可确保 LiveData 仅更新处于活跃生命周期状态的应用组件观察者。

从上述定义可以知道：

- LiveData 是一个`可观察`的`数据存储类`；
- LiveData 具有`生命周期感知`能力；
- LivaData `仅更新`处于`活跃生命周期状态（ STARTED 或 RESUMED 状态）`的应用组件观察者。

## LiveData的优势

- 确保界面符合数据状态；
- 不会发生内存泄漏；
- 不会因 Activity 的停止而导致崩溃
- 不需要手动处理生命周期
- 数据始终保持最新状态
- 共享资源
- 适当的配置修改

## LiveData的使用

### LiveData 基本使用

类型为 LiveData 的对象没有公开的方法给更新其 value，要想更新 LiveData 对象的 value，需要使用 类型为 MutableLiveData 的LiveData 对象，其提供了 [`setValue(T)`](https://developer.android.google.cn/reference/androidx/lifecycle/MutableLiveData#setValue(T)) 和 [`postValue(T)`](https://developer.android.google.cn/reference/androidx/lifecycle/MutableLiveData#postValue(T)) 方法，其中如果想在多线程中更新数据只能使用 `postValue(T)` 方法。

使用步骤主要分三步：

1. 创建 LiveData 对象实例（常在 ViewModel 中）；
2. 创建 Observer 对象（常在 Activity 或者 Fragment 中）；
3. 使用 observer() 方法将 Observer 对象附加到 LiveData 对象（通常在 Activity 或者 Fragment 中）。

示例：

1. 创建 LiveData 对象实例（常在 ViewModel 中），由于将可变的 LiveData 暴露给外部是不安全的，因此常见的作法是将其转换为不可变的 LiveData 类型对外部进行提供；

   ```kotlin
   class ViewModelWithLiveData : ViewModel() {
       private val _likedNumber = MutableLiveData<Int>()
       val likedNumber: LiveData<Int>
           get() = _likedNumber
   
       init {
           _likedNumber.value = 0
       }
   
       fun addLikedNumber(n: Int) {
           _likedNumber.value = _likedNumber.value?.plus(n)
       }
   }
   ```

   将用来用来界面展示的可更新的数据 LiveData 对象创建在 ViewModel 中，而不是创建在对应的 Activity 或 [Fragment](https://so.csdn.net/so/search?q=Fragment&spm=1001.2101.3001.7020) 中是为了避免是的对应的 Activity 或 Fragment 太过庞大不易后续维护，同时将其实例和 Activity 或 Fragment 分开可以使得 LiveData 对象在配置更改后继续存在。

2. 通常在 Activity  或者 Fragment 中的`onCreate()`方法中进行 Observer 对象的创建并将其附加到 LiveData 对象，这样做是为了系统不会从 Activity 或 Fragment 的 `onResume()` 方法进行冗余调用（从生命周期图中可以看出 onCreate() 的执行的次数一般是少于 onResume() 的）。

   同时其作用为当 Activity 或 Fragment 在变为活跃状态后就具有可以立即显示的数据，当应用组件处于 STARTED 状态，就会从正在观察的 LiveData 对象接收最新的数据。观察示例代码如下：

   ```kotlin
   class MainActivity : AppCompatActivity() {
       private val viewModelWithLiveData by lazy {
           ViewModelProvider(this).get(ViewModelWithLiveData::class.java)
       }
       private lateinit var textView: TextView
       private lateinit var imageButtonLike: ImageButton
       private lateinit var imageButtonDislike: ImageButton
       override fun onCreate(savedInstanceState: Bundle?) {
           super.onCreate(savedInstanceState)
           setContentView(R.layout.activity_main)
           textView = findViewById(R.id.textView)
           imageButtonLike = findViewById(R.id.imageButton)
           imageButtonDislike = findViewById(R.id.imageButton2)
   
           viewModelWithLiveData.likedNumber.observe(this) {
               textView.text = it.toString()
           }
   
           imageButtonLike.setOnClickListener {
               viewModelWithLiveData.addLikedNumber(1)
           }
           imageButtonDislike.setOnClickListener {
               viewModelWithLiveData.addLikedNumber(-1)
           }
       }
   }
   ```

### 转换 LiveData

对于转换 LiveData 来说，可以使用 Transformations 提供的 map() 与 switchMap() 方法。

- map() 方法主要应用在给你提供的信息内容较多，但是我们只需要其内容的一部分这种情况。例如有一个 User 类，其属性有姓名，年龄，性别等，但是我们只需要姓名，就可以使用 map()。

  ```kotlin
  val userLiveData: LiveData<User> = UserLiveData()
  val userName: LiveData<String> = Transformations.map(userLiveData) {
      user -> "${user.name}"
  }
  ```

- switchMap() 方法则更多的适用于 ViewModel 中的某个 LiveData 对象是调用其他的方法获取到的，此时可以使用 switchMap() 方法将其转换为一个可观察的 LiveData 对象。

  ```kotlin
  private fun getUser(id: String): LiveData<User> {
    ...
  }
  val userId: LiveData<String> = ...
  val user = Transformations.switchMap(userId) { id -> getUser(id) }
  ```