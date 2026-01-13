# 完整项目同步指南

此指南将帮助您将本地YOLO-POSE项目的所有文件同步到GitHub仓库，包括大型文件。

## 当前项目结构

```
YOLO-POSE/
├── README.md
├── .gitignore
├── .gitattributes
├── UPLOAD_GUIDE.md
├── make_dataset/
│   ├── generate_rings.py
│   ├── generate_rings2.py
│   └── generate_rings3.py
├── test1/
│   ├── train.py
│   ├── TFLite.py
│   ├── generate1.py
│   ├── transonnx.py
│   ├── transtensorflow.py
│   ├── best.pt (3613.2KB)
│   ├── ring_model.onnx (4702.5KB)
│   ├── ring_model.tflite (1186.0KB)
│   ├── ring_dataset/ (包含图像和标签文件)
│   ├── ring_saved_model/ (包含SavedModel格式模型)
│   └── yolov5/ (完整的YOLOv5项目)
└── train_yolo/
    └── train.py
```

## 同步步骤

### 1. 克隆远程仓库到本地

```bash
git clone https://github.com/Jackie-damn/YOLO-POSE.git
cd YOLO-POSE
```

### 2. 复制本地项目文件到仓库目录

将你的本地项目文件复制到克隆的仓库目录中：

```bash
# 复制 make_dataset 目录
cp -r /path/to/local/project/make_dataset/* ./make_dataset/

# 复制 test1 目录
cp -r /path/to/local/project/test1/* ./test1/

# 复制 train_yolo 目录
cp -r /path/to/local/project/train_yolo/* ./train_yolo/
```

### 3. 确保Git LFS已正确配置

```bash
git lfs install
```

### 4. 添加所有文件到Git

```bash
git add .
```

### 5. 检查哪些文件被Git LFS跟踪

```bash
git lfs ls-files
```

### 6. 提交更改

```bash
git commit -m "Add all project files including large model files"
```

### 7. 推送到远程仓库

```bash
git push origin main
```

## 处理大型文件的注意事项

1. **文件大小限制**：
   - GitHub对单个文件大小限制为100MB
   - 仓库总大小不应超过1GB（软限制）
   
2. **Git LFS配额**：
   - 免费账户每月有1GB的流量和1GB的存储空间
   - 如果您的模型文件较大，可能需要考虑云存储服务

3. **替代方案**：
   如果您的模型文件过大，可以考虑：
   - 将大型模型文件存储在云存储服务中，并在README中提供下载链接
   - 使用模型压缩技术减小文件大小
   - 分割大型文件为多个较小的部分

## 验证上传

上传完成后，检查仓库以确保所有文件都已正确上传：

```bash
git log -p --name-status HEAD~1..HEAD
```

## 故障排除

如果遇到"remote: fatal: protocol error"或"pack exceeds maximum allowed size"错误：

1. 修改Git配置增加缓冲区大小：
```bash
git config http.postBuffer 524288000  # 500MB buffer
```

2. 如果仍有问题，可能需要删除某些大型文件并提供下载链接：
```bash
# 删除特定大文件
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch path/to/large/file" \
--prune-empty --tag-name-filter cat -- --all
```

完成后，重新执行上述步骤。

## 最佳实践

1. 保持模型文件与代码分离
2. 在README中提供模型文件的下载链接
3. 定期清理不必要的历史记录以减少仓库大小
4. 使用语义化版本控制标记重要发布点