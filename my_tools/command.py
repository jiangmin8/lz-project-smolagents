"""
自定义工具：命令执行
安全执行预定义的 shell 命令（带日志）
"""
import subprocess
import logging
import os
from datetime import datetime
from smolagents import Tool

# 配置日志（使用可写目录）
LOG_DIR = "/media/lz/baba/资料/smolagents_project/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'tools.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CommandTool')

class CommandTool(Tool):
    name = "command"
    description = """
    执行预定义的 shell 命令。
    仅允许执行明确列出的安全命令。
    """
    inputs = {
        "command": {
            "type": "string",
            "description": "要执行的命令"
        },
        "args": {
            "type": "string",
            "description": "命令参数（可选）",
            "nullable": True
        }
    }
    output_type = "string"

    # 允许的命令白名单
    ALLOWED_COMMANDS = {
        'ls': ['ls'],
        'pwd': ['pwd'],
        'date': ['date'],
        'echo': ['echo'],
        'cat': ['cat'],
        'head': ['head', '-n'],
        'tail': ['tail', '-n'],
        'wc': ['wc'],
        'grep': ['grep'],
        'find': ['find'],
    }

    def forward(self, command: str, args: str = "") -> str:
        start_time = datetime.now()
        logger.info(f"[Command] 执行: {command} | 参数: {args}")

        try:
            if command not in self.ALLOWED_COMMANDS:
                logger.warning(f"[Command] 命令不在白名单: {command}")
                return f"错误: 命令 '{command}' 不在白名单中"

            cmd_parts = self.ALLOWED_COMMANDS[command].copy()

            if args:
                # 限制参数长度，防止注入
                safe_args = args[:500]
                cmd_parts.append(safe_args)

            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=10
            )

            duration = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                output = result.stdout.strip() or "命令执行成功（无输出）"
                logger.info(f"[Command] 成功 | 耗时: {duration:.3f}s")
                return output
            else:
                logger.warning(f"[Command] 失败: {result.stderr.strip()} | 耗时: {duration:.3f}s")
                return f"命令执行失败: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            logger.error(f"[Command] 超时 | 耗时: {duration:.3f}s")
            return "错误: 命令执行超时"
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[Command] 异常: {str(e)} | 耗时: {duration:.3f}s")
            return f"执行错误: {str(e)}"
