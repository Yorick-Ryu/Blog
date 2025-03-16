---
title: 安卓面试经验 - 现代Android开发技术篇
tags:
  - interview
  - modern
  - kotlin
  - compose
index_img: /img/android-bot.png
categories:
  - Android
date: 2025-03-09 19:13:06
---

## 第六部分：现代Android开发技术篇

### 33、Jetpack Compose
- **什么是Jetpack Compose？它与传统View系统有什么区别？** ⭐⭐⭐⭐⭐

  Jetpack Compose是Android的现代声明式UI工具包，基于Kotlin构建。

  与传统View系统的主要区别：
  1. **声明式vs命令式**：Compose使用声明式编程模型，开发者描述UI应该是什么样子，而不是如何创建/更新UI
  2. **无XML**：Compose完全使用Kotlin代码定义UI，无需XML布局文件
  3. **更少的模板代码**：不需要findViewById、ViewHolder等模板代码
  4. **状态驱动**：UI自动响应状态变化，不需要手动更新视图
  5. **一致性动画**：内置动画系统，更容易实现复杂动画
  6. **无需Fragment**：可以直接在Composable函数间导航，简化架构
  7. **更好的性能**：智能重组系统只更新需要变化的部分

- **Compose中的重组(Recomposition)是什么？什么时候会触发重组？** ⭐⭐⭐⭐

  重组是Compose更新UI的过程，当组件依赖的数据发生变化时，Compose会重新执行相关的Composable函数来更新UI。

  触发重组的情况：
  1. **状态变化**：使用mutableStateOf、remember等创建的状态对象值改变时
  2. **参数变化**：传递给Composable函数的参数发生变化时
  3. **组合参数变化**：CompositionLocal值在当前作用域变化时
  4. **配置变化**：如设备旋转、暗黑模式切换等
  5. **手动调用**：通过recomposer手动触发重组

  重组是智能的，只会重组受影响的部分，而不是整个UI树。

- **如何在Compose中管理状态？State、MutableState、remember和rememberSaveable的区别？** ⭐⭐⭐⭐⭐

  **State与MutableState**：
  - `State<T>`：只读状态接口，提供value属性读取值
  - `MutableState<T>`：可变状态接口，继承State，额外提供修改value的能力
  - 当State/MutableState值变化时自动触发重组

  **remember**：
  - 在组件初始创建时计算一个值并在重组过程中保留该值
  - 基本用法：`val count = remember { mutableStateOf(0) }`
  - 仅在组件在组合中存在期间保留值，组件被移除后值会丢失
  - 配置变化（如旋转屏幕）时值也会丢失

  **rememberSaveable**：

  - 类似remember，但在配置变化（如屏幕旋转）和进程重建时保留状态
  - 基本用法：`val count = rememberSaveable { mutableStateOf(0) }`
  - 可通过Saver、Parcelize、mapSaver等方式存储复杂对象

  **选择指南**：
  - 临时UI状态（如动画状态）：使用remember
  - 需要持久化的用户数据：使用rememberSaveable
  - 需要在多个组件间共享的状态：使用ViewModel结合collect

- **Compose中的副作用(Side-Effects)有哪些？各自应用场景是什么？** ⭐⭐⭐⭐

  Compose中的主要副作用API：

  1. **LaunchedEffect**：
     - 启动协程作用域，当键发生变化时重新启动
     - 适用于：异步操作、一次性事件、动画
     - 例：`LaunchedEffect(key) { /* 协程代码 */ }`

  2. **DisposableEffect**：
     - 需要清理资源的副作用，如注册/注销监听器
     - 在离开组合或键变化时调用onDispose清理
     - 例：`DisposableEffect(key) { onDispose { /* 清理 */ } }`

  3. **SideEffect**：
     - 每次重组成功后运行，用于与非Compose代码同步状态
     - 例：`SideEffect { /* 同步到非Compose系统 */ }`

  4. **produceState**：
     - 将非Compose状态转换为Compose状态
     - 返回可在组合中读取的State对象
     - 例：`val state = produceState(initial) { /* 更新value */ }`

  5. **derivedStateOf**：
     - 基于其他状态计算派生状态，避免不必要的重组
     - 例：`val filtered = remember { derivedStateOf { list.filter(predicate) } }`

  6. **rememberCoroutineScope**：
     - 创建绑定到组合点的协程作用域，可在事件处理程序中使用
     - 例：`val scope = rememberCoroutineScope()`

  7. **rememberUpdatedState**：
     - 在长寿命效应中引用最新值
     - 例：`val latest = rememberUpdatedState(value)`

  8. **snapshotFlow**:
     - 将Compose状态转换为Flow
     - 例：`snapshotFlow { state.value }`

