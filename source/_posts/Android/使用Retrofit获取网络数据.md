---
title: 安卓使用Retrofit获取网络数据
tags:
  - Retrofit
index_img: /img/default.png
categories:
  - Android
date: 2023-01-17 14:33:39
sticky:
---

# 使用Retrofit获取网络数据

参考：[从互联网获取数据 (google.cn)](https://developer.android.google.cn/codelabs/basic-android-kotlin-compose-getting-data-internet)

Retrofit官方文档：[Retrofit (square.github.io)](https://square.github.io/retrofit/)

## 添加Retrofit依赖项

Android Gradle 允许您将外部库添加到项目中。除了库依赖项之外，您还需要添加托管库的代码库。

1. 打开模块级 Gradle 文件 `build.gradle` `(Module: MarsPhotos.app)`。

2. 在 `dependencies` 部分，为 Retrofit 库添加以下几行代码：

   ```groovy
   // Retrofit
   implementation "com.squareup.retrofit2:retrofit:2.9.0"
   // Retrofit with Scalar Converter
   implementation "com.squareup.retrofit2:converter-scalars:2.9.0"
   ```

这两个库协同工作。第一个依赖项用于 Retrofit 2 库本身，而第二个依赖项则用于 Retrofit 标量转换器。Retrofit2 是 Retrofit 库的更新版本。此标量转换器允许 Retrofit 将 JSON 结果作为 `String` 返回。

## 添加数据层

添加一个数据层，供 `ViewModel` 用来与网络服务通信。您将按照以下步骤实现 Retrofit 服务 API。

- 创建一个数据源：`XxxxApiService` 类。
- 使用基准网址和转换器工厂创建 Retrofit 对象，以转换字符串。
- 创建一个可说明 Retrofit 如何与网络服务器通信的接口。
- 创建一个 Retrofit 服务，并向应用的其余 API 服务公开实例。

示例：

1. 右键点击 Android 项目窗格中的 `com.example.android.marsphotos` 软件包，然后依次选择 **New > Package**。
2. 在弹出式窗口中，将 **network** 附加到建议软件包名称的末尾。
3. 在新软件包“network”下创建新的 Kotlin 文件。将该文件命名为 `MarsApiService`。
4. 打开 `network/MarsApiService.kt`。
5. 为网络服务的基准网址添加以下常量。

    ```kotlin
    private const val BASE_URL =
       "https://android-kotlin-fun-mars-server.appspot.com"
    ```

6. 在该常量正下方添加 Retrofit 构建器，用于构建和创建 Retrofit 对象。

    ```kotlin
    import retrofit2.Retrofit
    
    private val retrofit = Retrofit.Builder()
    ```

Retrofit 需要网络服务的基本 URI 和转换器工厂来构建网络服务 API。转换器会告知 Retrofit 如何处理它从网络服务获取的数据。在这种情况下，您需要 Retrofit 从网络服务提取 JSON 响应，并将该响应作为 `String` 返回。Retrofit 包含一个 `ScalarsConverter`，它支持字符串和其他基元类型。

7. 使用 `ScalarsConverterFactory` 实例对构建器调用 `addConverterFactory()`。

    ```kotlin
    import retrofit2.converter.scalars.ScalarsConverterFactory

    private val retrofit = Retrofit.Builder()
       .addConverterFactory(ScalarsConverterFactory.create())
    ```

8. 使用 `baseUrl()` 方法为网络服务添加基准网址。
9. 调用 `build()` 以创建 Retrofit 对象。

    ```kotlin
    private val retrofit = Retrofit.Builder()
       .addConverterFactory(ScalarsConverterFactory.create())
       .baseUrl(BASE_URL)
       .build()
    ```

10. 在对 Retrofit 构建器的调用的下方，定义一个名为 `MarsApiService` 的接口，该接口定义 Retrofit 如何使用 HTTP 请求与网络服务器通信。

    ```kotlin
    interface MarsApiService {
    }
    ```

11. 向 `MarsApiService` 接口添加一个名为 `getPhotos()` 的函数，以从网络服务中获取响应字符串。

    ```kotlin
    interface MarsApiService {
        fun getPhotos()
    }
    ```

12. 使用 `@GET` 注解告知 Retrofit 这是 GET 请求，并为该网络服务方法指定端点。在这种情况下，端点为 `photos`。如上个任务中所述，您将在此 Codelab 中使用 [/photos](https://android-kotlin-fun-mars-server.appspot.com/photos) 端点。

    ```kotlin
    import retrofit2.http.GET
    
    interface MarsApiService {
        @GET("photos")
        fun getPhotos()
    }
    ```

调用 `getPhotos()` 方法时，Retrofit 会将端点 `photos` 附加到您用于启动请求的基准网址（由您在 Retrofit 构建器中定义）。

13. 将函数的返回值类型添加到 `String`。

    ```kotlin
    interface MarsApiService {
        @GET("photos")
        fun getPhotos(): String
    }
    ```

14. 创建MarsApi对象

    ```kotlin
    object MarsApi {
        val retrofitService: MarsApiService by lazy {
            retrofit.create(MarsApiService::class.java)
        }
    }
    ```

## 在 ViewModel 中调用网络服务

前提：使用ViewModel管理状态。

### ViewModelScope

[`viewModelScope`](https://developer.android.google.cn/topic/libraries/architecture/coroutines#viewmodelscope) 是为应用中的每个 `ViewModel` 定义的内置协程作用域。在此作用域内启动的协程会在 `ViewModel` 被清除时自动取消。

您可以使用 `viewModelScope` 启动协程，并在后台发出网络服务请求。由于 `viewModelScope` 属于 `ViewModel`，因此，即使应用发生配置更改，请求也会继续发出。

1. 在 `MarsApiService.kt` 文件中，将 `getPhotos()` 设置为挂起函数，使其异步，并且不会阻塞发起调用的线程。您可以从 [`viewModelScope`](https://developer.android.google.cn/topic/libraries/architecture/coroutines#viewmodelscope) 内调用此函数。

    ```kotlin
    @GET("photos")
    suspend fun getPhotos(): String
    ```

2. 打开 `ui/screens/MarsViewModel.kt` 文件。向下滚动到 `getMarsPhotos()` 方法。删除用于将状态响应设置为 `"Set the Mars API Response here!"` 的代码行，使 `getMarsPhotos()` 方法为空。

    ```kotlin
    private fun getMarsPhotos() {}
    ```

3. 在 `getMarsPhotos()` 中，使用 `viewModelScope.launch` 启动协程。

    ```kotlin
    import androidx.lifecycle.viewModelScope
    import kotlinx.coroutines.launch

    fun getMarsPhotos() {
        viewModelScope.launch {}
    }
    ```

4. 在 `viewModelScope` 中，使用单例对象 `MarsApi` 从 `retrofitService` 接口调用 `getPhotos()` 方法。将返回的响应保存在名为 `listResult` 的 `val` 中。

    ```kotlin
    import com.example.marsphotos.network.MarsApi

    viewModelScope.launch {
        val listResult = MarsApi.retrofitService.getPhotos()
    }
    ```

5. 将刚刚从后端服务器收到的结果分配给 `marsUiState`。`marsUiState` 是一个可变状态对象，表示最近的网络请求的状态。

    ```kotlin
    val listResult = MarsApi.retrofitService.getPhotos()
    marsUiState = listResult
    ```

6. 运行应用。请注意，该应用会立即关闭，不一定会显示错误弹出窗口。应用发生了崩溃。
7. 点击 Android Studio 中的 **Logcat** 标签页，并记下日志中以如下所示的代码行开头的错误消息：“`------- beginning of crash`”。

    ```kotlin
        --------- beginning of crash
    22803-22865/com.example.android.marsphotos E/AndroidRuntime: FATAL EXCEPTION: OkHttp Dispatcher
        Process: com.example.android.marsphotos, PID: 22803
        java.lang.SecurityException: Permission denied (missing INTERNET permission?)
    ...
    ```

此错误消息表示应用可能缺少 `INTERNET` 权限。下一步添加互联网权限并解决此问题。

## 添加互联网权限和异常处理

应用需要 `INTERNET` 权限才能访问互联网。

### 添加互联网权限

在 `AndroidManifest.xml` 文件中添加 `<uses-permission>` 标签来声明它所需的权限。

1. 打开 `manifests/AndroidManifest.xml`。将下面这行代码添加到 `<application>` 标签的前面：

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

2. 编译并再次运行应用。

### **异常处理**

如果没有进行异常处理，执行以下步骤，应用会崩溃：

1. 将设备或模拟器设为飞行模式，以模拟网络连接错误。

2. 从“最近”菜单中重新打开应用，或从 Android Studio 中重启应用。

3. 点击 Android Studio 中的 **Logcat** 标签页，并记下日志中如下所示的严重异常：

   ```
   3302-3302/com.example.android.marsphotos E/AndroidRuntime: FATAL EXCEPTION: main
       Process: com.example.android.marsphotos, PID: 3302
   ```

此错误消息表示应用尝试连接并超时。在现实环境中，诸如此类的异常非常常见。与权限问题不同，此错误无法解决，但您可以自行处理。在下一步中，您将了解如何处理此类异常。

连接到服务器时可能出现的问题包括：

- 在 API 中使用的网址或 URI 不正确。
- 服务器不可用，应用无法连接到服务器。
- 网络延迟问题。
- 设备的互联网连接状况不佳或无互联网连接。

这些异常无法在编译时进行处理，但您可以使用 `try-catch` 代码块在运行时处理异常。

在 `try` 代码块中，您可以在预期会引发异常的位置添加代码。在您的应用中，这会是一次网络调用。在 `catch` 代码块中，您需要实现用于防止应用突然终止的代码。如果存在异常，系统会执行 `catch` 代码块，以从错误中恢复，而不是突然终止应用。

1. 在 `getMarsPhotos()` 中的 `launch` 代码块内，围绕 `MarsApi` 调用添加一个 `try` 代码块来处理异常。
2. 在 `try` 代码块之后添加一个 `catch` 代码块。

    ```kotlin
    viewModelScope.launch {
       try {
           val listResult = MarsApi.retrofitService.getPhotos()
           marsUiState = listResult
       } catch (e: IOException) {

       }
    }
    ```

1. 再次运行该应用。请注意，应用这次不会崩溃。

### 添加状态界面

在 `MarsViewModel` 类中，最近的网络请求的状态 `marsUiState` 会保存为可变状态对象。但是，这个类缺乏保存如下不同状态的功能：正在加载、成功和失败。

- **Loading**状态表示应用正在等待数据。
- **Success**状态表示已成功从网络服务检索到数据。
- **Error**状态表示存在网络或连接错误。

如需表示应用中的这三种状态，您将使用封装接口。`sealed interface` 通过限制可能的值来轻松管理状态。在 Mars Photos 应用中，您将 `marsUiState` 网络响应限制为三种状态（数据类对象）：正在加载、成功和错误，如以下代码所示：

```kotlin
// No need to copy over
sealed interface MarsUiState {
   data class Success : MarsUiState
   data class Loading : MarsUiState
   data class Error : MarsUiState
}
```

在上述代码段中，如果返回成功响应，您会从服务器收到火星照片信息。为了存储数据，请向 `Success` 数据类添加一个构造函数参数。

对于 `Loading` 和 `Error` 状态，您无需设置新数据和创建新对象；只需传递网络响应即可。将 `data` 类更改为 `Object`，以便为网络响应创建对象。

1. 打开 `ui/MarsViewModel.kt` 文件。在 import 语句后，添加 `MarsUiState` 封装接口。添加后，`MarsUiState` 对象的值就会变得详尽。

   ```kotlin
   sealed interface MarsUiState {
       data class Success(val photos: String) : MarsUiState
       object Error : MarsUiState
       object Loading : MarsUiState
   }
   ```

2. 在 `MarsViewModel` 类中，更新 `marsUiState` 定义。将类型更改为 `MarsUiState`，将 `MarsUiState.Loading` 作为其默认值。将 setter 设为不公开，以保护写入 `marsUiState` 的内容。

   ```kotlin
   var marsUiState: MarsUiState by mutableStateOf(MarsUiState.Loading)
     private set
   ```

3. 向下滚动到 `getMarsPhotos()` 方法。将 `marsUiState` 值更新为 `MarsUiState.Success`，并传递 `listResult`。

   ```kotlin
   val listResult = MarsApi.retrofitService.getPhotos()
   marsUiState = MarsUiState.Success(listResult)
   ```

4. 在 `catch` 代码块内部，处理故障响应。将 `MarsUiState` 设为 `Error`。

   ```kotlin
   catch (e: IOException) {
      marsUiState = MarsUiState.Error
   }
   ```

5. 您可以从 `try-catch` 代码块中取出 `marsUiState` 分配。完成后的函数应如以下代码所示：

   ```kotlin
   private fun getMarsPhotos() {
      viewModelScope.launch {
          marsUiState = try {
              val listResult = MarsApi.retrofitService.getPhotos()
              MarsUiState.Success(listResult)
          } catch (e: IOException) {
              MarsUiState.Error
          }
      }
   }
   ```

6. 在 `screens/HomeScreen.kt` 文件中，对 `marsUiState` 添加一个 `when` 表达式。如果 `marsUiState` 为 `MarsUiState.Success`，则调用 `ResultScreen` 并传入 `marsUiState.photos`。现阶段，请忽略错误。

   ```kotlin
   fun HomeScreen(
      marsUiState: MarsUiState,
      modifier: Modifier = Modifier
   ) {
       when (marsUiState) {
           is MarsUiState.Success -> ResultScreen(marsUiState.photos, modifier)
       }
   }
   ```

   <p class="note note-success">注意：marsUiState 属性不再是字符串。您已将其更改为 MarsUiState 封装接口，该接口有三个不同的对象值：MarsUiState.Loading、MarsUiState.Success 和 MarsUiState.Error。</p>

7. 在 `when` 代码块内，为 `MarsUiState.Loading` 和 `MarsUiState.Error` 添加检查项。让该应用显示 `LoadingScreen`、`ResultScreen` 和 `ErrorScreen` 可组合项，稍后您会实现这些可组合项。

   ```kotlin
   fun HomeScreen(
      marsUiState: MarsUiState,
      modifier: Modifier = Modifier
   ) {
       when (marsUiState) {
           is MarsUiState.Loading -> LoadingScreen(modifier)
           is MarsUiState.Success -> ResultScreen(marsUiState.photos, modifier)
           is MarsUiState.Error -> ErrorScreen(modifier)
       }
   }
   ```

   <p class="note note-success">如果实现 MarsUiState interface 时未使用 sealed 关键字，则需要添加一个 Success、Error、Loading 和 else 分支。由于没有第四个选项 (else)，因此，您可以使用 sealed 接口告知编译器只有三个选项（这会使条件语句变得详尽）</p>

8. 打开 `res/drawable/loading_animation.xml`。该可绘制对象是围绕中心点旋转图片可绘制对象 `loading_img.xml` 的动画。（您在预览中看不到这段动画。）

   ![loading.png](./img/92a448fa23b6d1df.png)

9. 在 `screens/HomeScreen.kt` 文件中的 `HomeScreen` 可组合项下方，添加以下 `LoadingScreen` 可组合函数以显示加载动画。起始代码中包含 `loading_img` 可绘制资源。

   ```kotlin
   import androidx.compose.ui.res.painterResource
   import androidx.compose.ui.unit.dp
   import androidx.compose.foundation.layout.size
   import androidx.compose.foundation.Image
   
   @Composable
   fun LoadingScreen(modifier: Modifier = Modifier) {
       Box(
           contentAlignment = Alignment.Center,
           modifier = modifier.fillMaxSize()
       ) {
           Image(
               modifier = Modifier.size(200.dp),
               painter = painterResource(R.drawable.loading_img),
               contentDescription = stringResource(R.string.loading)
           )
       }
   }
   ```

10. 在 `LoadingScreen` 可组合项下方，添加以下 `ErrorScreen` 可组合函数，以便应用显示错误消息。

    ```kotlin
    @Composable
    fun ErrorScreen(modifier: Modifier = Modifier) {
        Box(
            contentAlignment = Alignment.Center,
            modifier = modifier.fillMaxSize()
        ) {
            Text(stringResource(R.string.loading_failed))
        }
    }
    ```

11. 再次运行应用，保持飞行模式开启状态。应用这次不会突然关闭，而是会显示错误消息：

12. 在手机或模拟器上，关闭飞行模式。运行并测试您的应用，确保一切正常，并且您能够看到 JSON 字符串。

## 使用 kotlinx.serialization 解析 JSON 响应

### 添加 `kotlinx.serialization` 依赖项

1. 打开 **build.gradle (Module: app)**。

2. 在 `plugins` 代码块中，添加 `kotlinx serialization` 插件。

      ```groovy
      id 'org.jetbrains.kotlin.plugin.serialization' version '1.7.10'
      ```

      

3. 在“dependencies”部分，添加以下代码以包含 `kotlinx.serialization` 依赖项。此依赖项可为 Kotlin 项目提供 JSON 序列化。

      ```groovy
      // Kotlin serialization
      implementation "org.jetbrains.kotlinx:kotlinx-serialization-json:1.4.1"
      ```

4. 在 `dependencies` 代码块中，找到 Retrofit 标量转换器所在的代码行，并将其更改为使用 `kotlinx-serialization-converter`：

   **将以下代码**

   ```groovy
   // Retrofit with scalar Converter
   implementation "com.squareup.retrofit2:converter-scalars:2.9.0"
   ```

   **替换为以下代码**

   ```groovy
   // Retrofit with Kotlin serialization Converter
   implementation "com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:0.8.0"
   ```

5. 点击 **Sync Now**，以使用新的依赖项重建项目。

### 实现数据类

例如：

您从网络服务中获取的 JSON 响应的示例条目类似于您之前看到的内容：

```json
[
    {
        "id":"424906",
        "img_src":"http://mars.jpl.nasa.gov/msl-raw-images/msss/01000/mcam/1000ML0044631300305227E03_DXXX.jpg"
    },
...]
```

请注意，在上面的示例中，每个火星照片条目都具有以下 JSON 键值对：

- `id`：资源的 ID，用字符串表示。由于它封装在英文引号 (`" "`) 中，因此它是 `String` 类型，而不是 `Integer`。
- `img_src`：图片的网址，用字符串表示。

kotlinx.serialization 会解析此 JSON 数据并将其转换为 Kotlin 对象。为此，kotlinx.serialization 需要一个 Kotlin 数据类来存储解析后的结果。在此步骤中，您将创建数据类 `MarsPhoto`。

1. 右键点击 **network** 软件包，然后依次选择 **New > Kotlin File/Class**。

2. 在对话框中，选择 **Class**，然后输入 `MarsPhoto` 作为类的名称。系统将在 `network` 软件包中创建一个名为 `MarsPhoto.kt` 的新文件。

3. 在类定义前添加 `data` 关键字，使 `MarsPhoto` 成为数据类。

4. 将英文大括号 `{}` 更改为英文圆括号 `()`。此更改会引发错误，因为数据类必须至少定义一个属性。

   ```kotlin
   data class MarsPhoto()
   ```

5. 将以下属性添加到 `MarsPhoto` 类定义中。

   ```kotlin
   data class MarsPhoto(
       val id: String,  val img_src: String
   )
   ```

6. 使 `MarsPhoto` 类可序列化，并为其添加 `@Serializable` 注解。

   ```kotlin
   import kotlinx.serialization.Serializable
   
   @Serializable
   data class MarsPhoto(
       val id: String,  val img_src: String
   )
   ```

   请注意，`MarsPhoto` 类中的每个变量都对应于 JSON 对象中的一个键名。为了匹配特定 JSON 响应中的类型，您可以为所有值使用 `String` 对象。

   `kotlinx serialization` 解析 JSON 时，它会按名称匹配键，并用适当的值填充数据对象。

**@SerialName 注解**

有时，JSON 响应中的键名可能会使 Kotlin 属性混淆，或者可能与建议的编码样式不匹配。例如，在 JSON 文件中，`img_src` 键使用下划线，而 Kotlin 惯例使用大写和小写字母（“驼峰式大小写”）。

如需在数据类中使用与 JSON 响应中的键名不同的变量名称，请使用 `@SerialName` 注解。在以下示例中，数据类中变量的名称为 `imgSrc`。可以使用 `@SerialName(value = "img_src")` 将该变量映射到 JSON 属性 `img_src`。

1. 将 `img_src` 键所在的代码行替换为如下所示的代码行。

   ```kotlin
   import kotlinx.serialization.SerialName
   
   @SerialName(value = "img_src")
   val imgSrc: String
   ```

### 更新 MarsApiService 和 MarsViewModel

在此任务中，您将使用 `kotlinx.serialization` 转换器将 JSON 对象转换为 Kotlin 对象。

1. 打开 `network/MarsApiService.kt`。

2. 请注意 `ScalarsConverterFactory` 的未解析引用错误。这些错误是由上一部分中的 Retrofit 依赖项更改导致的。

3. 删除 `ScalarConverterFactory` 的导入作业。

    ```kotlin
    import retrofit2.converter.scalars.ScalarsConverterFactory
    ```

4. 在 `retrofit` 对象声明中，将 Retrofit 构建器更改为使用 `kotlinx.serialization` 而不是 `ScalarConverterFactory`。

   ```kotlin
   import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
   import kotlinx.serialization.json.Json
   import okhttp3.MediaType
   
   private val retrofit = Retrofit.Builder()
       .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
       .baseUrl(BASE_URL)
       .build()
   // 这里我一直引入失败，改为了：Json.asConverterFactory(MediaType.get("application/json"))
   ```
   **如果`toMediaType()`报错**：
    在`build.gradle(app)`的`dependencies`中导入okhttp3依赖并同步.

    ```groovy
    dependencies {
    ...
    implementation "com.squareup.okhttp3:okhttp:4.10.1"
    }
    ```
    就可以使用了：
    ```kotlin
    import okhttp3.MediaType.Companion.toMediaType
   
    val contentType = "application/json".toMediaType()
    ```

现在，您已具备 `kotlinx.serialization`，可以要求 Retrofit 从 JSON 数组中返回 `MarsPhoto` 对象列表，而不是返回 JSON 字符串。

5. 更新 `MarsApiService` 接口，以便 Retrofit 返回 `MarsPhoto` 对象列表，而不是返回 `String`。

   ```kotlin
   interface MarsApiService {
       @GET("photos")
       suspend fun getPhotos(): List<MarsPhoto>
   }
   ```

6. 对 `viewModel` 进行类似的更改。打开 `MarsViewModel.kt`，并向下滚动到 `getMarsPhotos()` 方法。

   在 `getMarsPhotos()` 方法中，`listResult` 是 `List<MarsPhoto>`，而不再是 `String`。该列表的大小就是已接收和解析的照片数。

7. 如需输出检索的照片数，请按如下方式更新 `marsUiState`：

   ```kotlin
   val listResult = MarsApi.retrofitService.getPhotos()
   marsUiState = MarsUiState.Success(
      "Success: ${listResult.size} Mars photos retrieved"
   )
   ```

8. 确保在设备或模拟器中关闭飞行模式，编译并运行应用。

   这一次，消息应显示网络服务返回的资源数，而不是较大的 JSON 字符串。

示例应用完整代码：

[google-developer-training/basic-android-kotlin-compose-training-mars-photos: Solution code for Android Basics in Kotlin course (github.com)](https://github.com/google-developer-training/basic-android-kotlin-compose-training-mars-photos)

## 总结

### REST 网络服务

- 网络服务是通过互联网提供的基于软件的功能，可让您的应用发出请求并获取返回的数据。
- 常见网络服务使用的是 [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) 架构。提供 REST 架构的网络服务称为 RESTful 服务。RESTful 网络服务是使用标准网络组件和协议构建的。
- 您可通过 URI 以标准化方式向 REST 网络服务发出请求。
- 若要使用网络服务，应用必须建立网络连接，然后与该服务进行通信。然后，应用必须接收响应数据，并将该数据解析成应用可以使用的格式。
- [Retrofit](https://square.github.io/retrofit/) 库是一个客户端库，可让应用向 REST 网络服务发出请求。
- 使用转换器指示 Retrofit 如何处理它发送至网络服务的数据，以及它从网络服务获取的返回数据。例如，`ScalarsConverter` 会将网络服务数据视为 `String` 或其他基元。
- 如需让应用能够连接到互联网，请在 Android 清单中添加 `"android.permission.INTERNET"` 权限。
- 延迟初始化会将对象创建操作委派为在首次使用时执行。它会创建引用，但不会创建对象。在首次访问对象后，此后每次访问都会创建并使用引用。

### JSON 解析

- 网络服务的响应通常会采用 [JSON](https://www.json.org/) 格式（一种表示结构化数据的通用格式）。
- JSON 对象是键值对的集合。
- JSON 对象集合是一个 JSON 数组。作为网络服务的响应，您会得到一个 JSON 数组。
- 键值对中的键会用英文引号引起来。值可以是数字或字符串。
- 在 Kotlin 中，数据序列化工具位于单独的组件 [kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization) 中。kotlinx.serialization 提供了一系列库，用于将 JSON 字符串转换为 Kotlin 对象。
- Kotlin 序列化转换器库是一个社区开发的库，适用于 Retrofit：[retrofit2-kotlinx-serialization-converter](https://github.com/JakeWharton/retrofit2-kotlinx-serialization-converter#kotlin-serialization-converter)。
- kotlinx.serialization 可将 JSON 响应中的键与具有相同名称的数据对象中的属性进行匹配。
- 如需为键使用不同的属性名称，请使用 `@Serializable` 注解和 JSON 键 `value` 为该属性添加注解。
