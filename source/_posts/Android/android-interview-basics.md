---
title: 安卓面试经验 - 基础知识篇
tags:
  - interview
  - basics
index_img: /img/android-bot.png
categories:
  - Android
date: 2025-03-09 19:13:06
---

## 第二部分：Android基础知识篇

### 5、Context
- **谈谈你对Activity的Context的认识？** ⭐⭐⭐⭐⭐

  Context是Android应用程序环境的全局信息接口，是一个抽象类。通过Context，我们可以访问应用程序特定的资源、启动Activity、获取系统服务等。
  
  Activity的Context特点：
  - 生命周期与Activity相同，当Activity销毁时，其Context也随之销毁
  - 可以用于显示UI相关操作，如启动新Activity、显示Dialog等
  - 持有Activity的引用，所以在内存管理上需要注意避免内存泄漏
  - 可以访问主题相关属性，包含Activity的主题信息

- **Application和Activity,Context的区别？** ⭐⭐⭐⭐⭐

  两者都是Context的子类，但有以下区别：
  
  1. 生命周期不同：
     - Application Context存在于整个应用生命周期
     - Activity Context仅在Activity生命周期内有效
  
  2. 功能差异：
     - Activity Context可以用于UI操作（如启动Activity、显示Dialog）
     - Application Context不应用于UI操作，主要用于获取应用级资源
  
  3. 内存影响：
     - 长期持有Activity Context可能导致内存泄漏
     - 使用Application Context通常更安全
  
  4. 获取方式：
     - Activity中可通过this或getBaseContext()获取
     - Application可通过getApplicationContext()获取

- **getApplication()和getApplicationContext()的区别？** ⭐⭐⭐⭐

  1. 返回类型不同：
     - getApplication()返回Application实例，需要强制类型转换才能访问自定义Application中的方法和变量
     - getApplicationContext()返回Context类型
  
  2. 使用范围不同：
     - getApplication()只能在Activity和Service中使用
     - getApplicationContext()可在任何拥有Context引用的地方使用
  
  3. 功能上：
     - 在大多数场景中，两者作用相同，都可获取应用级Context
     - 但如果自定义了Application类，getApplication()可以直接调用自定义方法

- **context错误用法有哪些？** ⭐⭐⭐

  常见错误用法：
  
  1. 使用Activity Context做长生命周期对象的引用，导致内存泄漏
  2. 使用Application Context展示Dialog或启动Activity（缺少必要主题属性）
  3. 在Application的onCreate前调用getApplicationContext()
  4. 在静态方法或单例中持有Activity Context
  5. 在多进程应用中，跨进程使用同一Context对象

- **如何正确使用Context，如何获取Context？** ⭐⭐⭐⭐

  正确使用原则：
  
  1. 需要与UI相关的操作（Dialog、启动Activity）使用Activity Context
  2. 生命周期长的对象应使用Application Context
  3. 在匿名内部类、异步任务中引用Context时使用弱引用
  
  获取Context的方式：
  - Activity中：this或getBaseContext()
  - Fragment中：getActivity()或requireContext()
  - Service中：this
  - Receiver中：onReceive方法参数
  - Application中：this或getApplicationContext()
  - 自定义View中：getContext()
  - 非UI线程中：可通过Handler传递，或使用ApplicationContext

- **一个应用程序有几个Context？** ⭐⭐⭐⭐

  一个应用程序中的Context数量是动态变化的，包括：
  
  1. 一个Application Context（全局唯一）
  2. 每个Activity一个Context实例
  3. 每个Service一个Context实例
  4. 每个ContentProvider一个Context实例
  5. 每个BroadcastReceiver在激活时会临时获得一个Context
  
  因此，Context总数 = 1 + 活动的四大组件数量。所有这些Context都继承自ContextWrapper，最终都指向同一个ContextImpl实现类，但具有不同的功能限制和生命周期。

### 6、Intent
- **什么是Intent？** ⭐⭐⭐⭐⭐

  Intent是Android组件之间通信的一种消息传递机制，用于启动组件、传递数据和触发操作。Intent可以视为一个包含操作请求的抽象描述。
  
  Intent的主要用途：
  - 启动Activity（startActivity/startActivityForResult）
  - 启动Service（startService/bindService）
  - 传递广播（sendBroadcast）
  - 在组件间传递数据

  Intent的主要组成部分：
  - Component（组件）：指定目标组件
  - Action（动作）：指定要执行的操作类型
  - Data（数据）：操作要执行的数据URI
  - Category（类别）：提供关于组件处理Intent的附加信息
  - Extras（附加数据）：键值对形式传递的额外数据
  - Flags（标志）：指示Android系统如何启动Activity

