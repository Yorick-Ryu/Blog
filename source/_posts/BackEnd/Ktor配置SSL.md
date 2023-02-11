---
title: Ktor配置SSL
tags:
  - ktor
index_img: /img/default.png
categories:
  - BackEnd
date: 2023-01-26 22:37:45
sticky:
---

#  Ktor配置SSL实现https

参考：

[SSL and certificates | Ktor](https://ktor.io/docs/ssl.html)

[SSL - 快速入门 - Ktor (kotlincn.net)](https://ktor.kotlincn.net/quickstart/guides/ssl.html)

## 生成SSL证书

我直接在阿里云白嫖了免费SSL证书：[选购SSL证书 (aliyun.com)](https://promotion.aliyun.com/ntms/act/sslbuy.html)

选择`jks`格式并下载解压

应该有一个`xxx.jks`文件和一个`jks-password.txt`密钥文件

## 查看证书别名(keyAlias)

1. 找到电脑的JDK路径
2. 在`\bin`中找到`keytool.exe`复制到证书所在目录
3. 在证书所在目录运行cmd
4. 输入`keytool -list -v -keystore file.jks -storepass password`，其中`file.jks`是证书名字，`password`要用密钥来代替。

## 在Ktor中配置SSL

首先，打开`application.conf`

1. 添加`sslPort`

   ```conf
   ktor {
       deployment {
           sslPort = 8443
       }
   }
   ```

2. 添加security组，`keyStore`为证书路径，本地放在项目根目录，服务器和Jar包同级。

   `keyAlias`填入证书别称

   `keyStorePassword`和`privateKeyPassword`填入证书密码

   ```conf
   ktor {
       security {
           ssl {
               keyStore = keystore.jks
               keyAlias = sampleAlias 
               keyStorePassword = foobar
               privateKeyPassword = foobar
           }
       }
   }
   ```

3. 重新生成Jar包并上传到服务器，同时上传jks证书文件，和Jar包在同级目录。

   参考：[Ktor部署到云服务器](https://yorick.love/2023/01/26/BackEnd/Ktor部署到云服务器/

