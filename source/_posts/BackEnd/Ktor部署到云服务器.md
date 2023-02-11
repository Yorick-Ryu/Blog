---
title: Ktor部署到云服务器
tags:
  - ktor
  - Linux
  - CentOS
index_img: https://ktor.io/docs/images/ktor_logo.svg
categories:
  - BackEnd
date: 2023-01-26 17:22:29
sticky:
---

# Ktor部署到云服务器(Linux)

部署 Ktor 项目有很多种方式，包括 **war、jar 或是打包在 Docker 容器内**。 jar 是一种 Java 档案文件，可以将类文件打包成一个单一可运行的文件。 生成 jar 文件后，就可以通过 java -jar *.jar 的方式将程序运行起来。

## 前提

- 一个准备部署的[Ktor](https://ktor.io/)项目
- 一台Linux服务器（CentOS7.6），如果没有服务器可以点击[这里](https://www.aliyun.com/minisite/goods?userCode=cucsy8ip)购买，新用户超低价！

## 打包为Jar

参考：[Creating fat JARs using the Ktor Gradle plugin | Ktor](https://ktor.io/docs/fatjar.html)

To build a fat JAR, you need to configure the Ktor plugin first:

在打包为`fat Jar`之前，你需要先配置`Ktor plugin`

1. 打开`build.gradle.kts`，在plugins中添加插件：

   ```kotlin
   plugins {
       id("io.ktor.plugin") version "2.2.2"
   }
   ```

   

2. 确保`application`中填入[main](https://ktor.io/docs/server-dependencies.html#create-entry-point)方法所在类名：

   ```kotlin
   application {
       mainClass.set("com.example.ApplicationKt") // main方法所在类名
   }
   ```

   

3. 可选项，配置打包后的文件名称 ：

   ```kotlin
   ktor {
       fatJar {
           archiveFileName.set("fat.jar")
       }
   }
   ```

4. 点击`Gradle`同步项目，找到buildFatJar并双击构建Jar包：

   ![image-20230126174449384](./img/image-20230126174449384.png)

5. 打包好的文件在`build/libs`：

   ![image-20230126174735567](./img/image-20230126174735567.png)

## 上传Jar包并运行

服务器配置和Jar包上传参考[部署 Ktor 应用至云服务器 | The JetBrains Blog](https://blog.jetbrains.com/zh-hans/2020/05/29/ktor-cloud/#创建阿里云_ECS_实例)

1. 服务器安装JDK，版本与项目版本一致

   ```shell
   yum install java-11-openjdk-devel
   ```

2. 上传打包好的Jar包，运行Jar包，输出日志`msg.log`

   ```shell
   nohup java -jar ktor-sample-all.jar >msg.log 2>&1 &
   ```

3. 查看日志或者访问Api测试，可以直接关闭shell后台运行

4. 停止项目

   查找进程：

   ```shell
   ps -ef|grep java
   ```

   输出：

   ```
   root     26847     1  0 16:55 ?        00:00:12 java -jar ktor-sample-all.jar  
   ```

   找到进程ID:26847，杀死进程：

   ```shell
   kill -9 26847
   ```

   

参考：

[Creating fat JARs using the Ktor Gradle plugin | Ktor](https://ktor.io/docs/fatjar.html)

[部署 Ktor 应用至云服务器 | The JetBrains Blog](https://blog.jetbrains.com/zh-hans/2020/05/29/ktor-cloud/#创建阿里云_ECS_实例)

[Java部署jar包并后台运行 - 李宗光 - 博客园 (cnblogs.com)](https://www.cnblogs.com/lzg-blog/p/15013598.html)
