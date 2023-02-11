---
title: Compose中的状态
index_img: ./img/f415ca9336d83142.png
categories: 
  - Android
date: 2022-12-08 15:38:04
tags: 
  - Jetpack
  - Compose
sticky: 
---

# Compose中的状态

应用的“状态”是指可以随时间变化的任何值。这是一个非常宽泛的定义，从 [Room](https://developer.android.com/jetpack/androidx/releases/room) 数据库到类的变量，全部涵盖在内。

所有 Android 应用都会向用户显示状态。下面是 Android 应用中的一些状态示例：

- 聊天应用中最新收到的消息。
- 用户的个人资料照片。
- 在项列表中的滚动位置。

**关键提示**：状态决定界面在任何特定时间的显示内容。

优秀实践是为所有可组合函数提供默认的 [`Modifier`](https://developer.android.com/reference/kotlin/androidx/compose/ui/Modifier)，从而提高可重用性。它应作为第一个可选参数显示在参数列表中，位于所有必需参数之后。

“状态”是指可以随时间变化的任何值，例如，聊天应用最新收到的消息。但是，是什么原因导致状态更新呢？在 Android 应用中，状态会根据事件进行更新。

事件是从应用外部或内部生成的输入，例如：

- 用户与界面互动，例如按下按钮。
- 其他因素，例如传感器发送新值或网络响应。

**应用的状态说明了要在界面中显示的内容，而事件则是一种机制，可在状态发生变化时导致界面发生变化。**

**关键提示**：通常的描述为“是”某状态，“发生”某事件。

事件用于通知程序发生了某事。所有 Android 应用都有核心界面更新循环，如下所示：

![f415ca9336d83142.png](./img/f415ca9336d83142.png)

- 事件：由用户或程序的其他部分生成。
- 更新状态：事件处理脚本会更改界面所使用的状态。
- 显示状态：界面会更新以显示新状态。

Compose 中的状态管理主要是了解状态和事件之间的交互方式。


Compose 应用通过调用可组合函数将数据转换为界面。**组合**是指 Compose 在执行可组合项时构建的界面描述。如果发生状态更改，Compose 会使用新状态重新执行受影响的可组合函数，从而创建更新后的界面。这一过程称为**重组**。Compose 还会查看各个可组合项需要哪些数据，以便仅重组数据发生了变化的组件，而避免重组未受影响的组件。

**组合**：Jetpack Compose 在执行可组合项时构建的界面描述。

**初始组合**：通过首次运行可组合项创建组合。

**重组**：在数据发生变化时重新运行可组合项以更新组合。

为此，**Compose 需要知道要跟踪的状态**，以便在收到更新时安排重组。

**Compose 采用特殊的状态跟踪系统，可以为读取特定状态的任何可组合项安排重组**。这让Compose 能够实现精细控制，并且仅重组需要更改的可组合函数，而不是重组整个界面。这将通过同时跟踪针对状态的“写入”（即状态变化）和针对状态的“读取”来实现。

使用 Compose 的 [`State`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/State) 和 [`MutableState`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/MutableState) 类型让 Compose 能够观察到状态。

Compose 会跟踪每个读取状态 `value` 属性的可组合项，并在其 `value` 更改时触发重组。您可以使用 [`mutableStateOf`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary#mutableStateOf(kotlin.Any,androidx.compose.runtime.SnapshotMutationPolicy)) 函数来创建可观察的 `MutableState`。它接受初始值作为封装在 `State` 对象中的参数，这样便可使其 `value` 变为可观察。

更新 `WaterCounter` 可组合项，以便 `count` 以 `0` 为初始值来使用 `mutableStateOf` API。当 `mutableStateOf` 返回 `MutableState` 类型时，您可以更新其 `value` 以更新状态，并且 Compose 会在其 `value` 被读取时触发这些函数的重组。

如前所述，对 `count` 所做的任何更改都会安排对自动重组读取 `count` 的 `value` 的所有可组合函数进行重组。在此情况下，点击按钮即会触发重组 `WaterCounter`。

如果现在运行应用，您会再次发现没有发生任何变化！

安排重组的过程没有问题。不过，当重组发生时，变量 `count` 会重新初始化为 0，因此我们需要通过某种方式在重组后保留此值。

为此，我们可以使用 [`remember`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary#remember(kotlin.Function0)) 可组合内嵌函数。系统会在初始组合期间将由 **`remember`** 计算的值存储在组合中，并在重组期间一直保持存储的值。

您可以将 **`remember`** 视为一种在组合中存储单个对象的机制，就像私有 val 属性在对象中执行的操作一样。

`remember` 和 `mutableStateOf` 通常在可组合函数中一起使用。

修改 `WaterCounter`，将对 `mutableStateOf` 的调用置于 `remember` 内嵌可组合函数的内部。

```kotlin
@Composable
fun WaterCounter(modifier: Modifier = Modifier) {
    Column(modifier = modifier.padding(16.dp)) {
        val count: MutableState<Int> = remember { mutableStateOf(0) }
        Text(
            text = "You've had ${count.value} glasses.",
            modifier = modifier.padding(16.dp)
        )
        Button(onClick = { count.value++ }, Modifier.padding(top = 8.dp)) {
            Text("Add one")
        }
    }
}
```

使用 Kotlin 的[委托属性](https://kotlinlang.org/docs/delegated-properties.html)来简化 `count` 的使用。

您可以使用关键字 **by** 将 `count` 定义为 var。通过添加委托的 getter 和 setter 导入内容，我们可以间接读取 `count` 并将其设置为可变，而无需每次都显式引用 `MutableState` 的 `value` 属性。

现在，`WaterCounter` 如下所示：

```kotlin
@Composable
fun WaterCounter(modifier: Modifier = Modifier) {
    Column(modifier = modifier.padding(16.dp)) {
        var count by remember { mutableStateOf(0) }
        Text(
            text = "You've had $count glasses.",
            modifier = modifier.padding(16.dp)
        )
        Button(onClick = { count++ }, Modifier.padding(top = 8.dp)) {
            Text("Add one")
        }
    }
}
```

[Compose 和其他库  | Jetpack Compose  | Android Developers](https://developer.android.com/jetpack/compose/libraries#streams)

如果您更改语言、在深色模式与浅色模式之间切换，或者执行任何导致 Android 重新创建运行中 activity 的其他配置更改时，也会发生相同的情况。

虽然 `remember` 可帮助您在重组后保持状态，但不会帮助您**在配置更改后保持状态**。为此，您必须使用 [`rememberSaveable`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/saveable/package-summary#rememberSaveable(kotlin.Array,androidx.compose.runtime.saveable.Saver,kotlin.String,kotlin.Function0))，而不是 `remember`。

`rememberSaveable` 会自动保存可保存在 [`Bundle`](https://developer.android.com/reference/android/os/Bundle) 中的任何值。对于其他值，您可以将其传入自定义 Saver 对象。如需详细了解如何[在 Compose 中恢复状态](https://developer.android.com/jetpack/compose/state#restore-ui-state)，请参阅相关文档。

在 `WaterCounter` 中，将 `remember` 替换为 `rememberSaveable`：

```kotlin
import androidx.compose.runtime.saveable.rememberSaveable

@Composable
fun WaterCounter(modifier: Modifier = Modifier) {
        ...
        var count by rememberSaveable { mutableStateOf(0) }
        ...
}
```

现在运行应用并尝试进行一些配置更改。您应该会看到计数器已正确保存。

在重新创建 activity 或进程后，您可以使用 **`rememberSaveable`** 恢复界面状态。除了在重组后保持状态之外，**`rememberSaveable`** 还会在重新创建 activity 和进程之后保留状态。



使用 **`remember`** 存储对象的可组合项包含内部状态，这会使该可组合项**有状态**。在调用方不需要控制状态，并且不必自行管理状态便可使用状态的情况下，“有状态”会非常有用。但是，**具有内部状态的可组合项往往不易重复使用，也更难测试**。

**不保存任何状态的可组合项称为无状态可组合项**。如需创建**无状态**可组合项，一种简单的方法是使用状态提升。

Compose 中的状态提升是一种将状态移至可组合项的调用方以使可组合项无状态的模式。Jetpack Compose 中的常规状态提升模式是将状态变量替换为两个参数：

- **value: T**：要显示的当前值
- **onValueChange: (T) -> Unit**：请求更改值的事件，其中 T 是建议的新值

其中，此值表示任何可修改的状态。

状态下降、事件上升的这种模式称为单向数据流 (UDF)，而状态提升就是我们在 Compose 中实现此架构的方式。如需了解相关详情，请参阅 [Compose 架构文档](https://developer.android.com/jetpack/compose/architecture#udf-compose)。

以这种方式提升的状态具有一些重要的属性：

- **单一可信来源**：通过移动状态，而不是复制状态，我们可确保只有一个可信来源。这有助于避免 bug。
- **可共享**：可与多个可组合项共享提升的状态。
- **可拦截**：无状态可组合项的调用方可以在更改状态之前决定忽略或修改事件。
- **分离**：无状态可组合函数的状态可以存储在任何位置。例如，存储在 ViewModel 中。

## 有状态与无状态

当所有状态都可以从可组合函数中提取出来时，生成的可组合函数称为无状态函数。

**无状态**可组合项是指不具有任何状态的可组合项，这意味着它不会存储、定义或修改新状态。

**有状态**可组合项是一种具有可以随时间变化的状态的可组合项。

在实际应用中，让可组合项 100% 完全无状态可能很难实现，具体取决于可组合项的职责。在设计可组合项时，您应该让可组合项拥有尽可能少的状态，并能够在必要时通过在可组合项的 API 中公开状态来提升状态。



**要点**：提升状态时，有三条规则可帮助您弄清楚状态应去向何处：

1. 状态应至少提升到使用该状态（读取）的所有可组合项的**最低共同父项**。
2. 状态应至少提升到**它可以发生变化（写入）的最高级别**。
3. 如果**两种状态发生变化以响应相同的事件**，它们应**提升到同一级别**。

您可以将状态提升到高于这些规则要求的级别，但如果未将状态提升到足够高的级别，则遵循单向数据流会变得困难或不可能。

## [ViewModel 中的状态](https://developer.android.com/codelabs/jetpack-compose-state?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fjetpack-compose-for-android-developers-1%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fjetpack-compose-state#11)

屏幕或界面状态指示应在屏幕上显示的内容（例如任务列表）。**该状态通常会与层次结构中的其他层相关联，原因是其包含应用数据**。

界面状态描述屏幕上显示的内容，而应用逻辑则描述应用的行为方式以及应如何响应状态变化。逻辑分为两种类型：第一种是界面行为或界面逻辑，第二种是业务逻辑。

- 界面逻辑涉及如何在屏幕上显示状态变化（例如导航逻辑或显示信息提示控件）。
- 业务逻辑决定如何处理状态更改（例如付款或存储用户偏好设置）。该逻辑通常位于业务层或数据层，但绝不会位于界面层。

[ViewModel](https://developer.android.com/topic/libraries/architecture/viewmodel) 提供界面状态以及对位于应用其他层中的业务逻辑的访问。此外，ViewModel 还会在配置更改后继续保留，因此其生命周期比组合更长。ViewModel 可以遵循 Compose 内容（即 activity 或 fragment）的主机的生命周期，也可以遵循导航图的目的地的生命周期（如果您使用的是 [Compose Navigation 库](https://developer.android.com/jetpack/compose/navigation)）。

如需详细了解架构和界面层，请参阅[界面层文档](https://developer.android.com/jetpack/guide/ui-layer#define-ui-state)。

**警告**：ViewModel 并不是组合的一部分。因此，您不应保留可组合项中创建的状态（例如，记住的值），因为这可能会导致内存泄漏。