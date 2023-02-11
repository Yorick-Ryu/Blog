---
title: Android使用Proto_DataStore
tags:
  - DataStore
  - Jetpack
index_img: /img/android-jetpack.svg
categories:
  - Android
date: 2023-01-28 19:02:05
sticky:
---

# 使用Proto DataStore存储数据

摘自：

[应用架构：数据层 - DataStore - Android 开发者  | Android Developers](https://developer.android.com/topic/libraries/architecture/datastore?hl=zh-cn)

[使用 Proto DataStore  | Android Developers](https://developer.android.com/codelabs/android-proto-datastore?hl=zh-cn)

## **什么是 DataStore？**

DataStore 是经过改进的新版数据存储解决方案，旨在取代 SharedPreferences。DataStore 基于 Kotlin 协程和 Flow 构建，提供以下两种不同的实现：**Proto DataStore**，用于存储**类型化对象**（由[协议缓冲区](https://developers.google.com/protocol-buffers?hl=zh-cn)支持）；**Preferences DataStore**，用于存储**键值对**。DataStore 以异步、一致的事务方式存储数据，克服了 SharedPreferences 的一些缺点。

## DataStore - 基础知识 

您可能经常需要存储较小或简单的数据集。为此，您过去可能使用过 SharedPreferences，但此 API 也存在一系列缺点。Jetpack DataStore 库旨在解决这些问题，从而创建一个简单、安全性更高的异步 API 来存储数据。它提供 2 种不同的实现：

- Preferences DataStore
- Proto DataStore

| **功能**                             | **SharedPreferences**                                        | **PreferencesDataStore**                       | **ProtoDataStore**                                           |
| ------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------ |
| 异步 API                             | ✅（仅用于通过[监听器](https://developer.android.com/reference/android/content/SharedPreferences.OnSharedPreferenceChangeListener?hl=zh-cn)读取已更改的值） | ✅（通过 `Flow` 以及 RxJava 2 和 3 `Flowable`） | ✅（通过 `Flow` 以及 RxJava 2 和 3 `Flowable`）               |
| 同步 API                             | ✅（但无法在界面线程上安全调用）                              | ❌                                              | ❌                                                            |
| 可在界面线程上安全调用               | ❌(1)                                                         | ✅（这项工作已在后台移至 `Dispatchers.IO`）     | ✅（这项工作已在后台移至 `Dispatchers.IO`）                   |
| 可以提示错误                         | ❌                                                            | ✅                                              | ✅                                                            |
| 不受运行时异常影响                   | ❌(2)                                                         | ✅                                              | ✅                                                            |
| 包含一个具有强一致性保证的事务性 API | ❌                                                            | ✅                                              | ✅                                                            |
| 处理数据迁移                         | ❌                                                            | ✅                                              | ✅                                                            |
| 类型安全                             | ❌                                                            | ❌                                              | ✅ 使用[协议缓冲区](https://developers.google.com/protocol-buffers?hl=zh-cn) |

(1) SharedPreferences 有一个看上去可以在界面线程中安全调用的同步 API，但是该 API 实际上执行磁盘 I/O 操作。此外，`apply()` 会阻断 `fsync()` 上的界面线程。每次有服务启动或停止以及每次 activity 在应用中的任何地方启动或停止时，系统都会触发待处理的 `fsync()` 调用。界面线程在 `apply()` 调度的待处理 `fsync()` 调用上会被阻断，这通常会导致 [ANR](https://developer.android.com/topic/performance/vitals/anr?hl=zh-cn)。

(2) SharedPreferences 会将解析错误作为运行时异常抛出。

### **Preferences DataStore 与 Proto DataStore**

虽然 Preferences DataStore 和 Proto DataStore 都允许保存数据，但它们保存数据的方式不同：

- 与 SharedPreferences 一样，**Preferences DataStore** 根据键访问数据，而无需事先定义架构。
- **Proto DataStore** 使用[协议缓冲区](https://developers.google.com/protocol-buffers?hl=zh-cn)来定义架构。使用协议缓冲区可**持久保留强类型数据**。与 XML 和其他类似的数据格式相比，协议缓冲区速度更快、规格更小、使用更简单，并且更清楚明了。虽然使用 Proto DataStore 需要学习新的序列化机制，但我们认为 Proto DataStore 有着强大的类型优势，值得学习。

### **Room 与 DataStore**

如果您需要实现部分更新、引用完整性或大型/复杂数据集，您应考虑使用 Room，而不是 DataStore。DataStore 非常适合小型或简单的数据集，但不支持部分更新或引用完整性。

## Proto DataStore - 概览 

SharedPreferences 和 Preferences DataStore 的一个缺点是无法定义架构，保证不了存取键时使用了正确的数据类型。Proto DataStore 可利用[协议缓冲区](https://developers.google.com/protocol-buffers?hl=zh-cn)定义架构来解决此问题。通过使用协议，DataStore 可以知道存储的类型，并且无需使用键便能提供类型。

## **添加依赖项**

为了使用 Proto DataStore，让协议缓冲区为我们的架构生成代码，我们需要对 build.gradle 文件进行一些更改：

- 添加协议缓冲区插件
- 添加协议缓冲区和 Proto DataStore 依赖项
- 配置协议缓冲区

```groovy
plugins {
    ...
    id "com.google.protobuf" version "0.8.17"
}

dependencies {
    implementation  "androidx.datastore:datastore-core:1.0.0"
    implementation  "com.google.protobuf:protobuf-javalite:3.18.0"
    ...
}

protobuf {
    protoc {
        artifact = "com.google.protobuf:protoc:3.14.0"
    }

    // Generates the java Protobuf-lite code for the Protobufs in this project. See
    // https://github.com/google/protobuf-gradle-plugin#customizing-protobuf-compilation
    // for more information.
    generateProtoTasks {
        all().each { task ->
            task.builtins {
                java {
                    option 'lite'
                }
            }
        }
    }
}
```

## 使用Proto DataStore

### 定义架构

#### 定义和使用 protobuf 对象 

协议缓冲区是一种对结构化数据进行序列化的机制。您只需对数据结构化的方式进行一次定义，编译器便会生成源代码，轻松写入和读取结构化数据。

#### **创建 proto 文件**

您可以在 proto 文件中定义架构。在此 Codelab 中，我们有两个用户偏好设置：`show_completed` 和 `sort_order`；目前两者以两种不同的对象来表示。因此，我们的一个目标是将这两个标志统一到存储在 DataStore 中的一个 `UserPreferences` 类下。我们将在协议缓冲区架构而非 Kotlin 中定义该类。

请查看 [Proto 语言指南](https://developers.google.com/protocol-buffers/docs/overview?hl=zh-cn)，深入了解关于语法的信息。在此 Codelab 中，我们仅关注我们需要使用的类型。

在 `app/src/main/proto` 目录中创建一个名为 `user_prefs.proto` 的新文件。如果您未看到此文件夹结构，请切换到**项目视图**。在协议缓冲区中，每个结构都使用一个 `message` 关键字进行定义，并且结构中的每一个成员都会根据类型和名称在消息内进行定义，从而获得从 1 开始的排序。

示例：

```protobuf
syntax = "proto3";

option java_package = "com.example.application";
option java_multiple_files = true;

message Settings {
  int32 example_counter = 1;
}
```

<p class="note note-warning">注意：您的存储对象的类在编译时由 proto 文件中定义的 message 生成。请务必重新构建您的项目。</p>

### 创建 Proto DataStore

创建 Proto DataStore 来存储类型化对象涉及两个步骤：

1. 定义一个实现 `Serializer<T>` 的类，其中 `T` 是 proto 文件中定义的类型。此序列化器类会告知 DataStore 如何读取和写入您的数据类型。请务必为该序列化器添加默认值，以便在尚未创建任何文件时使用。
2. 使用由 `dataStore` 创建的属性委托来创建 `DataStore<T>` 的实例，其中 `T` 是在 proto 文件中定义的类型。在您的 Kotlin 文件顶层调用该实例一次，便可在应用的所有其余部分通过此属性委托访问该实例。`filename` 参数会告知 DataStore 使用哪个文件存储数据，而 `serializer` 参数会告知 DataStore 第 1 步中定义的序列化器类的名称。

```kotlin
object SettingsSerializer : Serializer<Settings> {
  override val defaultValue: Settings = Settings.getDefaultInstance()

  override suspend fun readFrom(input: InputStream): Settings {
    try {
      return Settings.parseFrom(input)
    } catch (exception: InvalidProtocolBufferException) {
      throw CorruptionException("Cannot read proto.", exception)
    }
  }

  override suspend fun writeTo(
    t: Settings,
    output: OutputStream) = t.writeTo(output)
}

val Context.settingsDataStore: DataStore<Settings> by dataStore(
  fileName = "settings.pb",
  serializer = SettingsSerializer
)
```

### 从 Proto DataStore 读取内容

使用 `DataStore.data` 显示所存储对象中相应属性的 `Flow`。

```kotlin
val exampleCounterFlow: Flow<Int> = context.settingsDataStore.data
  .map { settings ->
    // The exampleCounter property is generated from the proto schema.
    settings.exampleCounter
  }
```

### 将内容写入 Proto DataStore

Proto DataStore 提供了一个 [`updateData()`](https://developer.android.com/reference/kotlin/androidx/datastore/core/DataStore?hl=zh-cn#updatedata) 函数，用于以事务方式更新存储的对象。`updateData()` 为您提供数据的当前状态，作为数据类型的一个实例，并在原子读-写-修改操作中以事务方式更新数据。

```kotlin
suspend fun incrementCounter() {
  context.settingsDataStore.updateData { currentSettings ->
    currentSettings.toBuilder()
      .setExampleCounter(currentSettings.exampleCounter + 1)
      .build()
    }
}
```

## 扩展

[在同步代码中使用 DataStore](https://developer.android.com/topic/libraries/architecture/datastore?hl=zh-cn#synchronous)

[在多进程代码中使用 DataStore](https://developer.android.com/topic/libraries/architecture/datastore?hl=zh-cn#multiprocess)