- **显式Intent和隐式Intent的区别？** ⭐⭐⭐⭐

  显式Intent:
  - 明确指定目标组件的名称（包名和类名）
  - 用于启动应用内部的组件
  - 确保唯一匹配，不会弹出选择对话框
  - 示例：`Intent intent = new Intent(MainActivity.this, SecondActivity.class);`
  
  隐式Intent:
  - 不明确指定目标组件，而是通过Intent过滤器进行匹配
  - 用于调用其他应用的功能，如拨打电话、打开网页等
  - 可能匹配多个组件，系统会显示选择对话框
  - 通过Action、Category、Data等属性进行匹配
  - 示例：`Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://www.example.com"));`

  主要区别：
  - 指定方式不同：组件名称 vs 意图描述
  - 适用范围不同：应用内部 vs 跨应用调用
  - 安全性不同：显式更安全，隐式可能被恶意应用拦截

- **在隐式启动中Intent可以设置多个action,多个category吗？** ⭐⭐⭐⭐

  关于多个action:
  - Intent只能设置一个action
  - 同时设置多个会覆盖之前的设置，只有最后一个生效
  - 示例：`intent.setAction("action1"); intent.setAction("action2");` 只有action2生效

  关于多个category:
  - Intent可以添加多个category
  - 使用addCategory方法可以添加多个不同的category
  - 示例：`intent.addCategory("category1"); intent.addCategory("category2");` 两个category都生效
  - 所有添加的category都必须匹配才能启动目标组件

  注意事项：
  - 系统默认会添加CATEGORY_DEFAULT，所以在过滤器中必须包含此category
  - 多个category是"与"关系，目标组件必须同时支持所有指定的category

- **隐式Intent的匹配规则？** ⭐⭐⭐⭐⭐

  匹配过程基于AndroidManifest.xml中的Intent-filter，包括以下步骤：
  
  1. Action匹配规则：
     - Intent必须有一个action
     - 该action必须和过滤器中的某个action相同
     - 过滤器没有指定action时，无法匹配任何Intent
  
  2. Category匹配规则：
     - Intent中所有category必须在过滤器中找到匹配项
     - Intent可以没有category（但系统会默认添加DEFAULT）
     - 过滤器可以声明多个category
  
  3. Data匹配规则：
     - 包括URI和MIME类型两部分
     - URI进一步分解为scheme、host、port、path等
     - 所有部分都必须匹配
     - 如过滤器未指定data，则只接收没有data的Intent

  完整匹配流程：
  - 首先检查组件是否已导出（exported属性）
  - 然后逐步检查action、category、data是否匹配
  - 三个条件必须同时满足才算匹配成功
  - 如匹配多个组件，系统会显示选择器

- **Activity之间传递数据的方式Intent是否有大小限制，如果传递的数据量偏大，有哪些方案？** ⭐⭐⭐

  Intent大小限制：
  - Android对Intent传递数据大小有限制，约为1MB（具体取决于设备）
  - 超过限制会抛出TransactionTooLargeException异常
  - 这个限制是因为Intent会被序列化并通过Binder传递，Binder事务缓冲区大小有限
  
  传递大数据的替代方案：
  
  1. 使用单例或静态变量（不推荐，可能导致内存泄漏）
     - 在发送方保存数据引用
     - 在接收方获取该引用
  
  2. 使用本地存储：
     - SharedPreferences（适合小型键值对数据）
     - 文件存储（保存数据到文件，传递文件路径）
     - SQLite数据库（结构化数据）
  
  3. 使用ContentProvider：
     - 创建临时ContentProvider
     - 通过URI访问数据
  
  4. 使用系统服务：
     - 使用剪贴板ClipboardManager
  
  5. 使用Application全局变量：
     - 在自定义Application中定义变量
     - 注意生命周期管理
  
  6. 使用第三方解决方案：
     - EventBus
     - RxJava
  
  最佳实践：
  - 为大型复杂对象使用持久化存储方案
  - 传递唯一标识符（如ID或URI）而不是完整对象
  - 考虑数据分片传输

