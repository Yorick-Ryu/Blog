---
title: Android开屏动画
tags:
  - UI
index_img: /img/default.png
categories:
  - Android
date: 2023-01-28 13:44:33
sticky:
---

# Android开屏动画(Splash Screen)

摘自：[启动画面  | Android 开发者  | Android Developers](https://developer.android.com/guide/topics/ui/splash-screen?hl=zh-cn)

从 Android 12 开始，在搭载 Android 12 或更高版本的设备上运行时，所有应用都将拥有启动动画。这包括启动时的进入应用动作、显示应用图标的启动画面，以及向应用本身的过渡。

## 启动画面的工作原理

当用户启动应用而应用的进程未运行（[冷启动](https://developer.android.com/topic/performance/vitals/launch-time?hl=zh-cn#cold)）或 activity 尚未创建（[温启动](https://developer.android.com/topic/performance/vitals/launch-time?hl=zh-cn#warm)）时，会发生以下事件。（在[热启动](https://developer.android.com/topic/performance/vitals/launch-time?hl=zh-cn#hot)期间从不显示启动画面。）

1. 系统使用主题以及您已定义的任何动画显示启动画面。
2. 当应用准备就绪时，系统会关闭启动画面并显示应用。

## 启动画面的元素和机制

启动画面的元素由 Android 清单中的 XML 资源文件定义。每个元素都有浅色模式和深色模式版本。

启动画面的可自定义元素包括应用图标、图标背景和窗口背景：

关于这些元素，请注意以下几点：

1. **应用图标**应该是矢量可绘制对象，它可以是静态或动画形式。虽然动画的时长可以不受限制，但我们建议不超过 1000 毫秒。默认情况下，使用启动器图标。
2. 可以选择添加**图标背景**；在图标与窗口背景之间需要更高的对比度时图标背景很有用。如果您使用一个[自适应图标](https://developer.android.com/guide/practices/ui_guidelines/icon_design_adaptive?hl=zh-cn)，当该图标与窗口背景之间的对比度足够高时，就会显示其背景。
3. 与自适应图标一样，前景的三分之一被遮盖。
4. **窗口背景**由不透明的单色组成。如果窗口背景已设置且为纯色，则未设置相应的属性时默认使用该背景。

### 启动画面尺寸

启动画面图标使用的规范与[自适应图标](https://developer.android.com/guide/practices/ui_guidelines/icon_design_adaptive?hl=zh-cn)相同，如下所示：

- 品牌图片：尺寸应为 200×80 dp。
- 带有图标背景的应用图标：尺寸应为 240×240 dp，并且位于直径 160 dp 的圆圈内。
- 无图标背景的应用图标：尺寸应为 288×288 dp，并且位于直径 192 dp 的圆圈内。

例如，如果图片的完整尺寸为 300×300 dp，则图标需要位于直径 200 dp 的圆圈内。圆圈以外的所有内容将不可见（被遮盖）。

### 启动画面动画和启动序列

额外的延迟时间通常与在冷启动时启动应用有关。向启动画面添加动画图标具有明显的美感，并提供更优质的体验，除此之外，还有额外的好处：用户研究表明，在观看动画时，用户感知到的启动时间会缩短。

启动画面动画会嵌入到以下启动序列组件中。

1. 进入动画：由系统视图到启动画面组成。这由系统控制且不可自定义。
2. 启动画面：您可以对启动画面进行自定义，从而提供自己的徽标动画和品牌形象。它必须满足本文档中所述的[要求](https://developer.android.com/guide/topics/ui/splash-screen?hl=zh-cn#splash-screen-animate-reqs)，才能正常运行。
3. 退出动画：由隐藏启动画面的动画运行组成。如果您要[对其进行自定义](https://developer.android.com/guide/topics/ui/splash-screen?hl=zh-cn#customize-animation)，您将可以访问 [`SplashScreenView`](https://developer.android.com/reference/android/window/SplashScreenView?hl=zh-cn) 及其图标，并且可以在它们之上运行任何动画（需要设置转换、不透明度和颜色）。在这种情况下，当动画完成时，需要手动移除启动画面。

运行图标动画时，如果应用先前已准备就绪，应用启动功能可让您选择跳过相应序列。应用会触发 `onResume()` 或者启动画面会自动超时，因此确保用户能够轻松跳过启动画面动画。只有当从视觉角度来看应用稳定后，才应通过 `onResume()` 关闭启动画面，因此无需额外的旋转图标。引入不完整的界面可能会给用户带来不快，并让用户感觉不可预知或不够完善。

#### 启动画面动画要求

启动画面应符合以下规范：

- 设置不透明的单一窗口背景颜色。[SplashScreen compat 库](https://developer.android.com/reference/kotlin/androidx/core/splashscreen/SplashScreen?hl=zh-cn)同时支持日间模式和夜间模式。
- 确保动画图标符合以下规范：
  - **格式**：必须是[动画形式的矢量可绘制对象 (AVD)](https://developer.android.com/reference/android/graphics/drawable/AnimatedVectorDrawable?hl=zh-cn) XML。
  - 尺寸：AVD 图标的大小必须是自适应图标大小的四倍，如下所示：
    - 图标面积必须是 432 dp（即 108 dp 的 4 倍，108 dp 是无遮盖自适应图标的面积）。
    - 图片内部三分之二的区域在启动器图标上可见，并且必须是 288 dp（即 72 dp 的四倍，72 dp 是自适应图标内部遮盖区域的面积）。
  - **时长**：我们建议在手机上的时长不超过 1,000 毫秒。您可以使用延迟启动，但不能超过 166 毫秒。如果应用启动时间超过 1000 毫秒，请考虑使用循环动画。
- 确定合适的时间来关闭启动画面，这发生在应用绘制第一帧时。您可以按照本文档中[让启动画面在屏幕上显示更长时间](https://developer.android.com/guide/topics/ui/splash-screen?hl=zh-cn#suspend-drawing)部分的说明进一步自定义此设置。

## 自定义应用中的启动画面

默认情况下，`SplashScreen` 使用主题的 `windowBackground`（如果它是单色）和启动器图标。启动画面的自定义通过向应用主题添加属性来完成。

您可以通过以下任一方式自定义应用的启动画面：

- 设置主题属性以更改其外观
- 让其在屏幕上显示更长时间
- 自定义用于关闭启动画面的动画

### 设置启动画面的主题以更改其外观

您可以在 activity 主题中指定以下属性来自定义应用的启动画面。如果您已有使用 `android:windowBackground` 等属性的旧版启动画面实现，不妨考虑为 Android 12 及更高版本提供替代资源文件。

1. 使用 [`windowSplashScreenBackground`](https://developer.android.com/reference/android/R.attr?hl=zh-cn#windowSplashScreenBackground) 以特定的单色填充背景：

   ```xml
   <item name="android:windowSplashScreenBackground">@color/...</item>
   ```

2. 使用 [`windowSplashScreenAnimatedIcon`](https://developer.android.com/reference/android/R.attr?hl=zh-cn#windowSplashScreenAnimatedIcon) 替换起始窗口中心的图标。如果该对象可通过 [`AnimationDrawable`](https://developer.android.com/reference/android/graphics/drawable/AnimationDrawable?hl=zh-cn) 和 [`AnimatedVectorDrawable`](https://developer.android.com/reference/android/graphics/drawable/AnimatedVectorDrawable?hl=zh-cn) 呈现动画效果和进行绘制，那么您还需要设置 `windowSplashScreenAnimationDuration`，以在显示起始窗口的同时播放动画。

   ```xml
   <item name="android:windowSplashScreenAnimatedIcon">@drawable/...</item>
   ```

3. 使用 [`windowSplashScreenAnimationDuration`](https://developer.android.com/reference/android/R.attr?hl=zh-cn#windowSplashScreenAnimationDuration) 指示启动画面图标动画的时长。设置该时长对显示启动画面的实际时间不会产生任何影响，但您可以在自定义启动画面退出动画时使用 [`SplashScreenView#getIconAnimationDuration`](https://developer.android.com/guide/topics/ui/splash-screen/reference/android/window/SplashScreenView?hl=zh-cn#getIconAnimationDuration()) 检索图标动画的时长。如需了解详情，请参阅下一部分中的[让启动画面显示更长时间](https://developer.android.com/guide/topics/ui/splash-screen?hl=zh-cn#suspend-drawing)。

   ```xml
   <item name="android:windowSplashScreenAnimationDuration">1000</item>
   ```

4. 使用 `windowSplashScreenIconBackgroundColor` 设置启动画面图标后面的背景。当窗口背景与图标之间的对比度不够高时，这很有用。

   ```xml
   <item name="android:windowSplashScreenIconBackgroundColor">@color/...</item>
   ```

5. （可选）您可以使用 [`windowSplashScreenBrandingImage`](https://developer.android.com/reference/android/R.attr?hl=zh-cn#windowSplashScreenBrandingImage) 设置要显示在启动画面底部的图片。设计准则建议不要使用品牌图片。

   ```xml
   <item name="android:windowSplashScreenBrandingImage">@drawable/...</item>
   ```
