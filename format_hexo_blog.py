# 将任意路径下的所有md文档格式化为Hexo博客并转移到Hexo目录下，同时转移图片文件
import os
import re
import datetime

# md文档路径
md_path = r"C:\Users\yurui\Desktop\Coding_Note\python_note"
# 获取文档名的正则表达式
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
# 资源文件夹没有迁移
# 修改文章名称是文件名称不变
