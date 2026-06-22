"""
Smolagents 配置文件
"""
import os

class Config:
    # ===== 项目基础路径 =====
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
    
    # ===== 模型配置 =====
    # 方式A: llama server
    LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL", "http://localhost:8080/v1")
    LLAMA_MODEL_ID = os.getenv("LLAMA_MODEL_ID", "Qwen3-8B-Q5_K_M")

    # 方式B: 本地模型路径 (Transformers直接加载)
    LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "/media/lz/baba/model/Qwen3-8B-Q5_K_M.gguf")

    # ===== 安全配置 =====
    ADDITIONAL_AUTHORIZED_IMPORTS = ['requests', 'bs4', 'json', 're', 'math', 'datetime', 'collections']

    # ===== 执行限制 =====
    MAX_STEPS = 30
    MAX_TIME = 120  # 秒

    # ===== MCP 配置 =====
    MCP_SERVER_PATH = os.getenv("MCP_SERVER_PATH", "")

    # ===== 日志 =====
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.path.join(LOGS_DIR, "agent.log")

    # ===== 工具配置 =====
    ADD_BASE_TOOLS = True

config = Config()