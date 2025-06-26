# 填空题练习APP - 云打包版本

这是一个基于Kivy框架开发的填空题练习移动应用，支持中文显示。

## 功能特性

- 📱 移动端友好界面
- 🔤 完美支持中文字体
- 📄 支持Word文档导入
- 💡 智能答案提示
- 📊 练习统计分析
- 💾 数据持久化存储

## 云打包说明

### GitHub Actions 自动构建

1. 将此项目上传到GitHub仓库
2. 进入仓库的Actions页面
3. 运行"Build Android APK"工作流
4. 下载生成的APK文件

### Google Colab 手动构建

1. 打开提供的Colab笔记本
2. 上传项目ZIP文件
3. 运行所有单元格
4. 下载生成的APK文件

## 文件说明

- `main.py` - 应用入口文件
- `TEST_V4.0_mobile.py` - 主应用代码
- `buildozer.spec` - 构建配置文件
- `requirements.txt` - Python依赖列表
- `.github/workflows/build.yml` - GitHub Actions工作流

## 安装说明

1. 下载生成的APK文件
2. 在Android设备上启用"未知来源"安装
3. 安装APK文件
4. 享受填空题练习!

## 技术栈

- Python 3.9+
- Kivy 2.1.0
- python-docx
- Buildozer

---

构建时间: 2025-06-26 00:05:37
