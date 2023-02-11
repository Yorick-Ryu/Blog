---
title: Python实用脚本收集
index_img: /img/default.png
categories: 
  - Python
date: 2022-04-21 16:50:41
tags: 
  - Script
sticky: 
---

# python实用脚本收集

## 图片压缩

BUG:部分图片压缩后体积反而变大
```python
from PIL import Image
import os

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile, outfile='', mb=400, step=10, quality=90):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)
    
def resize_image(infile, outfile='', x_s=1376):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    outfile = get_outfile(infile, outfile)
    out.save(outfile)


if __name__ == '__main__':
    # 这里填写图片的路径和输出路径
    compress_image(r"E:\download\yorick.love.png")
   #resize_image(r'D:\learn\space.jpg')
```

## QQ/TimOCR转md表格

```python
# 将表格内容的QCR文本结果还原为Markdown文档的表格格式
# 暂不支持空单元格
# 使用方法：
# 1. 运行脚本
# 2. 用QQ/Tim的OCR识别表格内容并复制
# 3. 按下快捷键 shift+alt+表格列数（2~4）
# 4. 粘贴文本
import pyperclip, keyboard

def formatTable(columnNum):
    # 获取剪贴板内容
    raw = pyperclip.paste()
    # 按行分割
    raw = raw.replace("\r", "")
    rawLine = raw.split("\n")

    # 接受结果
    tableLine = []

    for i in range(len(rawLine)):

        # 加入制表符
        if i == columnNum:
            tableLine.append(columnNum * "|---" + "|\n")

        if i % columnNum == 0:
            # 如果是第一列
            tableLine.append("|" + rawLine[i] + "|")
        elif i % columnNum == columnNum - 1:
            # 如果是最后一列
            tableLine.append(rawLine[i] + "|" + "\n")
        else:
            # 普通列
            tableLine.append(rawLine[i] + "|")

    # print("".join(tableLine))
    # 写入剪切板
    pyperclip.copy("".join(tableLine))

if __name__ == "__main__":
    keyboard.add_hotkey("shift+alt+2", formatTable, args=(2,))
    keyboard.add_hotkey("shift+alt+3", formatTable, args=(3,))
    keyboard.add_hotkey("shift+alt+4", formatTable, args=(4,))
    keyboard.record("shift+alt+1")

```

## hexo博客格式化

```python
# 将任意路径下的所有md文档格式化为Hexo博客并转移到Hexo目录下，同时转移图片文件
import os
import re
import datetime

# md文档路径
md_path = r"C:\Users\yurui\Desktop\Coding_Note\python_note"
# 获取文档名的正则表达式，例如“24_Python脚本.md”，提取后为Python脚本
re_file_name = r"[0-9]*_(.+?).md"
# 获取文档内容中图片路径的表达式
re_img_name = r"!\[.*\]\((.+?)\)"
# 博客首页图默认路径
img_default_url = r"/img/default.png"
# 定义默认分类
categories = "Python"
# 博客路径
post_url = r"D:\Blog\source\_posts"
# 前缀
prefix = "Python"

# 获取md文档并格式化
def format(md_path):
    # 得到文件夹下的所有文件名称，返回列表
    files = os.listdir(md_path)
    # 遍历每个文件
    for file_name in files:
        # 保存博客头信息
        heads_list = [
            "---\n",
            "title: {title}\n",
            "index_img: {img_path}\n",
            "categories: \n",
            "  - {categories}\n",
            "date: {time}\n",
            "tags: \n",
            "  - \n",
            "sticky: \n",
            "---\n",
        ]
        # 获取文件绝对路径
        file_path = md_path + "/" + file_name
        # 判断是否是文件
        if os.path.isfile(file_path) and file_name.split(".")[1] == "md":
            # 获取blog名称
            blog_name = re.findall(re_file_name, file_name)
            if len(blog_name) == 1:
                blog_name = blog_name[0]
            else:
                blog_name = file_name.split(".")[0]
            # 获取blog首图
            with open(file_path, "r", encoding="utf-8") as f:
                # 获取文件全部内容
                content = f.read()
                # 正则匹配
                img_url = re.findall(re_img_name, content)
                if len(img_url) > 0:
                    img_url = img_url[0]
                else:
                    img_url = img_default_url
            # 将assets替换为img
            img_url = img_url.replace("assets", "img")
            # 获取文件创建日期
            blog_time = int(os.path.getctime(file_path))
            blog_time = datetime.datetime.fromtimestamp(blog_time)

            heads_list[1] = heads_list[1].format(title=blog_name)
            heads_list[2] = heads_list[2].format(img_path=img_url)
            heads_list[4] = heads_list[4].format(categories=categories)
            heads_list[5] = heads_list[5].format(time=blog_time)

            for li in heads_list:
                print(li)
            flag = input("本博客头信息如上所示，是否修改？\n 0.完美，1.标题，2.图片路径，3.分类  ")
            while flag != "0":
                if flag == "1":
                    heads_list[1] = "title: {0}".format(input("请输入标题，回车后输入 0 提交："))
                elif flag == "2":
                    heads_list[2] = "index_img: {0}".format(
                        input("请输入图片路径，回车后输入 0 提交：")
                    )
                elif flag == "3":
                    heads_list[4] = "  - {0}".format(input("请输入分类，回车后输入 0 提交："))
                for li in heads_list:
                    print(li)
                flag = input("本博客头信息如上所示，是否修改？\n 0.完美，1.标题，2.图片路径，3.分类  ")

            # 获取博客
            blog_body = []
            with open(file_path, "r+", encoding="utf-8") as f:
                blog_body = f.readlines()

            # 将head写入博客头
            heads_list.append("\n")
            heads_list.reverse()
            for line in heads_list:
                blog_body.insert(0, line)

            # 批量替换关键词

            # 写入博客
            blog_url = post_url + "/" + prefix +blog_name + ".md"
            with open(blog_url, "w", encoding="utf-8") as f:
                f.writelines(blog_body)

            print(f"写入成功，博客路径：{blog_url}")


format(md_path)

# BUG
# 文章内图片路径没改
# 图片资源文件夹没有迁移
# 修改文章名称是文件名称不变
```