- **如何在Compose UI中集成传统View？反过来呢？** ⭐⭐⭐

  **在Compose中集成传统View**：

  - 使用`AndroidView`组件包装传统View
  ```kotlin
  AndroidView(
      factory = { context ->
          TextView(context).apply {
              text = "这是一个传统View"
          }
      },
      update = { textView ->
          textView.text = "更新的文本"
      }
  )
  ```
  - 可以通过update参数响应Compose状态变化
  - 复杂View如RecyclerView也可以包装集成

  **在传统View中集成Compose**：
  - 使用`ComposeView`类
  ```kotlin
  // 在Activity/Fragment中
  val composeView = ComposeView(context)
  composeView.setContent {
      MaterialTheme {
          MyComposable()
      }
  }
  layout.addView(composeView)
  ```
  - 在XML中使用`androidx.compose.ui.platform.ComposeView`
  ```xml
  <androidx.compose.ui.platform.ComposeView
      android:id="@+id/compose_view"
      android:layout_width="match_parent"
      android:layout_height="wrap_content" />
  ```
  ```kotlin
  findViewById<ComposeView>(R.id.compose_view).setContent {
      MyComposable()
  }
  ```

- **Compose的性能优化策略有哪些？** ⭐⭐⭐⭐

  1. **状态提升**：
     - 将状态提升到只需要它的最低公共祖先
     - 避免不必要的重组传播

  2. **稳定类型和不可变数据**：
     
     - 使用稳定类型(`@Stable`标记的类)和不可变对象
     - 使Compose更好地跟踪状态变化
     
  3. **使用key**：
     
     - 在列表项和动态内容中使用唯一且稳定的key
     - 帮助Compose正确跟踪项目身份
     
  4. **使用derivedStateOf**：
     
     - 避免中间状态变化触发重组
     - 仅在最终结果变化时重组
     
  5. **延迟布局计算**：
     - 使用`LazyColumn`而不是`Column`处理长列表
     - 使用`remember { derivedStateOf }`计算派生数据

  6. **避免不必要的重组**：
     - 分解大型Composable函数为更小的函数
     - 使用remember包装不依赖于状态的计算

  7. **Remember + lambda缓存**：
     
     - 缓存传递给子组件的lambda以避免重组
     ```kotlin
     val onClick = remember { { performAction() } }
     ```
     
  8. **明智地使用CompositionLocal**：
     
     - 避免过度使用CompositionLocal，它可能导致整个子树重组
     
  9. **使用Layout Inspector和Compose编译器报告**：
     - 分析重组原因和频率
     - 识别过度重组的组件

  10. **避免读取组合期间的全局状态**：
      - 将全局状态包装为Compose状态

- **如何在Compose中实现动画？有哪几种动画API？** ⭐⭐⭐

  Compose提供多种动画API，从简单到复杂：

  1. **高级动画API**：
     - `animateContentSize`：自动为大小变化添加动画
     ```kotlin
     Box(modifier = Modifier.animateContentSize()) { /* 内容 */ }
     ```
     - `AnimatedVisibility`：为组件的显示/隐藏添加动画
     ```kotlin
     AnimatedVisibility(visible = isVisible) { /* 内容 */ }
     ```
     - `animateColorAsState`/`animateFloatAsState`：为单个值变化添加动画
     ```kotlin
     val color = animateColorAsState(if (isSelected) Color.Red else Color.Black)
     ```

  2. **中级动画API**：
     - `Transition`：协调多个值的动画
     ```kotlin
     val transition = updateTransition(targetState)
     val color = transition.animateColor { state -> if (state) Color.Red else Color.Black }
     val size = transition.animateFloat { state -> if (state) 100f else 50f }
     ```
     - `InfiniteTransition`：无限循环动画
     ```kotlin
     val infiniteTransition = rememberInfiniteTransition()
     val color = infiniteTransition.animateColor(
         initialValue = Color.Red,
         targetValue = Color.Green,
         animationSpec = infiniteRepeatable(tween(1000), RepeatMode.Reverse)
     )
     ```

  3. **低级动画API**：
     - `Animatable`：命令式动画控制器
     ```kotlin
     val position = remember { Animatable(0f) }
     LaunchedEffect(key1) {
         position.animateTo(100f)
     }
     ```
     - `Animation`和`AnimationVector`：支持向量动画，如位置(x,y)

  4. **手势动画**：
     - `draggable`，`swipeable`，`transformable`修饰符
     - 结合`animateTo`和`animateDecay`实现完整交互动画
     ```kotlin
     val state = rememberDraggableState { delta -> /* 处理拖动 */ }
     Modifier.draggable(state, Orientation.Horizontal)
     ```

  通用动画规格包括`spring()`、`tween()`、`repeatable()`、`keyframes()`，支持不同的曲线和时间配置。

