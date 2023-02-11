---
title: Compose迁移
index_img: /img/android-jetpack.svg
categories: 
  - Android
date: 2022-12-09 15:19:16
tags: 
  - Jetpack
  - Compose
  - view
sticky: 
---

# 迁移到Compose

如何迁移到 Compose 取决于您和您的团队。要将 Jetpack Compose 集成到现有 Android 应用中，有多种不同的方法。常用的两种迁移策略为：

- 完全使用 Compose 开发一个新界面
- 选取一个现有界面，然后逐步迁移其中的各个组件。

## 新界面中的 Compose

在重构应用代码以适应新技术时，一种常用的方法是在为应用构建的新功能中采用该技术。在这种情况下，适合使用新的界面。如果您需要为应用构建新界面，请考虑使用 Compose，而应用的其余部分可以保留在 View 系统中。

在这种情况下，您需要在这些已迁移功能的边缘实现 Compose 互操作性。

## 搭配使用 Compose 和 View

对于特定界面，您可以将部分界面迁移到 Compose，让其他部分保留在 View 系统中。例如，您可以迁移 RecyclerView，同时将界面的其余部分保留在 View 系统中。

或者，使用 Compose 作为外部布局，并使用 Compose 中可能没有的一些现有 View，比如 MapView 或 AdView。

## 完成迁移

将全部 fragment 或界面迁移到 Compose，一次迁移一个。这种方式最为简单，但比较粗放。