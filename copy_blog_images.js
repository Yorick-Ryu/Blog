// javascript
const fs = require('fs-extra');
const path = require('path');

const sourceDir = 'source';
const targetDir = path.join(sourceDir, 'img');

async function copyImages(sourceDir, targetDir) {
  /**
   * 查找 sourceDir 下所有子目录中的 img 文件夹，将其中的图片复制到 targetDir，重复则覆盖。
   */
  async function walk(dir) {
    const files = fs.readdirSync(dir);

    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        if (filePath.endsWith('img') && filePath !== targetDir) {
          const imageFiles = fs.readdirSync(filePath);
          for (const imageFile of imageFiles) {
            const sourceFile = path.join(filePath, imageFile);
            const targetFile = path.join(targetDir, imageFile);
            try {
              await fs.copy(sourceFile, targetFile, { overwrite: true }); // copy 保留文件元数据
              console.log(`已复制: ${sourceFile} -> ${targetFile}`);
            } catch (e) {
              console.log(`复制失败: ${sourceFile} -> ${targetFile}, 错误: ${e}`);
            }
          }
        } else {
          await walk(filePath);
        }
      }
    }
  }

  await walk(sourceDir);
}

async function main() {
  // 确保目标文件夹存在
  fs.ensureDirSync(targetDir);
  await copyImages(sourceDir, targetDir);
  console.log('图片复制完成！');
}

main();