### 7、Handler异步消息机制
- **请介绍下Handler消息机制** ⭐⭐⭐⭐⭐
- **Handler 引起的内存泄露原因以及最佳解决方案** ⭐⭐⭐⭐⭐
- **为什么我们能在主线程直接使用 Handler，而不需要创建 Looper ？** ⭐⭐⭐⭐⭐
- **Handler、Thread和HandlerThread的差别** ⭐⭐⭐⭐
- **子线程中怎么使用 Handler？** ⭐⭐⭐⭐
- **为什么在子线程中创建 Handler 会抛异常？** ⭐⭐⭐⭐
- **Handler 里藏着的 Callback 能干什么？** ⭐⭐⭐
- **Handler 的 send 和 post 的区别？** ⭐⭐⭐⭐
- **创建 Message 实例的最佳方式** ⭐⭐⭐
- **Message 的插入以及回收是如何进行的，如何实例化一个 Message 呢？** ⭐⭐⭐
- **妙用Looper机制，或者你知道Handler机制的其他用途吗？** ⭐⭐⭐
- **Looper.loop()死循环一直运行是不是特别消耗CPU资源呢？不会造成应用卡死吗？** ⭐⭐⭐⭐⭐
- **MessageQueue 中如何等待消息？为何不使用 Java 中的 wait/notify 来实现阻塞等待呢？** ⭐⭐
- **你知道延时消息的原理吗？** ⭐⭐⭐⭐
- **handler postDelay这个延迟是怎么实现的？** ⭐⭐⭐⭐
- **如何保证在msg.postDelay情况下保证消息次序？** ⭐⭐⭐
- **更新UI的方式有哪些** ⭐⭐⭐⭐
- **线程、Handler、Looper、MessageQueue 的关系？** ⭐⭐⭐⭐
- **多个线程给 MessageQueue 发消息，如何保证线程安全？** ⭐⭐⭐
- **View.post 和 Handler.post 的区别？** ⭐⭐⭐
- **你知道 IdleHandler 吗？** ⭐⭐

### 8、HandlerThread
- **HandlerThread是什么？** ⭐⭐⭐⭐⭐
- **HandlerThread原理和使用场景？** ⭐⭐⭐⭐

### 9、AsyncTask
- **AsyncTask是什么？能解决什么问题** ⭐⭐⭐⭐
- **给我谈谈AsyncTask的三个泛型参数作用以及它的一些方法作用。** ⭐⭐⭐
- **给我说说AsyncTask的原理。** ⭐⭐⭐
- **你觉得AsyncTask有不足之处吗？有何使用注意事项？** ⭐⭐⭐

### 10、IntentService
- **IntentService是什么？** ⭐⭐⭐⭐⭐
- **IntentService原理和使用场景？** ⭐⭐⭐⭐
- **IntentService和Service的区别** ⭐⭐⭐⭐⭐

### 11、Fragment
- **Fragment是什么？和Activity的联系？生命周期如何？** ⭐⭐⭐⭐⭐⭐

  Fragment定义与特点：
  - Fragment是Activity中的一个UI模块，表示Activity中的行为或用户界面部分
  - 可以将多个Fragment组合在一个Activity中构建多窗格UI
  - 一个Fragment可以在多个Activity中复用
  - Fragment拥有自己的生命周期，但受宿主Activity生命周期影响
  - Android 3.0（API 11）引入，通过支持库可向下兼容

  与Activity的联系：
  - Fragment必须嵌入在Activity中使用，不能独立存在
  - Fragment的生命周期直接受宿主Activity生命周期的影响
  - 一个Activity可以包含多个Fragment
  - Fragment可以访问所属Activity的上下文
  - Fragment可以接收和处理输入事件，并拥有自己的回退栈

  Fragment生命周期：
  1. **onAttach()**: Fragment与Activity关联时调用
  2. **onCreate()**: 创建Fragment时调用，进行初始化但不应访问视图
  3. **onCreateView()**: 创建Fragment视图时调用，返回Fragment的UI根视图
  4. **onViewCreated()**: 在onCreateView()之后调用，此时视图层次已创建
  5. **onActivityCreated()**: Activity的onCreate()方法执行完毕后调用（已弃用）
  6. **onViewStateRestored()**: 视图状态恢复后调用
  7. **onStart()**: Fragment可见但不可交互时调用
  8. **onResume()**: Fragment可见且可交互时调用
  9. **onPause()**: 用户离开Fragment、Fragment不再交互时调用
  10. **onStop()**: Fragment不再可见时调用
  11. **onDestroyView()**: Fragment视图被移除时调用
  12. **onDestroy()**: Fragment状态被销毁时调用
  13. **onDetach()**: Fragment与Activity解除关联时调用

  Fragment生命周期特点：
  - 比Activity生命周期更复杂
  - AndroidX中引入了Fragment生命周期观察者(LifecycleObserver)
  - 与Activity生命周期紧密关联但又相互独立

