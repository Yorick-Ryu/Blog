---
title: Kotlin协程
tags:
  - 协程
  - Coroutine
index_img: ./img/image-20221216114040628.png
categories:
  - kotlin
date: 2022-12-15 16:27:41
sticky: 
---


# Kotlin协程

[TOC]

本篇以Android中的Kotlin协程为例

[Android 上的 Kotlin 协程  | Android 开发者  | Android Developers (google.cn)](https://developer.android.google.cn/kotlin/coroutines?hl=zh-cn)

## 协程基本介绍

协程是一项 Kotlin 功能，可将长时间运行的任务（例如数据库或网络访问）的异步回调转换为顺序代码。

为了避免用户在使用您的应用时感觉到任何卡顿，主线程必须[每隔 16 毫秒或更短时间](https://medium.com/androiddevelopers/exceed-the-android-speed-limit-b73a0692abc1)更新一次屏幕，也就是每秒约 60 帧，这个过程中会执行`onDraw()`方法来渲染UI。

下面的代码向网络请求数据。

```kotlin
fun onDataNeeded() {
    val result = networkRequest()
    // Successful network request
    databaseSave(result)
    // Result saved
}
```

但是会阻塞主线程。

![image-20221216112959847](./img/image-20221216112959847.png)

我们可以使用回调函数实现相同的功能，这样不会阻塞。

```kotlin
fun onDataNeeded() {
    // Async callbacks
    networkRequest { result ->
       // Successful network request
       databaseSave(result) { rows ->
         // Result saved
       }
    }
}
```

网络库将在另一个线程上请求网络，当数据准备好时，传递数据或回调到主线程。

![image-20221216112031955](./img/image-20221216112031955.png)

系统使用协程将基于回调的代码转换为顺序代码，我们的网络库仍然使用另一个线程来运行网络。

```kotlin
suspend fun onDataNeeded() {
    // The same code with coroutines
    val result = networkRequest()
    // Successful network request
    databaseSave(result)
    // Result saved
}
```

挂起函数内的代码和普通函数的执行方式不同，它执行每一行代码，直到到达一个调用，这时他会复制当前的状态然后挂起，等待网络请求完成，再恢复保存的状态。

![image-20221216114040628](./img/image-20221216114040628.png)

关键字 `suspend` 是 Kotlin 将函数（即函数类型）标记为可供协程使用的方式。当协程调用标记为 `suspend` 的函数时，它不会像常规函数调用一样在函数返回之前进行阻塞，而是**挂起**执行，直到结果就绪为止，然后从上次停止的位置**恢复**并使用返回的结果。当它挂起并等待结果时，**它会取消阻塞正在运行它的线程**，以便其他函数或协程可以运行。

协程的优点：

- 不用写复杂的回调函数（Replace  callbacks）
- 线程安全（Main safety）

在 Android 上，避免阻塞主线程是非常必要的。主线程是一个处理所有界面更新的线程，也是调用所有点击处理程序和其他界面回调的线程。因此，主线程必须顺畅运行才能确保出色的用户体验。

为了避免用户在使用您的应用时感觉到任何卡顿，主线程必须[每隔 16 毫秒或更短时间](https://medium.com/androiddevelopers/exceed-the-android-speed-limit-b73a0692abc1)更新一次屏幕，也就是每秒约 60 帧。许多常见任务所需的时间都比这个时间长，例如解析大型 JSON 数据集、将数据写入数据库或从网络提取数据。因此，从主线程调用此类代码可能会导致应用暂停、卡顿甚至冻结。如果您阻塞主线程太久，应用甚至可能会崩溃并显示一个**应用无响应**对话框。

## 向项目添加协程

要在 Kotlin 中使用协程，您必须在项目的 `build.gradle (Module: app)` 文件中添加 `coroutines-core` 库。

Android 上的协程作为核心库和 Android 专用扩展函数提供：

- **kotlinx-coroutines-core** - 用于在 Kotlin 中使用协程的主接口
- **kotlinx-coroutines-android** - 在协程中支持 Android 主线程

此初始应用已在 `build.gradle.` 中包含依赖项。创建新的应用项目时，您需要打开 `build.gradle (Module: app)` 并将协程依赖项添加到项目中。

```groovy
dependencies {
  ...
  implementation "org.jetbrains.kotlinx:kotlinx-coroutines-core:x.x.x"
  implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:x.x.x"
}
```

您可以在 [Kotlin 协程版本页面](https://github.com/Kotlin/kotlinx.coroutines/releases)上找到协程库的最新版版本号，以替代“xxx”。

## 回调模式

在不阻塞主线程的情况下执行长时间运行的任务的一种模式是回调。通过使用回调，您可以在后台线程上启动长时间运行的任务。任务完成后，系统会调用回调函数，以在主线程上告知您结果。

我们来看一个回调模式的示例。

```kotlin
// Slow request with callbacks
@UiThread
fun makeNetworkRequest() {
    // The slow network request runs on another thread
    slowFetch { result ->
        // When the result is ready, this callback will get the result
        show(result)
    }
    // makeNetworkRequest() exits after calling slowFetch without waiting for the result
}
```

由于此代码带有 [`@UiThread`](https://developer.android.google.cn/reference/android/support/annotation/UiThread?hl=zh-cn) 注解，因此它必须足够快地运行以在主线程上执行。也就是说，它需要非常快地返回，以便下一次屏幕更新不会出现延迟。不过，由于 `slowFetch` 需要几秒钟甚至几分钟才能完成，因此主线程不能等待结果。`show(result)` 回调允许 `slowFetch` 在后台线程上运行，并在准备就绪后返回结果。

## 使用协程移除回调

回调是一种很好的模式，但也存在缺点。过多使用回调的代码可能会变得难以读取和推演。此外，回调也不允许使用某些语言功能，例如异常。

Kotlin 协程使您能够将基于回调的代码转换为顺序代码。顺序编写的代码通常更易于阅读，甚至可以使用异常等语言功能。

最后，两者所做的事情完全相同：等待长时间运行的任务获得结果，然后继续执行。不过，两者的代码看起来却截然不同。

关键字 `suspend` 是 Kotlin 将函数（即函数类型）标记为可供协程使用的方式。当协程调用标记为 `suspend` 的函数时，它不会像常规函数调用一样在函数返回之前进行阻塞，而是**挂起**执行，直到结果就绪为止，然后从上次停止的位置**恢复**并使用返回的结果。当它挂起并等待结果时，**它会取消阻塞正在运行它的线程**，以便其他函数或协程可以运行。

例如，在下面的代码中，`makeNetworkRequest()` 和 `slowFetch()` 都是 `suspend` 函数。

```kotlin
// Slow request with coroutines
@UiThread
suspend fun makeNetworkRequest() {
    // slowFetch is another suspend function so instead of
    // blocking the main thread  makeNetworkRequest will `suspend` until the result is
    // ready
    val result = slowFetch()
    // continue to execute after the result is ready
    show(result)
}

// slowFetch is main-safe using coroutines
suspend fun slowFetch(): SlowResult { ... }
```

与回调版本一样，`makeNetworkRequest` 必须立即从主线程返回，因为它被标记为 `@UiThread`。这意味着，它通常无法调用 `slowFetch` 等阻塞方法。这里体现了 `suspend` 关键字的神奇之处。

{% note success %}
**重要提示**：`suspend` 关键字不指定运行代码的线程。挂起函数可以在后台线程或主线程上运行。
{% endnote %}


与基于回调的代码相比，协程代码可以利用更少的代码实现取消阻塞当前线程的相同效果。由于它具有顺序样式，因此可以轻松地链接多个长时间运行的任务，而无需创建多个回调。例如，如果代码从两个网络端点提取结果并将结果保存到数据库，则此代码可以编写为协程中的函数，而无需回调。类似以下代码：

```kotlin
// Request data from network and save it to database with coroutines

// Because of the @WorkerThread, this function cannot be called on the
// main thread without causing an error.
@WorkerThread
suspend fun makeNetworkRequest() {
    // slowFetch and anotherFetch are suspend functions
    val slow = slowFetch()
    val another = anotherFetch()
    // save is a regular function and will block this thread
    database.save(slow, another)
}

// slowFetch is main-safe using coroutines
suspend fun slowFetch(): SlowResult { ... }
// anotherFetch is main-safe using coroutines
suspend fun anotherFetch(): AnotherResult { ... }
```

## 了解 CoroutineScope

在 Kotlin 中，所有协程都在 [`CoroutineScope`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.experimental/-coroutine-scope/) 中运行。作用域在其整个作业期间会控制协程的生命周期。如果取消某个作用域的作业，则该作用域内启动的所有协程也将取消。在 Android 上，在一些情况下，例如当用户离开 `Activity` 或 `Fragment` 时，您可以使用作用域取消所有正在运行的协程。作用域还允许您指定默认调度程序。调度程序可以控制哪个线程运行协程。

对于界面启动的协程，通常在 [`Dispatchers.Main`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-main.html)（Android 上的主线程）上启动这类协程是正确的。在 [`Dispatchers.Main`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-main.html) 上启动的协程在挂起期间不会阻塞主线程。由于 `ViewModel` 协程几乎总是在主线程上更新界面，因此在主线程上启动协程可避免额外的线程切换。在主线程上启动的协程可在启动后随时切换调度程序。例如，它可以使用另一个调度程序从主线程外解析大型 JSON 结果。

{% note secondary%}
**协程提供主线程安全**
由于协程可以随时轻松地切换线程并将结果传递回原始线程，因此最好在主线程上启动与界面相关的协程。

使用协程时，[`Room`](https://developer.android.google.cn/jetpack/androidx/releases/room?hl=zh-cn) 和 [`Retrofit`](https://github.com/square/retrofit) 等库原生提供**主线程安全**，因此您无需管理线程来进行网络或数据库调用。这往往能大幅简化代码。

但是，即便使用协程，**阻塞代码**（例如对列表进行排序或从文件读取数据）仍然需要显式代码来创建**主线程安全**。如果您使用的网络或数据库（还）不支持协程，情况也是如此。
{% endnote %}

Kotlin 协程默认提供三个调度程序：[`Main`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-main.html)、[`IO`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-i-o.html) 和 [`Default`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html)。IO 调度程序针对 IO 工作进行了优化，例如从网络或磁盘读取内容，而 Default 调度程序则针对 CPU 密集型任务进行了优化。
