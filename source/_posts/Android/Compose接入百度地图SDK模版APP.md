---
title: Compose接入百度地图SDK模版APP
tags:
  - compose
index_img: /img/default.png
categories:
  - Android
date: 2025-07-16 23:04:12
sticky:
---

# 使用 Jetpack Compose 集成百度地图 SDK 的 Android 模板APP

项目地址：https://github.com/Yorick-Ryu/TemplateMap

# TemplateMap

一个使用 Jetpack Compose 集成百度地图 SDK 的 Android 模板应用。

## 📱 项目概述

TemplateMap 是一个现代化的 Android 应用模板，展示了如何在 Jetpack Compose 中集成和使用百度地图 SDK。项目采用最新的 Android 开发技术栈，提供了地图显示、定位服务、用户设置、日志记录分享等核心功能。

## ✨ 主要特性

- 🗺️ **百度地图集成**：基于百度地图 SDK 7.6.2，提供完整的地图功能
- 🎨 **现代化 UI**：使用 Jetpack Compose 构建现代化用户界面
- 🌙 **主题支持**：支持深色/浅色主题切换，支持动态主题
- 📍 **定位服务**：集成百度定位 SDK，提供精准定位功能
- 💾 **数据持久化**：使用 DataStore + Protocol Buffers 进行用户数据存储
- 🏗️ **模块化架构**：采用多模块架构，便于维护和扩展
- 🔧 **依赖注入**：使用 Hilt 进行依赖注入管理
- 📝 **日志系统**：基于 Timber 的完整日志解决方案

## 🏗️ 项目架构

项目采用多模块架构设计：

```
TemplateMap/
├── app/                   # 主应用模块
├── baidu-map-compose/     # 百度地图 Compose 封装库
└── common/                # 公共组件和工具库
```

### 模块说明

- **app**: 主应用模块，包含应用的核心业务逻辑
- **baidu-map-compose**: 百度地图的 Compose 封装库，提供易用的 Compose 地图组件
- **common**: 公共模块，包含通用组件、主题、工具类等

## 🛠️ 技术栈

- **语言**: Kotlin 2.2.0
- **UI框架**: Jetpack Compose (BOM 2025.06.01)
- **地图SDK**: 百度地图 SDK 7.6.2
- **定位SDK**: 百度定位 SDK 9.6.4
- **依赖注入**: Hilt 2.56.2
- **数据存储**: DataStore + Protocol Buffers
- **页面导航**: Navigation Compose 2.9.0
- **Material Design**: Material 3
- **日志**: Timber

## 📦 核心组件

### BDMap Compose 组件

项目的核心是 `BDMap` Compose 组件，它提供了：

- 地图显示和交互
- 相机位置控制
- 地图属性配置
- UI 设置管理
- 定位数据展示
- 地图事件回调
- 覆盖物支持

## 🚀 快速开始

### 环境要求

- **Android Studio**: Hedgehog | 2023.1.1 或更高版本（推荐最新稳定版）
- **JDK**: 19 或更高版本
- **Android SDK**: API 21+ (Android 5.0+)
- **目标版本**: API 36 (Android 16)
- **百度地图开发者账号**: 用于获取地图和定位服务AK

