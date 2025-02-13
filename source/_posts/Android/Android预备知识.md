---
title: Android预备知识
date: 2022-11-28 11:55:17
categories: 
- Android
index_img: /img/project_structure.png
sticky: 
---
# Android 预备知识

- [Android 预备知识](#android-预备知识)
  - [App运行日志](#app运行日志)
  - [APP 工程文件目录结构](#app-工程文件目录结构)
  - [Gradle](#gradle)
  - [单位](#单位)
    - [Dpi](#dpi)
    - [Density](#density)
    - [Dip](#dip)
    - [实验一](#实验一)
    - [实验二](#实验二)
  - [快捷键](#快捷键)
  - [格式化时间](#格式化时间)

## App运行日志
Android 采用Log工具打印日志，它将各类日志划分为五个等级：

- {% label primary @Log.e %}：表示错误信息，比如可能导致程序崩溃的异常。
- <span class="label label-warning">Log.w</span>：表示警告信息。
- <span class="label label-primary">Log.i</span>：表示一般消息。
- `Log.d`：表示调试信息，可把程序运行时的变量值打印出来，方便跟踪调试。
- `Log.v`：表示冗余信息。

![log](./img/log.png)

## APP 工程文件目录结构

App工程分为两个层次，第一个层次是项目，另一个层次是模块。模块依附于项目，每个项目至少有一个模块，也能拥有多个模块。一般所言的“编译运行App”，指的是运行某个模块，而非运行某个项目，因为模块才对应实际的App。

![project_structure](./img/project_structure.png)

从图中看到，该项目下面有两个分类：一个是 app(代表app模块)；另一个是 Gradle Scripts。其中，app 下面又有3个子目录，其功能说明如下：
(1) manifests 子目录，下面只有一个XML文件，即AndroidManifest.xml，它是 App 的运行配置文件。
(2) java子目录，下面有3个com.example.myapp包，其中第一个包存放当前模块的Java源代码，后面两个包存放测试用的Java代码。
(3) res子目录，存放当前模块的资源文件。res下面又有4个子目录：
- drawable目录存放图形描述文件与图片文件。
- layout目录存放App页面的布局文件。
- mipmap目录存放App的启动图标。
- values目录存放一些常量定义文件，例如字符串常量strings.xml、像素常量dimens.xml、颜色常量colors.xml、样式风格定义styles.xml等。

Gradle scripts 下面主要是工程的编译配置文件，主要有：
(1) `build.gradle`，该文件分为项目级与模块级两种，用于描述App工程的编译规则。
(2) `proguard-rules.pro`，该文件用于描述Java代码的混淆规则。
(3) `gradle.properties`，该文件用于配置编译工程的命令行参数，一般无须改动。
(4) `settings.gradle`，该文件配置了需要编译哪些模块。初始内容为`include ':app'`，表示只编译 app 模块。
(5)`local.properties`，项目的本地配置文件，它在工程编译时自动生成，用于描述开发者电脑的环境配置，包括SDK的本地路径、NDK的本地路径等。

## Gradle

Gradle 是一个项目自动化构建工具，帮我们做了依赖、打包、部署、发布、各种渠道的差异管理等工作。


## 单位

| 名称                 | 解释                                                                                                                  |
| -------------------- | --------------------------------------------------------------------------------------------------------------------- |
| px (Pixel像素)       | 也称为图像元素，是作为图像构成的基本单元，单个像素的大小并不固定，跟随屏幕大小和像素数量的关系变化，一个像素点为1px。 |
| Resolution(分辨率)   | 是指屏幕的垂直和水平方向的像素数量，如果分辨率是1920 1080，那就是垂直方向有1920个像素，水平方向有1080个像素。         |
| Dpi(像素密度)        | 是指屏幕上每英寸（1英寸=2.54厘米)距离中有多少个像素点。                                                               |
| Density(密度)        | 是指屏幕上每平方英寸(2.54^2平方厘米)中含有的像素点数量。                                                              |
| Dip/dp(设备独立像素) | 也可以叫做dp，长度单位，同一个单位在不同的设备上有不同的显示效果，具体效果根据设备的密度有关，详细的公式请看下面。    |

  计算规则  

我们以一个4.95英寸 1920 1080 的nexus5手机设备为例：
### Dpi
1. 计算直角边像素数量：$1920^2+1080^2=2202^2$ (勾股定理) 。
2. 计算DPI：$2202/4.95= 445$ 。
3. 得到这个设备的DPI为 445 (每英寸的距离中有445个像素)。
### Density
上面得到每英寸中有445像素，那么density为每平方英寸中的像素数量，应该为: $445^2=198025$ 。
### Dip
所有显示到屏幕上的图像都是以p×为单位，Dip是我们开发中使用的长度单位，最后他也需要转换成pX，计算这个设备上 1dip等于多少px：
`px = dip x dpi /160`
根据换算关系:320 x 480分辨率，3.6寸的手机: dpi为160，1dp=1px

### 实验一

相同分辨率，不同大小的手机AB：

| 代号  | 分辨率  | 尺寸  | dpi | dp        |
| ----- | ------- | ----- | --- | --------- |
| 手机A | 320x480 | 3.6寸 | 160 | 1dp=1px   |
| 手机B | 320x480 | 7.2寸 | 80  | 1dp=0.5px |
假如AB都设置一个宽度为100dp的TextView：
| 代号  | TextView宽度 | 手机宽度 | 比例关系 |
| ----- | ------------ | -------- | -------- |
| 手机A | 100px        | 320px    | 10/32    |
| 手机B | 50px         | 320px    | 5/32     |

得出结论:

  对于相同分辨率的手机，屏幕越大，同DP的组件占用屏幕比例越小。  

如图所示：

![dp_1](./img/dp_1.png)

### 实验二

相同大小，不同分辨率的手机AB：

| 代号  | 分辨率  | 尺寸  | dpi | dp      |
| ----- | ------- | ----- | --- | ------- |
| 手机A | 320x480 | 3.6寸 | 160 | 1dp=1px |
| 手机B | 640x960 | 3.6寸 | 320 | 1dp=2px |


假如AB都设置一个宽度为100dp的TextView：
| 代号  | TextView宽度 | 手机宽度 | 比例关系 |
| ----- | ------------ | -------- | -------- |
| 手机A | 100px        | 320px    | 10/32    |
| 手机B | 200px        | 640px    | 10/32    |

得出结论:

  对于相同尺寸的手机，即使分辨率不同，同DP的组件占用屏幕比例也相同。  

如图所示：

![dp_2](./img/dp_2.png)

综上：

  dp的UI效果只在相同尺寸的屏幕上相同，如果屏幕尺寸差异过大，则需要重做dp适配。  

这也是平板需要单独做适配的原因，可见dp不是比例。


## 快捷键

快捷键可以提高代码编写效率

- `Ctrl`+`Alt`+`L`：格式化代码
- `Ctrl`+`Alt`+`O`：清除多余的引用
- `选中变量名`+`Ctrl`+`Alt`+`O`+`Enter/Tab`：将局部变量转为全局变量

使用Compose构建布局时：

- `comp`快速生成可组合函数
- `prev`快速生成可组合函数的预览

## 格式化时间

<table border=0 cellspacing=3 cellpadding=0 summary="Examples of date and time patterns interpreted in the U.S. locale">
   <tr style="background-color: rgb(204, 204, 255);">
       <th align=left>Date and Time Pattern
       <th align=left>Result
   <tr>
       <td><code>"yyyy.MM.dd G 'at' HH:mm:ss z"</code>
       <td><code>2001.07.04 AD at 12:08:56 PDT</code>
   <tr style="background-color: rgb(238, 238, 255);">
       <td><code>"EEE, MMM d, ''yy"</code>
       <td><code>Wed, Jul 4, '01</code>
   <tr>
       <td><code>"h:mm a"</code>
       <td><code>12:08 PM</code>
   <tr style="background-color: rgb(238, 238, 255);">
       <td><code>"hh 'o''clock' a, zzzz"</code>
       <td><code>12 o'clock PM, Pacific Daylight Time</code>
   <tr>
       <td><code>"K:mm a, z"</code>
       <td><code>0:08 PM, PDT</code>
   <tr style="background-color: rgb(238, 238, 255);">
       <td><code>"yyyyy.MMMM.dd GGG hh:mm aaa"</code>
       <td><code>02001.July.04 AD 12:08 PM</code>
   <tr>
       <td><code>"EEE, d MMM yyyy HH:mm:ss Z"</code>
       <td><code>Wed, 4 Jul 2001 12:08:56 -0700</code>
   <tr style="background-color: rgb(238, 238, 255);">
       <td><code>"yyMMddHHmmssZ"</code>
       <td><code>010704120856-0700</code>
   <tr>
       <td><code>"yyyy-MM-dd'T'HH:mm:ss.SSSZ"</code>
       <td><code>2001-07-04T12:08:56.235-0700</code>
   <tr style="background-color: rgb(238, 238, 255);">
       <td><code>"yyyy-MM-dd'T'HH:mm:ss.SSSXXX"</code>
       <td><code>2001-07-04T12:08:56.235-07:00</code>
   <tr>
       <td><code>"YYYY-'W'ww-u"</code>
       <td><code>2001-W27-3</code>
</table>