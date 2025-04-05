# ILoveScratch记事本

一个基于PyQt5开发的轻量级记事本应用程序，提供基本的文本编辑功能和便捷的操作体验。

## 功能特性

- ✅ 新建/打开/保存文本文件（支持多种编码格式）
- ⌨ 常用编辑功能：撤销、重做、复制、粘贴、全选
- ⚙ 格式设置：字体选择、颜色设置、自动换行
- 🔎 查找替换功能（支持向前/向后查找）
- 📔 打印支持（包含页面设置选项）
- ℹ️ 帮助信息与关于页面
- 🕹 智能编码检测（自动识别GBK/UTF-8等编码）

## 安装指南

### 环境要求
- Python 3.7+

### 依赖要求
- PyQt5
- chardet

```bash
pip install PyQt5 chardet pyperclip
```

### 运行程序
```bash
python main.py
```

## 项目结构
```
Notepad/
├── main.py              # 程序入口
├── ui.py                # 主界面逻辑
├── about.py             # 关于页面
├── resources/           # 图标资源
├── requirements.txt     # 依赖列表
└── README.md            # 本说明文件
```

## 使用说明
1. 通过菜单栏或工具栏按钮进行文件操作
2. 使用Ctrl+Z/Ctrl+Y进行撤销重做
3. 右键菜单提供常用编辑功能
4. 格式菜单可设置字体样式和文本颜色
5. 状态栏实时显示编码格式和字数统计

## 版本信息
当前版本：0.7.0 Beta

## 开源协议
[GNU General Public License v3.0](LICENSE)