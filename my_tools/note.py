"""
自定义工具：笔记工具
创建和管理文本笔记（带日志）
"""
import os
import logging
from datetime import datetime
from smolagents import Tool
from utils.logger import get_logger

# 获取日志器
logger = get_logger('NoteTool')

class NoteTool(Tool):
    name = "note"
    description = """
    创建、读取和管理文本笔记。
    可以创建新笔记或读取现有笔记内容。
    """
    inputs = {
        "action": {
            "type": "string",
            "description": "操作类型: 'create' 创建笔记, 'read' 读取笔记"
        },
        "filename": {
            "type": "string",
            "description": "笔记文件名（不含扩展名）"
        },
        "content": {
            "type": "string",
            "description": "笔记内容（仅创建时需要）",
            "nullable": True
        },
        "notes_dir": {
            "type": "string",
            "description": "笔记存储目录（可选，默认为 ./notes）",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, action: str, filename: str, content: str = "", notes_dir: str = "./notes") -> str:
        start_time = datetime.now()
        logger.info(f"[Note] 操作: {action} | 文件: {filename} | 目录: {notes_dir}")

        try:
            # 创建目录（如果不存在）
            os.makedirs(notes_dir, exist_ok=True)

            file_path = os.path.join(notes_dir, f"{filename}.txt")

            if action == "create":
                with open(file_path, 'w', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"创建时间: {timestamp}\n\n")
                    f.write(content)
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"[Note] 创建成功: {file_path} | 耗时: {duration:.3f}s")
                return f"笔记已创建: {file_path}"

            elif action == "read":
                if not os.path.exists(file_path):
                    logger.warning(f"[Note] 文件不存在: {file_path}")
                    return f"笔记不存在: {file_path}"

                with open(file_path, 'r', encoding='utf-8') as f:
                    note_content = f.read()
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"[Note] 读取成功: {file_path} | 耗时: {duration:.3f}s")
                return f"笔记内容 ({file_path}):\n\n{note_content}"

            else:
                logger.warning(f"[Note] 未知操作: {action}")
                return f"未知操作: {action}，支持: create, read"

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[Note] 错误: {str(e)} | 耗时: {duration:.3f}s")
            return f"笔记操作错误: {str(e)}"