- **Compose中的LazyColumn和RecyclerView有什么区别？** ⭐⭐⭐⭐

  LazyColumn和RecyclerView都用于高效显示长列表，但有几个关键区别：

  1. **声明式vs命令式**：
     - LazyColumn：声明式API，直接描述每个项目应该是什么样子
     - RecyclerView：命令式API，需要Adapter、ViewHolder等配置

  2. **代码简洁性**：
     - LazyColumn大大减少了模板代码量
     ```kotlin
     LazyColumn {
         items(dataList) { item ->
             ItemComposable(item)
         }
     }
     ```
     - RecyclerView需要创建多个类（Adapter、ViewHolder）和XML布局

  3. **状态管理**：
     - LazyColumn：自动响应状态变化重组列表项
     - RecyclerView：需要手动通知适配器数据变化(notifyItem...)

  4. **差异化更新**：
     - LazyColumn：基于key()函数自动处理差异化更新
     - RecyclerView：需要DiffUtil或手动实现差异化更新

  5. **滚动状态**：
     - LazyColumn：使用LazyListState控制和观察滚动状态
     - RecyclerView：使用LayoutManager和ScrollListener

  6. **项目布局预测**：
     - LazyColumn：无需预测，基于组合逻辑
     - RecyclerView：可能需要预测布局以优化性能

  7. **自定义布局**：
     - LazyColumn：使用Arrangement和自定义item布局
     - RecyclerView：通过LayoutManager实现自定义布局

  8. **嵌套滚动**：
     - LazyColumn：更好的嵌套滚动支持，如滚动内部其他可滚动组件
     - RecyclerView：嵌套滚动需要额外配置和协调

  9. **内部实现**：
     - LazyColumn实际上在内部使用了类似RecyclerView的回收机制

- **Compose如何处理生命周期？** ⭐⭐⭐⭐

  Compose处理生命周期的几个关键方面：

  1. **Composition生命周期**：
     - Compose UI树有自己的生命周期，独立于Activity/Fragment
     - 主要阶段：初始组合(Initial Composition)、重组(Recomposition)、离开组合(Leaving Composition)

  2. **与Android生命周期集成**：
     - ComposeView自动跟随宿主View的生命周期
     - 在Activity中，setContent{}绑定到Activity生命周期

  3. **生命周期感知**：
     - 使用LocalLifecycleOwner访问Android LifecycleOwner
     ```kotlin
     val lifecycleOwner = LocalLifecycleOwner.current
     ```

  4. **副作用与生命周期**：
     - DisposableEffect：在组件"死亡"时清理资源
     ```kotlin
     DisposableEffect(Unit) {
         // 设置，类似onCreate
         onDispose {
             // 清理，类似onDestroy
         }
     }
     ```
     - LaunchedEffect：协程范围与组件生命周期绑定

  5. **状态保存**：
     - rememberSaveable：通过savedInstanceState在配置变化中保存状态
     - 类似于Activity.onSaveInstanceState的功能

  6. **BackHandler**：
     - 处理返回按键事件，替代Activity.onBackPressed
     ```kotlin
     BackHandler { /* 处理返回事件 */ }
     ```

  7. **与ViewModel集成**：
     - viewModel()函数获取ViewModel，自动与生命周期绑定
     ```kotlin
     val viewModel = viewModel<MyViewModel>()
     ```

  8. **记忆化与生命周期**：
     - remember跟随Composable生命周期，而不是Android组件生命周期
     - 配置变化时remember的值会丢失，除非使用rememberSaveable

  9. **副作用调用时机**：
     - SideEffect：每次成功重组后调用
     - LaunchedEffect：组件进入组合或key变化时调用
     - DisposableEffect：组件进入组合时调用，离开组合时清理

  Compose生命周期管理更加简洁和声明式，减少了生命周期相关bug的可能性。

### 34、Room
- **什么是Room持久性库？它与原生SQLite相比有什么优势？** ⭐⭐⭐⭐⭐
- **Room的三个主要组件是什么？各自的作用是什么？** ⭐⭐⭐⭐
- **如何在Room中定义复杂查询？能否举例说明？** ⭐⭐⭐
- **Room如何处理数据库迁移(Migration)？** ⭐⭐⭐⭐
- **Room与LiveData、Flow、RxJava如何结合使用？** ⭐⭐⭐⭐
- **Room的事务处理方式有哪些？** ⭐⭐⭐
- **TypeConverter在Room中的作用是什么？** ⭐⭐⭐
- **Room与协程如何结合使用？挂起函数在DAO中有什么特点？** ⭐⭐⭐⭐

