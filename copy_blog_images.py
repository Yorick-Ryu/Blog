import os
import shutil

source_dir = "source"
target_dir = os.path.join(source_dir, "img")

def copy_images(source_dir, target_dir):
    """
    查找 source_dir 下所有子目录中的 img 文件夹，将其中的图片复制到 target_dir，重复则覆盖。
    """
    for root, dirs, files in os.walk(source_dir):
        if root.endswith("img") and root != target_dir:
            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                try:
                    shutil.copy2(source_file, target_file)  # copy2 保留文件元数据
                    print(f"已复制: {source_file} -> {target_file}")
                except Exception as e:
                    print(f"复制失败: {source_file} -> {target_file}, 错误: {e}")

if __name__ == "__main__":
    # 确保目标文件夹存在
    os.makedirs(target_dir, exist_ok=True)
    copy_images(source_dir, target_dir)
    print("图片复制完成！")