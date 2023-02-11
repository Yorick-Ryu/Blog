---
title: Compose基本布局
index_img: ./img/c1e6c40e30136af2.gif
categories: 
  - Android
date: 2022-12-08 13:39:36
tags: 
  - Jetpack
  - Compose
  - layout
sticky: 
---

# Compose基本布局

[Compose 布局基础知识  | Jetpack Compose  | Android Developers](https://developer.android.com/jetpack/compose/layouts/basics#slot-based-layouts)

[Compose 中的布局  | Jetpack Compose  | Android Developers (google.cn)](https://developer.android.google.cn/jetpack/compose/layouts?hl=zh-cn)

编写可组合项时，您可以使用**修饰符**执行以下操作：

- 更改可组合项的尺寸、布局、行为和外观。
- 添加信息，例如无障碍标签。
- 处理用户输入。
- 添加高级互动，例如使元素可点击、可滚动、可拖动或可缩放。

[Compose 修饰符  | Jetpack Compose  | Android Developers](https://developer.android.com/jetpack/compose/modifiers)

[Compose 修饰符列表  | Jetpack Compose  | Android Developers](https://developer.android.com/jetpack/compose/modifiers-list)

一般来说，若要对齐父容器中的可组合项，您应设置该父容器的**对齐方式**。因此，您应告知父项如何对齐其子项，而不是告知子项将其自身放置在父项中。

对于 `Column`，您可以决定其子项的水平对齐方式。具体选项包括：

- Start
- CenterHorizontally
- End

对于 `Row`，您可以设置垂直对齐。具体选项类似于 `Column` 的选项：

- Top
- CenterVertically
- Bottom

对于 `Box`，您可以同时使用水平对齐和垂直对齐。具体选项包括：

- TopStart
- TopCenter
- TopEnd
- CenterStart
- Center
- CenterEnd
- BottomStart
- BottomCenter
- BottomEnd

容器的所有子项都将遵循这一相同的对齐模式。您可以通过向单个子项添加 [`align`](https://developer.android.com/reference/kotlin/androidx/compose/foundation/layout/ColumnScope#(androidx.compose.ui.Modifier).align(androidx.compose.ui.Alignment.Horizontal)) 修饰符来替换其行为。

在上一步中，您了解了对齐方式，它用于在**交叉轴**上对齐容器的子项。对于 `Column`，交叉轴是水平轴；对于 `Row`，交叉轴则是垂直轴。

不过，我们也可以决定如何在容器的**主轴**（对于 `Row`，是水平轴；对于 `Column`，是垂直轴）上放置可组合子项。

对于 `Row`，您可以选择以下排列方式：

![c1e6c40e30136af2.gif](./img/c1e6c40e30136af2.gif)

对于 `Column`：

![df69881d07b064d0.gif](./img/df69881d07b064d0.gif)

除了这些排列方式之外，您还可以使用 `Arrangement.spacedBy()` 方法，在每个可组合子项之间添加固定间距。

**基于槽位的布局**会在界面中留出空白区域，让开发者按照自己的意愿来填充。您可以使用它们创建更灵活的布局。

虽然设计与大多数设备尺寸都非常契合，但如果设备的高度不足（例如在横屏模式下），设计需要能够垂直滚动。这就需要您添加滚动行为。

如前所述，`LazyRow` 和 `LazyHorizontalGrid` 等延迟布局会自动添加滚动行为。但是，您不一定总是需要延迟布局。一般来说，**在列表中有许多元素或需要加载大型数据集时，您需要使用延迟布局**，因此一次发出所有项不仅会降低性能，还会拖慢应用的运行速度。如果列表中的元素数量有限，您也可以选择使用简单的 `Column` 或 `Row`，然后**手动添加滚动行为**。为此，您可以使用 [`verticalScroll`](https://developer.android.com/reference/kotlin/androidx/compose/foundation/package-summary#(androidx.compose.ui.Modifier).verticalScroll(androidx.compose.foundation.ScrollState,kotlin.Boolean,androidx.compose.foundation.gestures.FlingBehavior,kotlin.Boolean)) 或 [`horizontalScroll`](https://developer.android.com/reference/kotlin/androidx/compose/foundation/package-summary#(androidx.compose.ui.Modifier).horizontalScroll(androidx.compose.foundation.ScrollState,kotlin.Boolean,androidx.compose.foundation.gestures.FlingBehavior,kotlin.Boolean)) 修饰符。这些修饰符需要 [`ScrollState`](https://developer.android.com/reference/kotlin/androidx/compose/foundation/ScrollState)，后者包含当前的滚动状态，可用于从外部修改滚动状态。