### 35、Kotlin语言特性
- **Kotlin与Java相比有哪些优势？** ⭐⭐⭐⭐⭐

  Kotlin相比Java的主要优势：

  1. **空安全**：通过类型系统区分可空和非空类型，在编译时就避免NullPointerException
  
  2. **简洁性**：
     - 类型推断减少了显式类型声明
     - 数据类简化POJO对象创建
     - Lambda表达式和高阶函数
     - 属性自动生成getter/setter
  
  3. **函数式编程支持**：
     - 一等公民函数
     - 不可变集合
     - 丰富的集合操作API
  
  4. **扩展函数**：无需继承即可扩展类的功能
  
  5. **协程支持**：简化异步编程和并发
  
  6. **互操作性**：与Java完全兼容，可以调用Java代码，Java也可以调用Kotlin
  
  7. **安全特性**：
     - 显式类型转换
     - 智能类型转换
     - 运算符重载

  8. **更现代化的语法**：
     - 默认参数值和命名参数
     - 表达式函数体
     - 字符串模板

  9. **避免常见错误**：
     - 没有原始类型
     - 默认为final类和方法
     - 强制处理异常

- **Kotlin中的空安全是如何实现的？什么是安全调用操作符和非空断言操作符？** ⭐⭐⭐⭐

  Kotlin的空安全系统通过类型系统区分可空类型和非空类型实现：

  1. **可空和非空类型**：
     - 默认情况下变量不可为null：`val name: String`
     - 添加问号表示可空：`val name: String?`
     - 编译器强制检查可空类型的使用

  2. **安全调用操作符**（`?.`）：
     - 仅当对象非空时才执行调用，否则返回null
     - 例：`person?.name` (如果person为null，则返回null，不执行.name)
     - 可链式使用：`person?.department?.head?.name`

  3. **非空断言操作符**（`!!`）：
     - 将任何值转换为非空类型，如果为null则抛出NPE
     - 例：`val length = str!!.length` (如果str为null，抛出异常)
     - 应该尽量避免使用，除非确实需要NPE

  4. **Elvis操作符**（`?:`）：
     - 当左侧表达式为null时提供默认值
     - 例：`val name = person?.name ?: "Unknown"`

  5. **安全类型转换**（`as?`）：
     - 尝试转换类型，如果不匹配则返回null而不抛出异常
     - 例：`val customer = person as? Customer`

  6. **平台类型**：
     - 从Java代码返回的类型被视为"平台类型"，编译器不确定其空安全性
     - 可以被当作可空或非空类型处理，但开发者需要小心

- **什么是Kotlin的扩展函数？它与Java相比有什么不同？** ⭐⭐⭐⭐

  扩展函数允许给现有类添加新函数，无需继承或装饰器模式。

  **基本概念**：
  ```kotlin
  fun String.addHello(): String {
      return "Hello, $this"
  }
  
  // 使用
  val result = "World".addHello() // 返回 "Hello, World"
  ```

  **与Java区别**：
  1. **静态解析**：
     - Kotlin扩展在编译时静态解析，不是运行时动态派发
     - 实际编译为带接收者参数的静态方法
     - Java需要辅助类或装饰器模式实现类似功能

  2. **接收者类型**：
     - 扩展声明在接收者类型外部
     - 可以为任何类型定义扩展，包括第三方库和Java类

  3. **可空接收者**：
     - 可以为可空类型定义扩展，安全处理null
     ```kotlin
     fun String?.isNullOrBlank(): Boolean = this == null || this.isBlank()
     ```

  4. **可见性**：
     - 扩展函数对整个项目可见，不局限在类内部
     - 可以导入特定扩展，避免命名冲突

  5. **成员优先原则**：
     - 如果扩展函数和成员函数签名相同，成员函数优先调用

  6. **属性扩展**：
     - 也可以定义扩展属性
     ```kotlin
     val String.lastChar: Char get() = this[length - 1]
     ```

  扩展函数的主要优势是不修改原类的情况下增强其功能，同时保持代码整洁和类型安全。