- **Activity和Fragment之间如何通讯？Fragment和Fragment之间如何通讯？** ⭐⭐⭐⭐⭐

  Activity与Fragment通信：
  
  1. 接口回调:
     ```java
     // 在Fragment中定义接口
     public interface OnFragmentInteractionListener {
         void onFragmentInteraction(Uri uri);
     }
     
     // Activity实现该接口
     public class MainActivity extends AppCompatActivity 
                             implements MyFragment.OnFragmentInteractionListener {
         @Override
         public void onFragmentInteraction(Uri uri) {
             // 处理Fragment传来的数据
         }
     }
     ```
  
  2. 直接方法调用:
     - Fragment通过`getActivity()`获取Activity实例并调用其方法
     - Activity通过`FragmentManager`获取Fragment实例并调用其方法
  
  3. Bundle传递数据:
     - 创建Fragment时通过`setArguments(Bundle)`传递参数
     - Fragment中通过`getArguments()`获取数据
  
  4. ViewModel共享:
     - 使用AndroidX ViewModel创建共享ViewModel
     - Activity和Fragment都可以访问这个ViewModel中的数据
  
  Fragment与Fragment通信：
  
  1. 通过Activity中转:
     - Fragment A → Activity → Fragment B
  
  2. 共享ViewModel:
     ```java
     // 在两个Fragment中获取相同的ViewModel实例
     SharedViewModel viewModel = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);
     ```
  
  3. Fragment Result API (AndroidX):
     ```java
     // Fragment A: 设置结果
     parentFragmentManager.setFragmentResult("requestKey", bundleOf("bundleKey" to "result"))
     
     // Fragment B: 监听结果
     parentFragmentManager.setFragmentResultListener("requestKey", viewLifecycleOwner) { key, bundle ->
         val result = bundle.getString("bundleKey")
         // 使用结果
     }
     ```
  
  4. EventBus等第三方库:
     - 使用发布-订阅模式进行解耦通信
  
  5. 接口回调（通过Activity):
     - 两个Fragment实现相同的接口，由Activity协调

- **Fragment的回退栈了解吗？** ⭐⭐⭐⭐

  Fragment回退栈是一种管理Fragment添加和移除操作的机制，使用户能通过返回按钮来逐步回退Fragment事务。
  
  主要特点：
  - 每个回退栈条目记录一次完整的Fragment事务
  - 由FragmentManager管理
  - 可以为事务指定一个名字，便于后续查找
  
  基本操作：
  ```java
  // 添加Fragment事务到回退栈
  getSupportFragmentManager().beginTransaction()
      .replace(R.id.container, newFragment)
      .addToBackStack("transaction_name")  // 添加到回退栈并命名
      .commit();
  
  // 弹出回退栈顶部事务
  getSupportFragmentManager().popBackStack();
  
  // 弹出指定名称的事务及其之上的所有事务
  getSupportFragmentManager().popBackStack("transaction_name", 0);
  
  // 弹出指定名称的事务（含）及其之上的所有事务
  getSupportFragmentManager().popBackStack("transaction_name", FragmentManager.POP_BACK_STACK_INCLUSIVE);
  ```
  
  注意事项：
  - 当回退栈为空时，按返回键会退出Activity
  - 可以通过`addToBackStack(null)`添加未命名的事务到回退栈
  - 可以监听回退栈变化：`addOnBackStackChangedListener()`
  - 调用`popBackStack()`是异步操作，立即调用`findFragmentByTag()`可能找不到预期的Fragment
  - Fragment状态保存后（onSaveInstanceState之后）不能再执行事务
  - 在AndroidX中使用`FragmentManager.popBackStackImmediate()`执行同步弹出操作

