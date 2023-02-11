---
title: Android应用架构指南
tags:
  - 应用
index_img: /img/default.png
categories:
  - Android
date: 2022-12-15 20:04:10
sticky:
---

# Android应用架构指南

[TOC]

[应用架构指南  | Android 开发者  | Android Developers (google.cn)](https://developer.android.google.cn/jetpack/guide?hl=zh-cn)

## 移动应用用户体验

典型的 Android 应用包含多个[应用组件](https://developer.android.google.cn/guide/components/fundamentals?hl=zh-cn#components)，包括 [Activity](https://developer.android.google.cn/guide/components/activities/intro-activities?hl=zh-cn)、[Fragment](https://developer.android.google.cn/guide/fragments?hl=zh-cn)、[Service](https://developer.android.google.cn/guide/components/services?hl=zh-cn)、[内容提供程序](https://developer.android.google.cn/guide/topics/providers/content-providers?hl=zh-cn)和[广播接收器](https://developer.android.google.cn/guide/components/broadcasts?hl=zh-cn)。您需要在[应用清单](https://developer.android.google.cn/guide/topics/manifest/manifest-intro?hl=zh-cn)中声明其中的大多数应用组件。Android 操作系统随后会使用此文件来决定如何将您的应用集成到设备的整体用户体验中。鉴于典型的 Android 应用可能包含多个组件，并且用户经常会在短时间内与多个应用进行互动，因此应用需要适应不同类型的用户驱动型工作流和任务。

请注意，移动设备的资源也很有限，因此操作系统可能随时终止某些应用进程以便为新的进程腾出空间。

鉴于这种环境条件，您的应用组件可以不按顺序地单独启动，并且操作系统或用户可以随时销毁它们。由于这些事件不受您的控制，因此您不应在内存中存储或保留任何应用数据或状态，并且应用组件不应相互依赖。

## 常见的架构原则

如果您不应使用应用组件存储应用数据和状态，那么您应该改为如何设计应用呢？

随着 Android 应用大小不断增加，您定义的架构务必要能允许应用扩缩、提升应用的稳健性并且方便对应用进行测试。

应用架构定义了应用的各个部分之间的界限以及每个部分应承担的职责。为了满足上述需求，您应该按照某些特定原则设计应用架构。

### 分离关注点

要遵循的最重要的原则是[分离关注点](https://en.wikipedia.org/wiki/Separation_of_concerns)。 一种常见的错误是在一个 [`Activity`](https://developer.android.google.cn/reference/android/app/Activity?hl=zh-cn) 或 [`Fragment`](https://developer.android.google.cn/reference/android/app/Fragment?hl=zh-cn) 中编写所有代码。这些基于界面的类应仅包含处理界面和操作系统交互的逻辑。您应使这些类尽可能保持精简，这样可以避免许多与组件生命周期相关的问题，并提高这些类的可测试性。

请注意，您并非拥有 `Activity` 和 `Fragment` 的实现；它们只是表示 Android 操作系统与应用之间关系的粘合类。操作系统可能会根据用户互动或因内存不足等系统条件随时销毁它们。为了提供令人满意的用户体验和更易于管理的应用维护体验，最好尽量减少对它们的依赖。

### 通过数据模型驱动界面

另一个重要原则是您应该通过数据模型驱动界面（最好是持久性模型）。数据模型代表应用的数据。它们独立于应用中的界面元素和其他组件。这意味着它们与界面和应用组件的生命周期没有关联，但仍会在操作系统决定从内存中移除应用的进程时被销毁。

持久性模型是理想之选，原因如下：

- 如果 Android 操作系统销毁应用以释放资源，用户不会丢失数据。
- 当网络连接不稳定或不可用时，应用会继续工作。

如果您的应用机构以数据模型类为基础，您的应用会更便于测试、更稳定可靠。

## 推荐的应用架构

本部分将演示如何按照建议的最佳做法构建应用。

{% note info %}
**注意**：本页中提供的建议和最佳实践可应用于广泛的应用。遵循这些建议和最佳实践可以提升应用的可扩缩性、质量和稳健性，并可使应用更易于测试。不过，您应该将这些提示视为指南，并视需要进行调整来满足您的要求。
{% endnote %}


基于上一部分提到的常见架构原则，每个应用应至少有两个层：

- 界面层 - 在屏幕上显示应用数据。
- 数据层 - 包含应用的业务逻辑并公开应用数据。

您可以额外添加一个名为“网域层”的架构层，以简化和重复使用界面层与数据层之间的交互。

![在典型的应用架构中，界面层会从数据层或可选网域层（位于界面层和数据层之间）获取应用数据。](./img/mad-arch-overview.png)

**图 1.** 典型应用架构的示意图。

{% note info %}
**注意**：本指南中示意图中的箭头表示各个类之间的依赖关系。例如，网域层依赖于数据层类。
{% endnote %}

### 界面层

界面层（或呈现层）的作用是在屏幕上显示应用数据。无论是因为用户互动（例如按下按钮）还是外部输入（例如网络响应）导致数据发生变化时，界面都应更新以反映相应的变化。

界面层由以下两部分组成：

- 在屏幕上呈现数据的界面元素。您可以使用 View 或 [Jetpack Compose](https://developer.android.google.cn/jetpack/compose?hl=zh-cn) 函数构建这些元素。
- 用于存储数据、向界面提供数据以及处理逻辑的状态容器（如 [ViewModel](https://developer.android.google.cn/topic/libraries/architecture/viewmodel?hl=zh-cn) 类）。

![在典型架构中，界面层的界面元素依赖于状态容器，而状态容器又依赖于来自数据层或可选网域层的类。](./img/mad-arch-overview-ui.png)

**图 2.**界面层在应用架构中的作用。

如需详细了解此层，请参阅[界面层页面](https://developer.android.google.cn/jetpack/guide/ui-layer?hl=zh-cn)。

### 数据层

应用的数据层包含*业务逻辑*。业务逻辑决定应用的价值，它包含决定应用如何创建、存储和更改数据的规则。

数据层由多个代码库组成，其中每个代码库可包含零到多个数据源。您应该为应用处理的每种不同类型的数据创建一个代码库类。例如，您可以为与电影相关的数据创建 `MoviesRepository` 类，或者为与付款相关的数据创建 `PaymentsRepository` 类。

![在典型架构中，数据层的代码库会向应用的其余部分提供数据，而这些代码库则依赖于数据源。](./img/mad-arch-overview-data.png)

**图 3.** 数据层在应用架构中的作用。

代码库类负责以下任务：

- 向应用的其余部分提供数据。
- 对数据进行集中更改。
- 解决多个数据源之间的冲突。
- 从应用的其余部分中提取数据源。
- 包含业务逻辑。

每个数据源类应仅负责处理一个数据源，该数据源可以是文件、网络来源或本地数据库。数据源类是应用与数据操作系统之间的桥梁。

如需详细了解此层，请参阅[数据层页面](https://developer.android.google.cn/jetpack/guide/data-layer?hl=zh-cn)。

### 网域层

网域层是位于界面与数据层之间的可选层。

网域层负责封装复杂的业务逻辑，或者由多个 ViewModel 重复使用的简单业务逻辑。此层是可选的，因为并非所有应用都有这类需求。请仅在需要时使用该层，例如处理复杂逻辑或支持可重用性。

![如果添加了此层，则该可选网域层会向界面层提供依赖项，而它自身依赖于数据层。](./img/mad-arch-overview-domain.png)

**图 4.**网域层在应用架构中的作用。

该层中的类通常称为*用例*或*交互方*。每个用例都应仅负责单个功能。例如，如果多个 ViewModel 依赖时区在屏幕上显示适当的消息，则您的应用可能具有 `GetTimeZoneUseCase` 类。

如需详细了解此层，请参阅[网域层页面](https://developer.android.google.cn/jetpack/guide/domain-layer?hl=zh-cn)。

## 管理组件之间的依赖关系

应用中的类要依赖其他类才能正常工作。您可以使用以下任一设计模式来收集特定类的依赖项：

- [依赖注入 (DI)](https://developer.android.google.cn/training/dependency-injection?hl=zh-cn)：依赖注入使类能够定义其依赖项而不构造它们。在运行时，另一个类负责提供这些依赖项。
- [服务定位器](https://en.wikipedia.org/wiki/Service_locator_pattern)：服务定位器模式提供了一个注册表，类可以从中获取其依赖项而不构造它们。

您可以借助这些模式来扩展代码，因为它们可提供清晰的依赖项管理模式（无需复制代码，也不会增添复杂性）。 此外，您还可以借助这些模式在测试和生产实现之间快速切换。

**我们建议在 Android 应用中采用依赖项注入模式并使用 [Hilt 库](https://developer.android.google.cn/training/dependency-injection/hilt-android?hl=zh-cn)。**Hilt 通过遍历依赖项树自动构造对象，为依赖项提供编译时保证，并为 Android 框架类创建依赖项容器。

## 常见的最佳做法

编程是一个创造性的领域，构建 Android 应用也不例外。 无论是在多个 Activity 或 Fragment 之间传递数据，检索远程数据并将其保留在本地以在离线模式下使用，还是复杂应用遇到的任何其他常见情况，解决问题的方法都会有很多种。

虽然以下建议不是强制性的，但在大多数情况下，遵循这些建议会使您的代码库更强大、可测试性更高且更易维护：

**不要将数据存储在应用组件中。**

请避免将应用的入口点（如 Activity、Service 和广播接收器）指定为数据源。相反，您应只将其与其他组件协调，以检索与该入口点相关的数据子集。每个应用组件存在的时间都很短暂，具体取决于用户与其设备的交互情况以及系统当前的整体运行状况。

**减少对 Android 类的依赖**。

您的应用组件应该是唯一依赖于 Android 框架 SDK API （例如 [`Context`](https://developer.android.google.cn/reference/android/content/Context?hl=zh-cn) 或 [`Toast`](https://developer.android.google.cn/guide/topics/ui/notifiers/toasts?hl=zh-cn)）的类。将应用中的其他类与这些类分离开来有助于改善可测试性，并减少应用中的[耦合](https://en.wikipedia.org/wiki/Coupling_(computer_programming))。

**在应用的各个模块之间设定明确定义的职责界限。**

例如，请勿在代码库中将从网络加载数据的代码散布到多个类或软件包中。同样，也不要将不相关的职责（如数据缓存和数据绑定）定义到同一个类中。遵循[推荐的应用架构](https://developer.android.google.cn/jetpack/guide?hl=zh-cn#recommended-app-arch)可以帮助您解决此问题。

**尽量少公开每个模块中的代码。**

例如，请勿试图创建从模块提供内部实现细节的快捷方式。短期内，您可能会省点时间，但随着代码库的不断发展，您可能会反复陷入技术上的麻烦。

**专注于应用的独特核心，以使其从其他应用中脱颖而出。**

不要一次又一次地编写相同的样板代码，这是在做无用功。 相反，您应将时间和精力集中放在能让应用与众不同的方面上，并让 Jetpack 库以及建议的其他库处理重复的样板。

**考虑如何使应用的每个部分可独立测试。**

例如，如果使用明确定义的 API 从网络获取数据，将会更容易测试在本地数据库中保留该数据的模块。如果您将这两个模块的逻辑混放在一处，或将网络代码分散在整个代码库中，那么即便能够进行有效测试，难度也会大很多。

**保留尽可能多的相关数据和最新数据。**

这样，即使用户的设备处于离线模式，他们也可以使用您应用的功能。请记住，并非所有用户都能享受到稳定的高速连接 - 即使有时可以使用，在比较拥挤的地方网络信号也可能不佳。

## 示例

以下 Google 示例展示了良好的应用架构。您不妨浏览一下它们，了解如何实际运用本指南：

- [iosched](https://github.com/google/iosched)（Google I/O 应用）
- [Sunflower](https://github.com/android/sunflower)
- [Trackr](https://github.com/android/trackr)
- [Jetnews](https://github.com/android/compose-samples/tree/main/JetNews)（使用 Jetpack Compose 实现）
- [架构示例](https://github.com/android/architecture-samples)