- **Kotlin中的数据类(data class)有什么特点？** ⭐⭐⭐⭐

  数据类是专为保存数据设计的类，仅通过一行代码就能替代传统Java POJO类的大量模板代码。

  **特点**：

  1. **自动生成方法**：
     - `equals()/hashCode()`：基于主构造函数中声明的所有属性
     - `toString()`：返回格式化字符串，包含所有属性
     - `componentN()`：用于解构声明
     - `copy()`：创建对象副本，可选择修改部分属性

  2. **声明简洁**：
     ```kotlin
     data class User(val name: String, val age: Int, val email: String)
     ```
     等同于Java中包含所有属性、getter/setter、equals/hashCode/toString的完整类

  3. **使用限制**：
     - 主构造函数必须至少有一个参数
     - 参数必须标记为`val`或`var`
     - 不能是抽象、开放、密封或内部类
     - 可以实现接口并继承其他类

  4. **解构能力**：
     ```kotlin
     val user = User("Alex", 30, "alex@example.com")
     val (name, age, email) = user  // 解构声明
     ```

  5. **不可变性支持**：
     - 推荐使用`val`声明属性，创建不可变数据类
     - 配合`copy()`方法实现不可变对象的修改

  6. **复制与修改**：
     ```kotlin
     val updatedUser = user.copy(age = 31)
     ```

  7. **集合操作优化**：
     - 适合用作映射的键或集合元素，因为有可靠的equals/hashCode

  数据类极大简化了处理数据的代码，提高可读性和可维护性，是Kotlin减少样板代码的典型例子。

- **什么是Kotlin的密封类(sealed class)？它与枚举相比有什么优势？** ⭐⭐⭐

  密封类是一种限制类继承层次结构的特殊类，提供了类型安全的方式来表示受限的类层次结构。

  **基本概念**：
  ```kotlin
  sealed class Result {
      data class Success(val data: Any) : Result()
      data class Error(val message: String, val cause: Exception? = null) : Result()
      object Loading : Result()
  }
  ```

  **特点**：
  1. **受限继承**：
     - 所有直接子类必须在同一文件中声明
     - 密封类自身是抽象的，不能直接实例化
  
  2. **穷举性检查**：
     - `when`表达式不需要`else`分支，编译器可以验证已覆盖所有可能情况
     ```kotlin
     when (result) {
         is Result.Success -> handleSuccess(result.data)
         is Result.Error -> handleError(result.message)
         is Result.Loading -> showLoadingIndicator()
     }
     ```

  **与枚举相比的优势**：
  1. **可承载数据**：
     - 每个子类可以有不同的属性和参数
     - 枚举每个常量只能有相同的属性集

  2. **灵活性**：
     - 子类可以是任意类型（data class、object、常规class）
     - 枚举常量本质上都是相同类型的单例

  3. **扩展性**：
     - 密封类子类可以有多个实例（除了object）
     - 枚举每个常量只有一个实例

  4. **层次结构**：
     - 密封类可以创建复杂类层次，子类还可以有子类
     - 枚举是扁平的结构

  **应用场景**：
  - 表示受限的类层次结构（如网络结果、UI状态）
  - 需要区分多种情况，且每种情况携带不同数据
  - 状态机实现
  - 代替类型码模式

- **Kotlin的委托属性(Delegated Properties)是什么？有什么用途？** ⭐⭐⭐⭐

  委托属性允许将属性的getter/setter逻辑委托给另一个对象，实现属性行为的定制化与复用。

  **基本语法**：
  ```kotlin
  class Example {
      var p: String by Delegate()
  }
  ```

  **工作原理**：
  - 委托对象必须实现`getValue()`和`setValue()`方法（对于var属性）
  - 编译器生成辅助属性和访问器，将操作委托给指定对象

  **常用内置委托**：

  1. **lazy**：实现延迟初始化
     ```kotlin
     val expensiveValue: String by lazy {
         println("Computing...")
         computeExpensiveString()
     }
     ```
     - 仅在首次访问时计算并缓存结果
     - 线程安全（默认同步锁定）

  2. **observable/vetoable**：观察/验证属性变化
     ```kotlin
     var name: String by Delegates.observable("Initial") { prop, old, new ->
         println("Name changed from $old to $new")
     }
     
     var age: Int by Delegates.vetoable(0) { prop, old, new ->
         new >= 0 // 负值将被拒绝
     }
     ```

  3. **map存储**：从Map读写属性
     ```kotlin
     class User(val map: Map<String, Any?>) {
         val name: String by map
         val age: Int by map
     }
     ```

  4. **notNull**：非空属性延迟初始化
     ```kotlin
     var name: String by Delegates.notNull()
     ```

  **主要用途**：

  1. **行为复用**：
     - 多个属性共享相同的访问逻辑
     - 避免重复代码

  2. **关注点分离**：
     - 将属性存储与访问逻辑从类主逻辑分离
     - 使类更专注于核心功能

  3. **自定义行为**：
     - 属性验证
     - 通知/事件触发
     - 懒加载
     - 值映射/转换

  4. **框架功能**：
     - ViewModel中的savedStateHandle属性委托
     - 视图绑定
     - 依赖注入

  委托属性是Kotlin最强大的特性之一，可以显著简化代码并提高可重用性。

