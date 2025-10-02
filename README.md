# JMComic Crawler GUI

一个基于 Flet 框架的 JMComic 爬虫图形界面应用程序。

## 简介

JMComic Crawler GUI 是一个用于下载 JMComic（禁漫天堂）漫画的图形界面应用程序。它基于 [JMComic-Python](https://github.com/hect0x7/JMComic-Crawler-Python) 库开发，提供了一个简单易用的界面来下载漫画，无需编写任何代码。

![GUI预览](https://raw.githubusercontent.com/hect0x7/JMComic-Crawler-Python/master/assets/gui_preview.png)

## 功能特性

- 🖼️ 图形化界面操作
- 🔍 支持通过ID或URL下载漫画
- 📋 实时日志显示
- 🔄 异步下载，不阻塞界面
- 📂 自动保存漫画到本地
- 🌐 支持跨平台（Windows, macOS, Linux）

## 安装

### 环境要求

- Python >= 3.7 (推荐 3.9+)
- Windows, macOS 或 Linux 操作系统

### 安装步骤

1. 克隆或下载本项目:
```bash
git clone https://github.com/your-username/JMComic-Crawler-GUI.git
cd JMComic-Crawler-GUI
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

或者使用 uv (推荐):
```bash
pip install uv
uv pip install -r requirements.txt
```

3. 安装 JMComic 库:
```bash
pip install jmcomic
```

## 使用方法

运行应用程序:
```bash
flet run
```

或者直接运行 Python 文件:
```bash
python src/main.py
```

### 下载漫画

1. 在输入框中输入漫画的ID或完整URL
   - 示例ID: `422866`
   - 示例URL: `https://jmcomic.me/album/422866`

2. 点击"下载"按钮开始下载

3. 在日志区域查看下载进度和结果

## 配置选项

JMComic 支持丰富的配置选项，可以通过创建 `option.yml` 文件来自定义下载行为：

```yaml
download:
  image:
    suffix: .png
client:
  impl: api
```

更多配置选项请参考 [JMComic官方文档](https://jmcomic.readthedocs.io/zh-cn/latest/)

## 注意事项

1. 请合理使用，避免对服务器造成过大压力
2. 建议在下载大量漫画时添加适当的延迟
3. 请遵守当地法律法规，仅用于个人学习和研究目的

## 许可证

本项目基于 MIT 许可证发布，详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- [JMComic-Python](https://github.com/hect0x7/JMComic-Crawler-Python) - 核心爬虫库
- [Flet](https://flet.dev/) - GUI框架