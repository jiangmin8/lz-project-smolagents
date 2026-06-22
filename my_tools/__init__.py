"""
工具加载器
统一管理和加载自定义工具
"""
from .calculator import CalculatorTool
from .file_search import FileSearchTool
from .command import CommandTool
from .note import NoteTool

def get_all_tools():
    """获取所有自定义工具"""
    return [
        CalculatorTool(),
        FileSearchTool(),
        CommandTool(),
        NoteTool(),
    ]

def get_tools_by_name(*names):
    """按名称获取指定工具"""
    all_tools = {tool.name: tool for tool in get_all_tools()}
    return [all_tools[name] for name in names if name in all_tools]

# 工具注册表
TOOL_REGISTRY = {
    "calculator": CalculatorTool,
    "file_search": FileSearchTool,
    "command": CommandTool,
    "note": NoteTool,
}

__all__ = [
    "CalculatorTool",
    "FileSearchTool",
    "CommandTool",
    "NoteTool",
    "get_all_tools",
    "get_tools_by_name",
    "TOOL_REGISTRY",
]