- **Kotlin的伴生对象(companion object)与Java的静态成员有什么区别？** ⭐⭐⭐

  伴生对象是Kotlin实现类级别功能的方式，与Java静态成员概念类似但有显著区别。

  **基本语法**：
  ```kotlin
  class MyClass {
      companion object {
          const val MAX_COUNT = 100
          fun create(): MyClass = MyClass()
      }
  }
  
  // 使用
  val max = MyClass.MAX_COUNT
  val instance = MyClass.create()
  ```

  **与Java静态成员的区别**：

  1. **实例性质**：
     - 伴生对象是真实的对象实例，而不只是静态成员集合
     - 在运行时确实存在，有自己的内存分配

  2. **特性和能力**：
     - 可以实现接口
     - 可以保存状态
     - 可以有初始化代码块
     ```kotlin
     class MyClass {
         companion object MyCompanion : SomeInterface {
             init { println("Companion initialized") }
             override fun interfaceMethod() {}
         }
     }
     ```

  3. **命名和引用**：
     - 可以命名（如上例的MyCompanion），也可以匿名
     - 可以被独立引用：`val companion = MyClass.Companion`

  4. **扩展函数**：
     - 伴生对象可以有扩展函数
     ```kotlin
     fun MyClass.Companion.additionalFunction() { /* ... */ }
     ```

  5. **JVM实现**：
     - 编译为类的私有静态final字段和静态初始化器
     - 使用`@JvmStatic`注解可使方法编译为真正的Java静态方法
     ```kotlin
     companion object {
         @JvmStatic fun staticMethod() {}
     }
     ```

  6. **作用域**：
     - 伴生对象可以访问包含类的私有成员
     - Java静态方法不能直接访问实例成员

  **伴生对象最佳实践**：
  - 工厂方法
  - 常量定义
  - 单例实现
  - 实用工具方法
  - 默认值提供

- **Kotlin中的高阶函数和Lambda表达式有什么特点？** ⭐⭐⭐⭐

  高阶函数和Lambda表达式是Kotlin函数式编程的核心特性，极大提升了代码简洁性和表达能力。

  **高阶函数**：
  - 接受函数作为参数或返回函数的函数
  ```kotlin
  fun <T, R> Collection<T>.mapCustom(transform: (T) -> R): List<R> {
      val result = mutableListOf<R>()
      for (item in this) {
          result.add(transform(item))
      }
      return result
  }
  ```

  **Lambda表达式特点**：

  1. **简洁语法**：
     ```kotlin
     val sum = { x: Int, y: Int -> x + y }
     val numbers = listOf(1, 2, 3, 4)
     val doubled = numbers.map { it * 2 }  // 使用it引用单个参数
     ```

  2. **函数类型**：
     - 明确的类型表示法：`(Int, Int) -> Int`
     - 可空函数类型：`((Int) -> String)?`
     - 带接收者的函数类型：`Int.(Int) -> Int`

  3. **闭包特性**：
     - Lambda可以引用和修改外部变量
     ```kotlin
     var sum = 0
     listOf(1, 2, 3).forEach { sum += it }
     ```

  4. **尾随Lambda**：
     - 当函数的最后一个参数是函数时，可以放在括号外
     ```kotlin
     files.filter { it.isFile }
          .map { it.name }
     ```

  5. **隐式参数**：
     - 单参数lambda可用`it`隐式引用
     ```kotlin
     list.filter { it > 0 }
     ```

  6. **解构**：
     - Lambda参数可以解构
     ```kotlin
     map.forEach { (key, value) -> println("$key = $value") }
     ```

  **常见用途**：

  1. **集合操作**：
     ```kotlin
     val adults = people
         .filter { it.age >= 18 }
         .sortedBy { it.name }
         .map { it.name }
     ```

  2. **操作构建器**：
     ```kotlin
     val dialog = AlertDialog.Builder(context)
         .setTitle("Title")
         .setPositiveButton("OK") { dialog, _ -> dialog.dismiss() }
         .create()
     ```

  3. **资源管理**：
     ```kotlin
     fun <T> withResource(resource: Resource, block: (Resource) -> T): T {
         try {
             return block(resource)
         } finally {
             resource.close()
         }
     }
     ```

  4. **自定义控制结构**：
     ```kotlin
     inline fun transaction(block: () -> Unit) {
         beginTransaction()
         try {
             block()
             commit()
         } catch (e: Exception) {
             rollback()
             throw e
         }
     }
     ```

