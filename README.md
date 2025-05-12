# 🧠 GPT-YAML 小工具平台

这是一个基于 Flask 构建的轻量级 Web 工具，用于上传、下载和管理 `.yaml` / `.yml` 文件，并通过 `ngrok` 快速创建公网访问链接。

---

## ✨ 项目亮点

- ✅ 登录分权限（管理员 / 访客）
- 📁 支持上传 YAML 文件（仅限 `.yaml` / `.yml`）
- 🌍 自动启动 `ngrok` 暴露本地端口
- 🔗 自动生成 **is.gd 短链接**（还能自定义）
- 📋 一键复制短链，发人超方便
- 🧽 管理员可删除上传文件
- 🔐 密码简单配置（硬编码，适合内部使用）

---

## 📦 使用方式

### 🖥 本地运行

> 请先安装依赖：

```bash
pip install flask requests pyperclip
python gptyaml.py
