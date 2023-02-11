---
title: Compose中使用Navigation
index_img: /img/android-jetpack.svg
categories: 
  - Android
date: 2022-12-14 15:35:47
tags: 
  - Jetpack
  - Compose
  - Navigation
sticky: 
---

# Jetpack Compose Navigation

[使用 Compose 进行导航  | Jetpack Compose  | Android Developers (google.cn)](https://developer.android.google.cn/jetpack/compose/navigation?hl=zh-cn)

## 迁移到 Compose Navigation

迁移到 Jetpack Compose 基本涉及以下几个步骤：

1. 添加最新的 [Compose Navigation 依赖项](https://mvnrepository.com/artifact/androidx.navigation/navigation-compose)
2. 设置 [`NavController`](https://developer.android.com/jetpack/compose/navigation#getting-started)
3. 添加 [`NavHost`](https://developer.android.com/jetpack/compose/navigation#create-navhost) 并创建导航图
4. 准备路线以在不同的应用目的地之间导航
5. 将当前导航机制替换为 Compose Navigation



使用 Compose 中的 Navigation 时，导航图中的每个可组合目的地都与一个[**路线**](https://developer.android.com/jetpack/compose/navigation#create-navhost)相关联。路线用字符串表示，用于定义指向可组合项的路径，并指引您的 `navController` 到达正确的位置。您可以将其视为指向特定目的地的隐式深层链接。**每个目的地都必须有一条唯一的路线**。

Navigation 的 3 个主要部分是 `NavController`、`NavGraph` 和 `NavHost`。`NavController` 始终与一个 `NavHost` 可组合项相关联。`NavHost` 充当容器，负责显示导航图的当前目的地。当您在可组合项之间进行导航时，`NavHost` 的内容会自动进行[重组](https://developer.android.com/jetpack/compose/mental-model#recomposition)。此外，它还会将 `NavController` 与导航图 ([`NavGraph`](https://developer.android.com/reference/androidx/navigation/NavGraph)) 相关联，后者用于标出能够在其间进行导航的可组合目的地。它实际上是一系列可提取的目的地。

我们将介绍同一 `navigateSingleTopTo` 扩展函数中可供您使用的一些其他选项：

- `launchSingleTop = true` - 如上所述，这可确保返回堆栈顶部最多只有给定目的地的一个副本
- 在 Rally 应用中，这意味着，多次重按同一标签页不会启动同一目的地的多个副本
- `popUpTo(startDestination) { saveState = true }` - 弹出到导航图的起始目的地，以免在您选择标签页时在返回堆栈上构建大型目的地堆栈
- 在 Rally 中，这意味着，在任何目的地按下返回箭头都会将整个返回堆栈弹出到“Overview”屏幕
- `restoreState = true` - 确定此导航操作是否应恢复 `PopUpToBuilder.saveState` 或 `popUpToSaveState` 属性之前保存的任何状态。请注意，如果之前未使用要导航到的目的地 ID 保存任何状态，**此项不会产生任何影响**
- 在 Rally 中，这意味着，重按同一标签页会保留屏幕上之前的数据和用户状态，而无需重新加载