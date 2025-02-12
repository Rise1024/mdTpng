# DeepSeek 本地化部署指南（Windows 和 macOS）

<center>两分钟教你如何在 <strong>Windows</strong> 和 <strong>macOS</strong> 系统上本地化部署 <strong>DeepSeek</strong> 系统
</center>


## 环境准备

### Windows 环境准备

1. **操作系统**: Windows 10 或更高版本。
2. **Python 版本**: 3.7 或更高版本。
   - 下载并安装 Python：[Python 官方下载]https://www.python.org/downloads/windows/。
   - 安装时勾选 `Add Python to PATH`。
3. **GPU 支持（可选）**:
   - 确保已安装 NVIDIA GPU 驱动程序。
   - 安装 CUDA Toolkit（推荐 CUDA 11.2）：[CUDA 下载]https://developer.nvidia.com/cuda-downloads。
   - 安装 cuDNN：[cuDNN 下载]https://developer.nvidia.com/cudnn。
4. **Git**: 下载并安装 Git：[Git 下载]https://git-scm.com/download/win。

### macOS 环境准备

1. **操作系统**: macOS 10.15 (Catalina) 或更高版本。
2. **Python 版本**: 3.7 或更高版本。
   - 使用 Homebrew 安装 Python：
     ```bash
     brew install python
     ```
   - 确保 Python 已添加到 PATH：
     ```bash
     echo 'export PATH="/usr/local/opt/python/libexec/bin:$PATH"' >> ~/.zshrc
     source ~/.zshrc
     ```
3. **GPU 支持（可选）**:
   - macOS 不支持 NVIDIA GPU，但可以使用 Apple 的 M1/M2 GPU（需安装 PyTorch 的 MPS 版本）。
4. **Git**: 使用 Homebrew 安装 Git：
   ```bash
   brew install git
   ```

---

## 依赖安装

1. **创建虚拟环境**:
   - Windows:
     ```bash
     python -m venv deepseek-env
     deepseek-env\Scripts\activate
     ```
   - macOS:
     ```bash
     python3 -m venv deepseek-env
     source deepseek-env/bin/activate
     ```

2. **安装 PyTorch**:
   - Windows (GPU):
     ```bash
     pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
     ```
   - macOS (M1/M2 GPU):
     ```bash
     pip install torch torchvision torchaudio
     ```

3. **安装其他依赖**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 代码获取

1. **克隆 DeepSeek 代码库**:
   ```bash
   git clone https://github.com/deepseek-ai/deepseek.git
   cd deepseek
   ```

2. **切换到稳定版本**:
   ```bash
   git checkout v1.0.0
   ```

---

## 模型下载

1. **下载预训练模型**:
   ```bash
   wget https://deepseek-model-repository.com/models/deepseek-model-v1.0.0.zip
   unzip deepseek-model-v1.0.0.zip -d models/
   ```

2. **验证模型文件**:
   ```bash
   ls models/deepseek-model-v1.0.0/
   ```

---

## 配置调整

1. **编辑配置文件**:
   打开 `config/config.yaml` 文件，根据您的环境进行调整：
   ```yaml
   model_path: "models/deepseek-model-v1.0.0"
   gpu_enabled: true  # Windows 启用 GPU，macOS 设置为 false 或使用 mps
   batch_size: 16
   ```

2. **设置环境变量**:
   - Windows:
     ```bash
     set DEEPSEEK_CONFIG_PATH=config\config.yaml
     ```
   - macOS:
     ```bash
     export DEEPSEEK_CONFIG_PATH="config/config.yaml"
     ```

---

## 服务启动

1. **启动 DeepSeek 服务**:
   ```bash
   python serve.py
   ```

2. **验证服务状态**:
   打开浏览器，访问 `http://localhost:5000/status`，确保服务正常运行。

---

## 测试与验证

1. **发送测试请求**:
   ```bash
   curl -X POST http://localhost:5000/ask -d '{"question": "What is DeepSeek?"}'
   ```

2. **检查响应**:
   确保返回的 JSON 数据包含正确的答案。

---

## 常见问题

1. **服务无法启动**:
   - 检查端口是否被占用。
   - 确保所有依赖已正确安装。

2. **模型加载失败**:
   - 检查模型路径是否正确。
   - 确保模型文件完整且未损坏。

3. **性能问题**:
   - Windows: 确保 GPU 驱动和 CUDA 版本兼容。
   - macOS: 使用 MPS 后端（需 PyTorch 1.12 或更高版本）。

---