- **Kotlin中的内联函数(inline function)有什么优势？** ⭐⭐⭐

  内联函数通过在编译时将函数调用替换为函数体内容，提高了使用Lambda表达式时的性能和功能。

  **基本用法**：
  ```kotlin
  inline fun repeat(times: Int, action: (Int) -> Unit) {
      for (index in 0 until times) {
          action(index)
      }
  }
  ```

  **主要优势**：

  1. **减少运行时开销**：
     - 避免为Lambda创建匿名类对象
     - 消除函数调用开销
     - 减少内存分配和垃圾回收压力
     ```kotlin
     // 使用内联函数
     repeat(1000) { println(it) }  // 编译后无额外对象创建
     
     // 非内联等效
     repeat(1000, object : Function1<Int, Unit> {  // 创建匿名对象
         override fun invoke(it: Int) {
             println(it)
         }
     })
     ```

  2. **支持非局部返回**：
     - 可以从Lambda中返回外层函数
     ```kotlin
     fun findPerson(people: List<Person>, predicate: (Person) -> Boolean): Person? {
         people.forEach {
             if (predicate(it)) return it  // 从findPerson函数返回
         }
         return null
     }
     ```

  3. **支持reified泛型参数**：
     - 在运行时保留泛型类型信息
     ```kotlin
     inline fun <reified T> Any.isOfType(): Boolean = this is T
     
     // 使用
     val isString = obj.isOfType<String>()  // 编译为 obj is String
     ```

  4. **crossinline与noinline修饰符**：
     - crossinline：禁止非局部返回但仍内联
     - noinline：禁止参数内联，当需要将Lambda作为对象传递时
     ```kotlin
     inline fun example(
         crossinline c: () -> Unit,
         noinline n: () -> Unit
     ) { /* ... */ }
     ```

  **常见应用场景**：
  1. **资源管理模式**：如`use`、`withLock`、`runBlocking`
  2. **控制流构建器**：如`run`、`let`、`apply`、`also`
  3. **重复操作**：如`repeat`
  4. **条件执行**：如`takeIf`、`takeUnless`
  5. **集合操作**：如`filter`、`map`、`forEach`

  **注意事项**：
  - 内联会增加生成代码的大小
  - 复杂函数内联可能导致代码膨胀
  - 应优先内联短小且频繁调用的函数

- **什么是Kotlin的解构声明(destructuring declaration)？** ⭐⭐⭐

  解构声明允许将一个对象同时解包到多个变量中，提高代码可读性和简洁性。

  **基本语法**：
  ```kotlin
  val (name, age, email) = person
  ```

  **工作原理**：
  - 依赖于命名为`componentN()`的函数
  - data class自动生成这些函数
  - 可以为任何类手动实现这些函数

  **支持解构的数据类型**：

  1. **数据类**：自动支持
     ```kotlin
     data class Person(val name: String, val age: Int, val email: String)
     val person = Person("Alex", 30, "alex@example.com")
     val (name, age, email) = person  // 解构
     ```

  2. **Pair和Triple**：
     ```kotlin
     val pair = Pair("John", 25)
     val (name, age) = pair
     ```

  3. **Map.Entry**：
     ```kotlin
     for ((key, value) in map) {
         println("$key -> $value")
     }
     ```

  4. **自定义类**：通过实现componentN函数
     ```kotlin
     class Point(val x: Int, val y: Int) {
         operator fun component1() = x
         operator fun component2() = y
     }
     
     val (x, y) = Point(10, 20)
     ```

  5. **数组和集合**：通过扩展函数支持
     ```kotlin
     val (first, second, third) = listOf(1, 2, 3)
     ```

  **高级用法**：

  1. **忽略部分值**：
     ```kotlin
     val (name, _, email) = person  // 忽略age
     ```

  2. **函数返回值解构**：
     ```kotlin
     fun getPersonInfo(): Triple<String, Int, String> = Triple("Alex", 30, "alex@example.com") 
     val (name, age, email) = getPersonInfo()
     ```

  3. **Lambda参数解构**：
     ```kotlin
     map.mapValues { (_, value) -> value.uppercase() }
     ```

  4. **解构与类型声明结合**：
     ```kotlin
     val (name: String, age: Int) = pair
     ```

  5. **循环中解构**：
     ```kotlin
     for ((index, element) in collection.withIndex()) {
         println("$index: $element")
     }
     ```

  解构声明使得处理复合数据结构更加直观和简洁，特别是在处理返回多个值的情况下。