- **Fragment的使用方式** ⭐⭐⭐

  1. XML静态添加:
     ```xml
     <fragment
         android:id="@+id/fragment_container"
         android:name="com.example.MyFragment"
         android:layout_width="match_parent"
         android:layout_height="match_parent" />
     ```
  
  2. 代码动态添加:
     ```java
     getSupportFragmentManager().beginTransaction()
         .add(R.id.fragment_container, new MyFragment())
         .commit();
     ```
  
  3. 使用FragmentContainerView (推荐):
     ```xml
     <androidx.fragment.app.FragmentContainerView
         android:id="@+id/fragment_container_view"
         android:name="com.example.MyFragment"
         android:layout_width="match_parent"
         android:layout_height="match_parent" />
     ```
  
  4. ViewPager2中使用Fragment:
     ```java
     viewPager.setAdapter(new FragmentStateAdapter(this) {
         @NonNull
         @Override
         public Fragment createFragment(int position) {
             return new MyFragment();
         }
         
         @Override
         public int getItemCount() {
             return 5;
         }
     });
     ```
  
  5. Navigation组件:
     ```xml
     <!-- nav_graph.xml -->
     <navigation xmlns:android="http://schemas.android.com/apk/res/android"
                 xmlns:app="http://schemas.android.com/apk/res-auto"
                 android:id="@+id/nav_graph"
                 app:startDestination="@id/homeFragment">
         <fragment
             android:id="@+id/homeFragment"
             android:name="com.example.HomeFragment"
             android:label="Home" />
     </navigation>
     ```

- **你有遇到过哪些关于Fragment的问题，如何处理的？** ⭐⭐⭐

  1. **Fragment重叠问题**:
     - 原因: 设备旋转或Activity重建时，FragmentManager会重新创建Fragment
     - 解决: 在Activity的onCreate中判断savedInstanceState是否为null，仅在null时添加Fragment
  
  2. **状态丢失异常 (IllegalStateException: Can not perform this action after onSaveInstanceState)**:
     - 原因: 在Activity状态保存后执行Fragment事务
     - 解决:
       - 使用commitAllowingStateLoss()替代commit()（不推荐）
       - 确保在合适的生命周期阶段执行事务（如onResumeFragments()或onPostResume()）
       - 使用ViewModel存储UI状态，避免依赖Fragment事务保存状态
  
  3. **Fragment嵌套问题**:
     - 原因: 子Fragment使用错误的FragmentManager
     - 解决: 在子Fragment中使用getChildFragmentManager()而非getParentFragmentManager()
  
  4. **Fragment通信问题**:
     - 原因: 直接引用造成耦合或内存泄漏
     - 解决: 使用ViewModel、接口回调或EventBus等解耦通信方式
  
  5. **屏幕旋转问题**:
     - 原因: Fragment实例重建导致数据丢失
     - 解决:
       - 使用setRetainInstance(true)保留Fragment实例（已弃用）
       - 使用ViewModel保存数据
       - 实现onSaveInstanceState()保存和恢复状态
  
  6. **Fragment回退栈管理复杂**:
     - 原因: 多层嵌套Fragment导致回退栈管理混乱
     - 解决: 使用Navigation组件统一管理导航和回退行为
  
  7. **Fragment懒加载问题**:
     - 原因: ViewPager中的Fragment预加载导致性能问题
     - 解决: 使用setUserVisibleHint()或Fragment的onHiddenChanged()实现懒加载（AndroidX中使用setMaxLifecycle()）

### 12、Binder
- **请介绍什么是Binder机制** ⭐⭐⭐⭐⭐

  Binder是Android系统中的一种进程间通信(IPC)机制，也是Android系统服务的核心基础设施。
  
  核心概念：
  - Binder是一种基于客户端-服务器架构的IPC机制
  - 它同时提供了传输机制和对象引用功能
  - 作为面向对象的RPC(远程过程调用)系统，允许一个进程调用另一个进程的方法
  - 基于mmap内存映射，通过内核空间作为中转站，实现进程间数据传递
  
  Binder的组成部分：
  1. **Binder驱动**: 内核空间的设备驱动，负责进程间Binder通信的建立和数据传递
  2. **ServiceManager**: 核心系统服务，管理所有Binder服务的注册和查询
  3. **IBinder接口**: 定义了Binder通信协议的基本接口
  4. **Binder类**: 实现IBinder接口，提供跨进程通信能力
  
  Binder通信模型中的四个角色：
  - **Server**: 提供服务的进程
  - **Client**: 使用服务的进程
  - **ServiceManager**: 管理各种服务，相当于"通讯录"
  - **Binder驱动**: 负责实际的通信传输，相当于"邮递员"

