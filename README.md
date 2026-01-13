# YOLO-POSE

这是一个基于YOLO算法的姿态估计项目，包含了YOLOv5和YOLOv7相关的训练和推理代码。

## 项目结构

- `make_dataset/`: 数据集生成相关脚本
- `test1/`: 测试代码和模型转换工具
- `train_yolo/`: YOLO模型训练代码

## 功能特性

- 支持多种YOLO模型架构（v5, v7等）
- 包含模型格式转换功能（ONNX, TensorFlow等）
- 提供数据集生成工具
- 包含训练和推理脚本

## 使用说明

具体使用方法请参考各子目录中的文档或注释。

## 上传所有文件（包括大型模型文件）

由于项目包含大型模型文件（如 .pt, .onnx, .tflite 等），我们使用Git LFS（Large File Storage）来有效管理这些文件。

### 步骤1：安装Git LFS

如果尚未安装Git LFS，请按以下步骤操作：

Windows:
```bash
# 使用Chocolatey
choco install git-lfs

# 或者从GitHub下载
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

macOS:
```bash
brew install git-lfs
```

Linux (Ubuntu/Debian):
```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

### 步骤2：配置Git LFS

在项目根目录下执行以下命令：

```bash
git lfs install
git lfs track "*.pt"
git lfs track "*.onnx"
git lfs track "*.tflite"
git lfs track "*.pb"
git lfs track "*.h5"
git lfs track "*.ckpt"
git lfs track "*.bin"
```

这将创建一个 `.gitattributes` 文件，其中列出了所有应该存储在Git LFS中的文件类型。

### 步骤3：添加并提交所有文件

```bash
git add .gitattributes
git add .
git commit -m "Add all project files including large model files"
```

### 步骤4：推送到GitHub

```bash
git push origin main
```

### 注意事项

- 上传大型文件可能需要较长时间，请耐心等待
- 如果遇到任何问题，请检查您的网络连接和GitHub访问权限
- 对于特别大的文件（超过1GB），GitHub可能有限制，您可能需要考虑使用其他存储解决方案