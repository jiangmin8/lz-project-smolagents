"""
自定义工具：文件搜索
在指定目录下搜索文件（带日志）
"""
import os
import logging
from datetime import datetime
from smolagents import Tool
from utils.logger import get_logger

# 获取日志器
logger = get_logger('FileSearchTool')

class FileSearchTool(Tool):
    name = "file_search"
    description = """
    在目录中搜索文件。
    可以按文件名关键词搜索，返回匹配的文件列表。
    """
    inputs = {
        "directory": {
            "type": "string",
            "description": "要搜索的目录路径"
        },
        "pattern": {
            "type": "string",
            "description": "文件名搜索关键词，如 '*.py' 或 'test'"
        }
    }
    output_type = "string"

    def forward(self, directory: str, pattern: str) -> str:
        start_time = datetime.now()
        logger.info(f"[FileSearch] 目录: {directory} | 模式: {pattern}")

        try:
            import glob

            if not os.path.isdir(directory):
                logger.warning(f"[FileSearch] 目录无效: {directory}")
                return f"错误: {directory} 不是有效目录"

            # 使用 glob 搜索
            search_pattern = os.path.join(directory, "**", f"*{pattern}*")
            files = glob.glob(search_pattern, recursive=True)

            if not files:
                logger.info(f"[FileSearch] 未找到匹配 '{pattern}' 的文件")
                return f"在 {directory} 中未找到匹配 '{pattern}' 的文件"

            # 限制返回数量
            files = files[:20]
            result = [f for f in files if os.path.isfile(f)]

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"[FileSearch] 找到 {len(result)} 个文件 | 耗时: {duration:.3f}s")

            if not result:
                return f"在 {directory} 中未找到匹配 '{pattern}' 的文件"

            return "找到以下文件:\n" + "\n".join(result)

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[FileSearch] 错误: {str(e)} | 耗时: {duration:.3f}s")
            return f"搜索错误: {str(e)}"