### 36、协程(Coroutines)
- **什么是协程？协程与线程的区别？** ⭐⭐⭐⭐⭐
- **协程的基本构建块有哪些？(CoroutineScope, CoroutineContext, Job等)** ⭐⭐⭐⭐
- **协程的调度器(Dispatchers)有哪些？各自适用于什么场景？** ⭐⭐⭐⭐
- **launch和async的区别是什么？什么时候使用哪一个？** ⭐⭐⭐⭐⭐
- **协程中的异常处理机制是怎样的？** ⭐⭐⭐⭐
- **协程的取消机制是如何工作的？如何确保协程可取消？** ⭐⭐⭐⭐
- **什么是结构化并发(Structured Concurrency)？它有什么优势？** ⭐⭐⭐⭐
- **suspend关键字的作用是什么？它与普通函数有什么区别？** ⭐⭐⭐⭐⭐
- **Flow是什么？它与RxJava、LiveData相比有什么特点？** ⭐⭐⭐⭐
- **协程作用域(CoroutineScope)有哪些？lifecycleScope、viewModelScope、GlobalScope分别适用于什么场景？** ⭐⭐⭐⭐

### 37、KAPT与KSP
- **什么是KAPT(Kotlin Annotation Processing Tool)？它与Java的注解处理器有什么区别？** ⭐⭐⭐⭐
- **KSP(Kotlin Symbol Processing)是什么？它相比KAPT有什么优势？** ⭐⭐⭐⭐⭐
- **KAPT在Dagger/Hilt、Room等框架中的应用？** ⭐⭐⭐
- **如何在项目中配置和使用KAPT/KSP？** ⭐⭐⭐
- **KSP与编译速度的关系？为什么KSP比KAPT更快？** ⭐⭐⭐⭐
- **如何编写兼容KAPT和KSP的注解处理器？** ⭐⭐⭐
- **KAPT/KSP在多模块项目中的配置和注意事项？** ⭐⭐⭐⭐

### 38、Jetpack库与架构组件
- **ViewModel的作用是什么？它如何帮助管理UI相关数据？** ⭐⭐⭐⭐⭐
- **LiveData是什么？它与Observable、Flow有什么区别？** ⭐⭐⭐⭐
- **DataBinding和ViewBinding的区别是什么？各自的优缺点？** ⭐⭐⭐⭐
- **Navigation组件的主要组成部分是什么？它如何简化Fragment之间的导航？** ⭐⭐⭐⭐
- **什么是Lifecycle组件？它如何解决生命周期管理问题？** ⭐⭐⭐⭐
- **WorkManager用于什么场景？它与其他后台处理方案相比有什么优势？** ⭐⭐⭐⭐
- **Paging 3的主要组件是什么？它如何实现高效的分页加载？** ⭐⭐⭐⭐
- **Hilt与Dagger 2相比有什么改进？它如何简化依赖注入？** ⭐⭐⭐⭐⭐
- **DataStore与SharedPreferences相比有什么优势？** ⭐⭐⭐
- **CameraX API与Camera2 API相比有什么优势？** ⭐⭐⭐

### 39、Kotlin多平台(KMP)与Compose Multiplatform
- **什么是Kotlin多平台(KMP)？它的主要优势是什么？** ⭐⭐⭐⭐
- **KMP项目架构通常如何组织？共享哪些代码？** ⭐⭐⭐⭐
- **Compose Multiplatform如何实现跨平台UI开发？** ⭐⭐⭐⭐⭐
- **如何在KMP项目中处理平台特定代码？expect/actual关键字的作用？** ⭐⭐⭐⭐
- **KMP项目如何处理网络请求和数据存储？** ⭐⭐⭐
- **KMP与Flutter、React Native等跨平台框架相比有什么优劣势？** ⭐⭐⭐⭐

### 40、App模块化与动态交付
- **什么是应用模块化？它有什么优势？** ⭐⭐⭐⭐
- **Dynamic Feature Module如何工作？它解决了什么问题？** ⭐⭐⭐⭐
- **模块间依赖与通信有哪些实现方式？** ⭐⭐⭐⭐
- **如何在多模块项目中管理版本依赖？** ⭐⭐⭐
- **多模块项目的构建速度优化策略有哪些？** ⭐⭐⭐⭐
- **模块化架构中如何实现单模块调试？** ⭐⭐⭐
- **App Bundle与Split APKs的区别和优势？** ⭐⭐⭐⭐
