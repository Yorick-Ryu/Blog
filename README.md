# Yorick's Blog

## 命令

```shell
# remove node_modules and reinstall dependencies:
rm -rf node_modules && npm install --force

# 1. Clear npm cache
npm cache clean --force

# 2. Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# 3. Install dependencies fresh
npm install

# 4. Install hexo-cli globally if not already installed
npm install -g hexo-cli

# 5. Try the clean command again
npm run clean
```

```shell
npm run clean    # Clean generated files
npm run build    # Generate static files
npm run server   # Start local server
npm run deploy   # Deploy your website
```

## 备注：

1. 链接命名方式为`source\_posts`里的相对路径
2. `copy_blog_images.js`文件是用来解决图片路径问题的，在build前自动运行