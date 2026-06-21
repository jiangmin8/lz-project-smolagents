# Smolagents 项目搭建进度报告

> 创建日期：2026-06-18
> 项目路径：`/media/lz/baba/smolagents_project`
> 虚拟环境：`/media/lz/baba/smolagents_env`

---

## 项目概述

本项目基于 HuggingFace 的 Smolagents 框架，搭建本地 AI Agent 系统。

### 硬件环境

| 项目 | 配置 |
|------|------|
| GPU | RTX 3060 12GB |
| 内存 | 32GB RAM |
| CPU | i5-10400F |
| 系统 | Ubuntu 2024.04 |

### 软件环境

| 项目 | 版本/路径 |
|------|----------|
| smolagents | 1.26.0 |
| 模型 | Qwen3-8B-Q5_K_M.gguf |
| llama.cpp | `/media/lz/baba/llama.cpp/build/bin/llama-server` |
| 虚拟环境 | `/media/lz/baba/smolagents_env` |

---

## 项目结构

```
/media/lz/baba/smolagents_project/
├── .env                          # 环境配置文件
├── requirements.txt               # Python 依赖
├── config/
│   └── settings.py               # 项目设置
├── examples/
│   ├── 01_basic_agent.py        # 基础 Agent 测试
│   ├── 02_agent_with_tools.py   # 带搜索工具测试
│   ├── 03_custom_tools.py       # 自定义工具测试
│   └── 04_integrated_tools.py   # 综合工具测试
├── my_tools/
│   ├── __init__.py              # 工具加载器
│   ├── calculator.py            # 计算器工具
│   ├── file_search.py           # 文件搜索工具
│   ├── command.py               # 命令执行工具
│   └── note.py                  # 笔记管理工具
├── logs/                        # 日志目录
│   └── tools.log               # 工具调用日志
└── notes/                       # 笔记存储目录
```

---

## 完成进度

### ✅ 第一阶段：基础部署

| 任务 | 状态 | 说明 |
|------|------|------|
| 虚拟环境创建 | ✅ 完成 | `/media/lz/baba/smolagents_env` |
| smolagents 安装 | ✅ 完成 | v1.26.0 |
| 依赖安装 | ✅ 完成 | smolagents[toolkit], smolagents[mcp], smolagents[openai] |
| llama server 连接 | ✅ 完成 | 使用 Qwen3-8B-Q5_K_M |
| 基础 Agent 测试 | ✅ 完成 | 1+1=2 计算正确 |
| 搜索工具测试 | ✅ 完成 | DuckDuckGo 搜索正常 |

### ✅ 第二阶段：工具库扩展

| 工具 | 状态 | 功能 |
|------|------|------|
| CalculatorTool | ✅ 完成 | 安全数学运算（+-\*/^sqrt等） |
| FileSearchTool | ✅ 完成 | 目录文件搜索 |
| CommandTool | ✅ 完成 | 白名单命令执行 |
| NoteTool | ✅ 完成 | 笔记创建/读取 |
| 日志功能 | ✅ 完成 | 同时输出到控制台和文件 |

### 🔄 第三阶段：待开发

| 任务 | 状态 | 优先级 |
|------|------|--------|
| MCP 服务集成 | ⏳ 待开发 | P0 |
| Web UI 部署 | ⏳ 待开发 | P1 |
| 多智能体架构 | ⏳ 待开发 | P1 |
| Goose 接入 | ⏳ 待研究 | P2 |

---

## 快速开始

### 1. 激活环境

```bash
source /media/lz/baba/smolagents_env/bin/activate
```

### 2. 启动 llama server（如果未运行）

```bash
/media/lz/baba/llama.cpp/build/bin/llama-server \
  -m /media/lz/baba/model/Qwen3-8B-Q5_K_M.gguf \
  -c 4096 \
  -host 0.0.0.0 \
  -port 8080
```

### 3. 运行示例

```bash
cd /media/lz/baba/smolagents_project

# 基础测试
python examples/01_basic_agent.py

# 自定义工具测试
python examples/03_custom_tools.py

# 综合工具测试
python examples/04_integrated_tools.py
```

### 4. 查看日志

```bash
# 实时日志
tail -f /media/lz/baba/资料/smolagents_project/logs/tools.log
```

---

## 工具使用说明

### CalculatorTool（计算器）

```python
result = calculator("sqrt(125)*7 + 100")
# 结果: 178.26
```

### FileSearchTool（文件搜索）

```python
result = file_search(directory="/path/to/dir", pattern="*.py")
```

### CommandTool（命令执行）

```python
result = command(command="ls", args="-la")
```

### NoteTool（笔记管理）

```python
# 创建笔记
result = note(action="create", filename="my_note", content="笔记内容")

# 读取笔记
result = note(action="read", filename="my_note")
```

---

## 环境变量配置

`.env` 文件位于 `/media/lz/baba/smolagents_project/.env`：

```bash
LLAMA_SERVER_URL=http://localhost:8080/v1
LLAMA_MODEL_ID=Qwen3-8B-Q5_K_M
HF_TOKEN=
MCP_SERVER_PATH=
LOG_LEVEL=INFO
```

---

## 技术参考

### 官方文档

- [Smolagents 文档](https://huggingface.co/docs/smolagents)
- [GitHub](https://github.com/huggingface/smolagents)
- [官网](https://smolagents.org/)

### 核心概念

| 概念 | 说明 |
|------|------|
| CodeAgent | 以代码形式输出动作的 Agent |
| ToolCallingAgent | 传统 JSON 工具调用的 Agent |
| managed_agents | 父 Agent 管理子 Agent |

---

## 后续计划

### 近期目标

1. MCP 服务集成 - 连接现有 MCP 工具
2. Web UI 部署 - Gradio 界面
3. 工具库扩展 - 增加更多实用工具

### 长期目标

1. 多智能体协作系统
2. 与 SkillOpt 项目结合
3. 生产环境部署

---

## 常见问题

**Q: 提示 `ModuleNotFoundError: No module named 'openai'`**
A: 运行 `pip install 'smolagents[openai]'`

**Q: 提示 `OSError: [Errno 30] 只读文件系统`**
A: 日志目录在 `/media/lz/baba/资料/smolagents_project/logs`

**Q: llama server 连接失败**
A: 确保 llama server 已启动并运行在 8080 端口

---

*最后更新：2026-06-18*
