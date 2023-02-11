---
title: DataBinding
index_img: ./img/image-20221105181749287.png
categories: 
  - Android
date: 2022-11-05 20:42:55
tags: 
  - Jetpack
  - DataBinding
  - Architecture
  - ViewModel
sticky: 
---

# DataBinding

![image-20221105181749287](./img/image-20221105181749287.png)

DataBinding是Google提供给我们的数据绑定的支持库，实现在页面组件中直接绑定应用程序的数据源。

## 使用DataBinding

示例App要实现的功能是，点击按钮Button，TextView的数字`+1`

1. 项目中引入dataBinding

   ```groovy
   // 在build.gradle文件添加
   android{
      ...
      dataBinding{
         enabled true
      }
      ...
   }
   ```

2. 新建activity和对应的layout布局文件。包括一个Button和一个Text View。

   ```xml
   <androidx.constraintlayout.widget.ConstraintLayout
       android:layout_width="match_parent"
       android:layout_height="match_parent"
       tools:context=".MainActivity">
   
       <TextView
           android:id="@+id/textView"
           android:layout_width="wrap_content"
           android:layout_height="wrap_content"
           android:text="Hello World"
           android:textSize="34sp"
           app:layout_constraintBottom_toBottomOf="parent"
           app:layout_constraintEnd_toEndOf="parent"
           app:layout_constraintStart_toStartOf="parent"
           app:layout_constraintTop_toTopOf="parent"
           app:layout_constraintVertical_bias="0.422" />
   
       <Button
           android:id="@+id/button"
           android:layout_width="wrap_content"
           android:layout_height="wrap_content"
           android:text="@string/button"
           app:layout_constraintBottom_toBottomOf="parent"
           app:layout_constraintEnd_toEndOf="parent"
           app:layout_constraintStart_toStartOf="parent"
           app:layout_constraintTop_toTopOf="parent"
           app:layout_constraintVertical_bias="0.71" />
   
   </androidx.constraintlayout.widget.ConstraintLayout>
   ```

3. 布局文件格式转换（普通layout➡️databing对应的layout）
   光标在布局文件的根布局➡️按`Alt` +` Enter`➡️点击 `Convert to data binding layout`

   得到转换后的layout布局文件，内容如下：

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <layout xmlns:android="http://schemas.android.com/apk/res/android"
       xmlns:app="http://schemas.android.com/apk/res-auto"
       xmlns:tools="http://schemas.android.com/tools">
   
       <data>
       </data>
   
       <androidx.constraintlayout.widget.ConstraintLayout
           android:layout_width="match_parent"
           android:layout_height="match_parent"
           tools:context=".MainActivity">
   
           <TextView
               android:id="@+id/textView"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:text="Hello World"
               android:textSize="34sp"
               app:layout_constraintBottom_toBottomOf="parent"
               app:layout_constraintEnd_toEndOf="parent"
               app:layout_constraintStart_toStartOf="parent"
               app:layout_constraintTop_toTopOf="parent"
               app:layout_constraintVertical_bias="0.422" />
   
           <Button
               android:id="@+id/button"
               android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:text="@string/button"
               app:layout_constraintBottom_toBottomOf="parent"
               app:layout_constraintEnd_toEndOf="parent"
               app:layout_constraintStart_toStartOf="parent"
               app:layout_constraintTop_toTopOf="parent"
               app:layout_constraintVertical_bias="0.71" />
   
       </androidx.constraintlayout.widget.ConstraintLayout>
   </layout>
   ```
   观察到外层嵌套了layout标签，里面增加了data标签。

4. 创建MyViewModel类

   ```kotlin
   class MyViewModel : ViewModel() {
       private val _number = MutableLiveData<Int>()
       val number: LiveData<Int>
           get() = _number
   
       init {
           _number.value = 0
       }
   
       fun add() {
           _number.value = _number.value?.plus(1)
       }
   }
   ```

5. 这里有两种方式实现`+1`功能

   - **方式一：**

     `DataBinding`会基于`layout`创建一个`Binding class`，这个类包含了布局属性(定义的变量)到相关视图的所有绑定，并且会为布局中的数据元素生成`setter`，生成的类的名称是基于`layout`的名称(驼峰命名，加上`Binding`后缀)。比如布局名是`activity_main.xml`，生成的类就是`ActivityMainBinding`。你能通过这个类去`inflate`布局和数据模型，也可以通过`DataBindingUtil`类。

     - 在`MainActivity`使用`DataBindingUtils`加载布局，这里使用了懒加载，即随用随加载。

       ```kotlin
       private val binding: ActivityMainBinding by lazy {
           DataBindingUtil.setContentView(
               this,
               R.layout.activity_main
           )
       }
       ```
     
     - `inflate`加载布局（此方法也能用于`RecyclerView`, `ViewPager`）
     
       ```kotlin
       class MainActivity : AppCompatActivity() {
           private val myViewModel by lazy { ViewModelProvider(this)[MyViewModel::class.java] }
           private val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
       
           override fun onCreate(savedInstanceState: Bundle?) {
               super.onCreate(savedInstanceState)
               setContentView(binding.root)
               ...
           }
       }
       ```
     
     上述两种方法大家二选一，一般在`Activity`中我们都用第一种。
     
     如果在fragment中绑定布局
     
     ```kotlin
     class MasterFragment : Fragment() {
     
         override fun onCreateView(
             inflater: LayoutInflater, container: ViewGroup?,
             savedInstanceState: Bundle?
         ): View {
             val viewModel = ViewModelProvider(requireActivity())[MyViewModel::class.java]
             val binding = DataBindingUtil.inflate<FragmentMasterBinding>(
                 inflater,
                 R.layout.fragment_master,
                 container,
                 false
             )
             binding.data = viewModel
             binding.lifecycleOwner = requireActivity()
             return binding.root
     }
     ```
     
     然后在`MainActivity`的`onCreate`方法添加Observe和按钮点击事件
     
     ```kotlin
     myViewModel.number.observe(this) {
     	binding.textView.text = it.toString()
     }
     binding.button.setOnClickListener {
     	myViewModel.add()
     }
     
   - **方式二：**
   
     反向绑定，把数据数据绑定和按钮点击事件放在布局文件中
   
     在layout的data中添加：
   
     ```xml
     <data>
         <variable
         	name="data"
         	type="com.yorick.databinding.MyViewModel" />
     </data>
     ```
   
     修改TextView的text属性：
   
     ```xml
     android:text="@{data.number.toString()}"
     ```
     Button增加onClick属性：
     
     ```xml
     android:onClick="@{()->data.add()}"
     ```
     Activity仅保留以下代码：
     ```kotlin
     class MainActivity : AppCompatActivity() {
         private val myViewModel by lazy { ViewModelProvider(this)[MyViewModel::class.java] }
         private val binding: ActivityMainBinding by lazy {
             DataBindingUtil.setContentView(
                 this,
                 R.layout.activity_main
             )
         }
         override fun onCreate(savedInstanceState: Bundle?) {
             super.onCreate(savedInstanceState)
             binding.data = myViewModel
             binding.lifecycleOwner = this
         }
     }
     ```

参考：

- [(在Android中使用DataBinding(Kotlin)_CSDN](https://blog.csdn.net/hncdcsm1/article/details/109505160)
- [Jetpeck DataBinding实践——轻松上手DataBinding_51CTO](https://blog.51cto.com/baorant24/5768873)