### 配置步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Yorick-Ryu/TemplateMap
   cd TemplateMap
   ```

2. **配置百度地图 AK**
   
   在 `app/src/main/AndroidManifest.xml` 中配置您的百度地图 AK（替换现有的示例AK）：
   ```xml
   <meta-data
       android:name="com.baidu.lbsapi.API_KEY"
       android:value="您的百度地图AK" />
   ```
   
   ⚠️ **重要**: 项目中包含的示例AK仅用于演示，请务必替换为您自己申请的AK。

3. **配置签名**
   
   复制 `keystore.properties.example` 为 `keystore.properties` 并配置您的签名信息：
   ```properties
   storeFile=您的keystore文件路径
   storePassword=keystore密码
   keyAlias=密钥别名
   keyPassword=密钥密码
   ```

4. **编译运行**
   ```bash
   ./gradlew assembleDebug
   ```

### 获取百度地图 AK

1. 访问 [百度地图开放平台](https://lbsyun.baidu.com/)
2. 注册并登录开发者账号
3. 创建应用并获取 AK
4. 配置 SHA1 指纹（用于定位功能）

## 📁 项目结构

```
app/src/main/java/com/yorick/templatemap/
├── data/                   # 数据层
│   ├── datastore/         # DataStore 相关
│   ├── di/                # 依赖注入模块
│   ├── model/             # 数据模型
│   ├── repository/        # 数据仓库
│   └── utils/             # 工具类
│       └── BDMapUtils.kt  # 百度地图工具类
├── ui/                    # UI 层
│   ├── map/               # 地图相关组件
│   ├── navigation/        # 导航组件
│   ├── screens/           # 屏幕组件
│   │   ├── HomeScreen.kt  # 主屏幕
│   │   ├── MapScreen.kt   # 地图屏幕
│   │   ├── MainScreen.kt  # 主界面
│   │   └── SettingsScreen.kt # 设置屏幕（含日志管理）
│   ├── viewmodels/        # ViewModel
│   └── TemplateMapApp.kt  # 主应用组件
├── MainActivity.kt        # 主Activity
└── TemplateMapApplication.kt # Application类

baidu-map-compose/src/main/java/com/melody/map/baidu_compose/
├── adapter/               # 适配器
├── extensions/            # 扩展函数
├── kernel/                # 核心功能
├── model/                 # 模型类
├── overlay/               # 覆盖物组件
│   ├── Arc.kt            # 弧线覆盖物
│   ├── Circle.kt         # 圆形覆盖物
│   ├── Marker.kt         # 标记覆盖物
│   ├── Polygon.kt        # 多边形覆盖物
│   └── Polyline.kt       # 折线覆盖物
├── poperties/             # 属性配置
├── position/              # 位置状态
├── utils/                 # 工具类
│   └── clustering/        # 聚合相关
├── BDMap.kt              # 主地图组件
├── MapApplier.kt         # 地图应用器
└── MapUpdater.kt         # 地图更新器

common/src/main/java/com/yorick/common/
├── data/                  # 公共数据模型
│   ├── model/             # 数据模型
│   └── utils/             # 公共工具类
│       ├── CommonUtils.kt # 通用工具
│       └── LogUtils.kt    # 日志管理工具
└── ui/                    # 公共UI组件
    ├── components/        # 通用组件
    ├── navigation/        # 导航相关
    └── theme/             # 主题配置

```

## 🎯 核心功能介绍

### 地图功能

- 地图显示和基本交互
- 地图类型切换
- 缩放控制
- 位置标记
- 地图事件处理

### 定位功能

- GPS 定位
- 网络定位
- 位置权限管理
- 位置数据展示

### 设置功能

- 主题切换（浅色/深色）
- 动态主题支持
- 用户偏好保存
- 日志分享与清理

## 🔧 自定义开发

### 添加新的地图覆盖物

在 `baidu-map-compose/src/main/java/com/melody/map/baidu_compose/overlay/` 目录下创建新的覆盖物组件。

### 扩展地图功能

1. 在 `MapProperties` 中添加新属性
2. 在 `MapUpdater` 中处理属性更新
3. 在 `BDMap` 组件中暴露相关参数

### 添加新屏幕

1. 在 `ui/screens/` 下创建新的屏幕组件
2. 在 `navigation/` 中添加导航路由
3. 在主应用中集成新屏幕

## 📝 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。

### 第三方库许可

- 百度地图 Compose 封装库部分基于 [OmniMap](https://github.com/TheMelody/OmniMap) 项目，感谢原作者的贡献
- 本项目使用的所有第三方库均遵循各自的开源许可协议
- 百度地图 SDK 的使用需遵循百度地图开放平台的服务条款

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 提交 Issue
- 💬 发送邮件（访问开发者主页获取）

## 🙏 致谢

- [百度地图开放平台](https://lbsyun.baidu.com/) - 提供地图和定位服务
- [OmniMap](https://github.com/TheMelody/OmniMap) - 地图Compose封装参考
- [Jetpack Compose](https://developer.android.com/jetpack/compose) - 现代化UI工具包
- [Timber](https://github.com/JakeWharton/timber) - 日志记录

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！ 