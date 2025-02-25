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


## 错误处理

### hexo d出现Permission denied (publickey). fatal: Could not read from remote repository.
git@github.com: Permission denied (publickey). fatal: Could not read from remote repository.

Collecting workspace informationFiltering to most relevant informationStill building the local workspace index, falling back to basic workspace search. Response may be less accurate.Based on the error message, it seems you're having an SSH authentication issue when trying to deploy your Hexo blog to GitHub. Here's how to fix it:


解决方法：

1. First, generate a new SSH key if you haven't already:

```sh
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. Add the SSH key to your SSH agent:

```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

3. Copy your public key:

```sh
cat ~/.ssh/id_ed25519.pub
```

4. Add this public key to your GitHub account:
   - Go to GitHub Settings > SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key

5. Test your SSH connection:

```sh
ssh -T git@github.com
```

After setting up SSH correctly, you can try deploying again using:

```sh
hexo clean && hexo deploy
```

This should resolve the "Permission denied (publickey)" error shown in your deployment attempt.

Note: Your deployment configuration in _config.yml is correct:

```yml
deploy:
- type: git
  repository: git@github.com:Yorick-Ryu/Yorick-Ryu.github.io.git
  branch: master
```