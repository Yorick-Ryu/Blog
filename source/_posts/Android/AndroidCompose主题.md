---
title: Compose主题
index_img: /img/md3_theme.png
categories: 
  - Android
date: 2022-12-09 12:58:44
tags: 
  - Jetpack
  - Compose
  - Theme
  - MaterialDesign
sticky: 
---

# Compose主题

[Compose 中的 Material Design 2  | Jetpack Compose  | Android Developers](https://developer.android.com/jetpack/compose/themes/material#material3)

[androidx.compose.material3  | Android Developers](https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary)

## 创建主题资源

1. 进入[Material Design](https://m3.material.io/theme-builder#/custom)

2. 选择品牌颜色，即`Primary Color`，也是种子颜色

3. 点击右上角Export按钮，选择`Jetpack Compose(Theme.kt)`，下载主题文件并放入项目包下

4. 配置主题，引入颜色，字体，形状等预定义元素

   示例：

   ```kotlin
   @Composable
   fun CokoToolsTheme(
       darkTheme: Boolean = isSystemInDarkTheme(), // 深色主题
       dynamicColor: Boolean = true, // 动态取色（Android12+）
       content: @Composable () -> Unit // 这里就是主题作用域
   ) {
       val cokeToolsColorScheme = when {
           dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
               val context = LocalContext.current
               if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
           }
           darkTheme -> DarkColors
           else -> LightColors
       }
   
       MaterialTheme(
           colorScheme = cokeToolsColorScheme,
           shapes = cokoToolsShapes,
           typography = cokoToolsTypography,
           content = content
       )
   }
   ```

   实际上，就是**替换**默认主题`MaterialTheme`里的元素。

## 使用主题资源

首先，将使用自定义主题的内容放在主题作用域中：

示例：在`MainActivity.kt`的`setContent`中放入我们的主题可组合项，并在其作用域内放入`HomeScreen`可组合项

```kotlin
setContent {
    CokoToolsTheme {
        HomeScreen()
    }
}
```

然后就可以在作用域内使用预定义资源：

- 使用颜色：

  ```kotlin
  color = MaterialTheme.colorScheme.primary
  ```

- 使用字体

  ```kotlin
  style = MaterialTheme.typography.titleLarge
  ```

- 使用形状

  ```kotlin
  shape = MaterialTheme.shapes.large
  ```