- **请介绍Binder机制流程** ⭐⭐⭐⭐

  Binder通信的基本流程：
  
  **1. 服务注册**
  - Server创建一个Binder实体对象
  - Server通过Binder驱动向ServiceManager注册服务
  - ServiceManager为服务创建对应的引用并保存在内部表中
  
  **2. 服务获取**
  - Client向ServiceManager查询服务
  - ServiceManager通过Binder驱动将Server的Binder引用返回给Client
  - Client获得引用后可以与Server通信
  
  **3. 远程调用**
  - Client通过持有的Binder引用，构建并发送请求数据
  - Binder驱动接收数据，查找目标进程，将数据从发送方拷贝到内核缓存区
  - Binder驱动通知目标进程有数据到达，目标进程从内核缓存区读取数据
  - Server处理请求，将结果返回给Client，同样经过Binder驱动中转
  
  具体代码层面流程：
  ```
  1. 服务端实现并发布Binder接口：
     - 定义AIDL接口
     - 实现接口中声明的方法
     - 实现onBind()方法返回Binder对象
  
  2. 客户端绑定并使用服务：
     - 通过Context.bindService()绑定服务
     - 在ServiceConnection.onServiceConnected()回调中获取IBinder
     - 通过接口定义的方法调用远程服务
  ```
  
  远程调用的数据流：
  1. Client进程：调用方法 → 打包参数 → 陷入内核态
  2. Binder驱动：处理请求 → 唤醒Server → 数据拷贝到目标进程
  3. Server进程：处理请求 → 处理数据 → 返回结果
  4. Binder驱动：处理返回 → 唤醒Client → 拷贝结果
  5. Client进程：解析结果 → 返回给调用者

- **Binder机制需要多少次内存拷贝** ⭐⭐⭐

  Binder IPC机制涉及的内存拷贝次数为**1次**，这是其高效性的重要原因。
  
  传统IPC内存拷贝过程（如管道、消息队列、共享内存）：
  1. 发送方进程缓冲区 → 内核缓冲区（1次拷贝）
  2. 内核缓冲区 → 接收方进程缓冲区（1次拷贝）
  总计：2次拷贝
  
  Binder IPC内存拷贝过程：
  1. 发送方进程 → 接收方进程映射的内核空间（1次拷贝）
  
  原理解释：
  - Binder基于内存映射（mmap）机制
  - 接收方进程通过mmap映射内核空间一块内存区域到自己的进程空间
  - 发送方将数据拷贝到内核空间的该区域
  - 接收方直接访问映射区域，无需二次拷贝
  
  最佳实践中的注意事项：
  - 虽然只有1次拷贝，但大数据传输仍会影响性能
  - 推荐传递轻量级数据，大数据考虑使用共享内存+Binder通知的方式
  - Binder传输有大小限制（约1MB），超出限制会抛出TransactionTooLargeException

- **Android有很多跨进程通信方法，为何选择Binder？** ⭐⭐⭐

  Android选择Binder作为主要IPC机制的原因：
  
  1. **性能效率高**：
     - 只需一次内存拷贝，比传统IPC（如Socket、管道）少一次拷贝
     - 基于共享内存实现，减少数据传输开销
  
  2. **安全性更好**：
     - 传统IPC无法获得对方可靠身份信息
     - Binder机制中，内核自动记录通信双方的进程UID/PID
     - 服务端可以通过Binder.getCallingUid()获取调用方身份，执行权限校验
  
  3. **稳定性**：
     - 基于C/S架构，职责明确，架构清晰
     - Server端以服务方式运行，生命周期明确，故障率低
  
  4. **面向对象**：
     - 提供了面向对象的接口，更符合Android Java环境
     - 可以将进程间通信转换为对象的远程方法调用
     - 开发使用更自然，无需关注底层细节
  
  5. **可扩展性**：
     - 支持嵌套调用（A→B→C）
     - 支持同步和异步调用模式
     - 支持死亡通知（DeathRecipient）机制
  
  Android其他IPC机制及与Binder对比：
  
  | IPC机制 | 优点 | 缺点 | 适用场景 |
  |---------|------|------|----------|
  | 共享内存 | 零拷贝，速度最快 | 复杂同步，无访问控制 | 高性能大数据传输 |
  | Socket | 通用性强，跨设备 | 传输效率低，API复杂 | 网络通信 |
  | 管道/消息队列 | 简单易用 | 仅支持简单数据，两次拷贝 | 简单命令传递 |
  | 信号 | 轻量级，实时性好 | 只能传递信号值，不能传数据 | 异步通知 |
  | Binder | 一次拷贝，安全性好，面向对象 | 仅限于Android系统 | Android系统服务通信 |
