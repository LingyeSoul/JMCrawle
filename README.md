# JMCrawler

一个基于 Flet 框架的 JMComic 爬虫图形界面应用程序。

## 简介

JMCrawler是一个用于下载 JMComic漫画的图形界面应用程序。它基于 [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) 库开发，提供了一个简单易用的界面来下载漫画，无需编写任何代码。

![GUI预览](https://raw.githubusercontent.com/hect0x7/JMComic-Crawler-Python/master/doc/preview.png)

## 功能特性

- 🖼️ 图形化界面操作
- 🔍 支持通过ID或URL下载漫画
- 📋 实时日志显示
- 🔄 异步下载，不阻塞界面
- 📂 自动保存漫画到本地
- 🌐 支持跨平台（Windows, macOS, Linux）
- 📖 漫画详情显示（包括封面）
- ⚙️ 可自定义配置选项

## 安装

### 环境要求

- Python >= 3.9 
- Windows, macOS 或 Linux 操作系统

### 安装步骤

1. 克隆或下载本项目:
```bash
git clone https://github.com/LingyeSoul/JMCrawler.git
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
2. 点击"下载"按钮开始下载
3. 在日志区域查看下载进度和结果


## 注意事项

1. 请合理使用，避免对服务器造成过大压力
2. 建议在下载大量漫画时添加适当的延迟
3. 请遵守当地法律法规，仅用于个人学习和研究目的

## 免责声明

### 重要提示
本项目仅供技术研究和学习使用，禁止用于任何商业用途。用户在使用本软件时必须遵守以下条款：

### 使用责任
1. 用户完全理解并同意，使用本软件下载的任何内容均受版权法保护。
2. 用户不得将通过本软件获取的内容用于商业目的或非法传播。
3. 用户应自行承担使用本软件的所有风险和责任。
4. 本软件开发者不对用户使用本软件产生的任何后果负责。

### 版权声明
1. 本软件不拥有任何漫画内容的版权。
2. 所有漫画内容的版权归其原始权利人所有。
3. 本软件仅提供技术手段，不参与任何内容的创作或分发。

### 法律合规
1. 用户在使用本软件时必须遵守所在国家/地区的所有适用法律法规。
2. 严禁使用本软件下载或传播任何侵犯第三方权益的内容。
3. 如用户违反相关法律法规，应自行承担全部法律责任。

### 技术限制
1. 本软件的功能可能因网站策略变更而失效。
2. 开发者不保证软件的持续可用性或功能完整性。
3. 用户理解并接受使用本软件可能面临的技术风险。

### 知识产权
1. 本软件基于 GPL-3.0 许可证发布，但不包括第三方库。
2. 本软件使用了 [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) 库，其版权属于原作者。
3. 本软件使用了 [Flet](https://flet.dev/) 框架，其版权属于 Flet 团队。

## 许可证

本项目基于 GPL-3.0 许可证发布，详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) - 核心爬虫库
- [Flet](https://flet.dev/) - GUI框架