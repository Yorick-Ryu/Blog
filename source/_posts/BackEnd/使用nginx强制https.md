---
title: 使用nginx强制https
tags:
  - Nginx
index_img: /img/default.png
categories:
  - BackEnd
date: 2023-01-12 20:35:02
sticky: 
---

如果没有服务器可以点击[这里](https://www.aliyun.com/minisite/goods?userCode=cucsy8ip)购买，新用户超低价！

ssl证书购买及安装请参考：

[在Nginx或Tengine服务器上安装证书 (aliyun.com)](https://help.aliyun.com/document_detail/98728.htm?spm=a2c4g.11186623.0.0.4c58310323WzTm#concept-n45-21x-yfb)

1. 进入nginx的服务器配置文件夹，默认在`/etc/nginx`

   ```shell
   cd /etc/nginx
   ```

2. 安装tree（非必要，可略过）

   ```shell
   sudo yum install tree
   ```

3. 使用tree查看nginx的目录结构

   ```shell
   tree
   ```

   我的输出如下：

   ```shell
   .
   ├── cert # 这里放证书和密钥
   │   ├── yorick.love.key
   │   └── yorick.love.pem
   ├── conf.d # 这里是配置文件夹，放各个应用的服务器配置
   │   └── hexo.conf
   ├── default.d 
   ├── fastcgi.conf
   ├── fastcgi.conf.default
   ├── fastcgi_params
   ├── fastcgi_params.default
   ├── koi-utf
   ├── koi-win
   ├── mime.types
   ├── mime.types.default
   ├── nginx.conf # 这里是主配置
   ├── nginx.conf.default
   ├── scgi_params
   ├── scgi_params.default
   ├── uwsgi_params
   ├── uwsgi_params.default
   └── win-utf
   ```

4. 由于我这里就一个应用，直接在主配置修改，应用配置注释掉。

   用vim命令编辑主配置

   ```shell
   vim nginx.conf
   ```

   注释掉原来监听80端口的server

   ```shell
   #    server {
   #        listen       80;
   #        listen       [::]:80;
   #        server_name  _;
   #        root         /usr/share/nginx/html;
   #
   #        # Load configuration files for the default server block.
   #        include /etc/nginx/default.d/*.conf;
   #
   #        error_page 404 /404.html;
   #        location = /404.html {
   #        }
   #
   #        error_page 500 502 503 504 /50x.html;
   #        location = /50x.html {
   #        }
   #    }
   ```

   **如何注释多行：**

   - 首先按`esc`进入命令行模式下，按下`Ctrl + V`，进入列（也叫区块）模式;

   - 在行首使用上下键选择需要注释的多行;

   - 按下键盘（大写）`“I”`键，进入插入模式；

   - 然后输入注释符（`“//”、“#”`等）;

   - 最后按下`“Esc”`键，稍等一会。

5. 修改监听443端口的配置：

   ```shell
   server {
       listen       443 ssl http2;
       server_name  yorick.love; // 网站域名或者ip
       root         /var/www/hexo; // 静态资源目录
   
       ssl_certificate cert/yorick.love.pem; // 证书相对路径
       ssl_certificate_key cert/yorick.love.key; // 密钥相对路径
       ssl_session_cache shared:SSL:1m;
       ssl_session_timeout 5m;
       ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
       ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;
   
       # Load configuration files for the default server block.
       include /etc/nginx/default.d/*.conf;
   
       error_page 404 /404.html;
       location = /40x.html {
       }
   
       error_page 500 502 503 504 /50x.html;
       location = /50x.html {
       }
   }
   ```

6. 最后，转发80端口的请求：

   ```shell
   server {
       listen  80;
       server_name  yorick.love; // 域名或者IP
   
       return 301 https://$host$request_uri; // 固定不用修改
   }
   ```
   
   
   
   

