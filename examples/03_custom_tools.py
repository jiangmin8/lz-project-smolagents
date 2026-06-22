"""
Smolagents 示例 #3 - 自定义工具测试
测试自定义计算器和文件搜索工具
"""
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, '/media/lz/baba/smolagents_project')

from smolagents import CodeAgent, OpenAIServerModel
from my_tools import get_all_tools

load_dotenv("/media/lz/baba/smolagents_project/.env")

def main():
    print("=" * 50)
    print("Smolagents 自定义工具测试")
    print("=" * 50)

    model = OpenAIServerModel(
        api_base=os.getenv("LLAMA_SERVER_URL", "http://localhost:8080/v1"),
        model_id=os.getenv("LLAMA_MODEL_ID", "Qwen3-8B-Q5_K_M"),
        api_key="dummy"
    )
    print("[OK] 模型连接成功")

    # 加载自定义工具
    tools = get_all_tools()
    print(f"[OK] 加载了 {len(tools)} 个自定义工具: {[t.name for t in tools]}")

    # 创建带自定义工具的 Agent
    agent = CodeAgent(
        tools=tools,
        model=model,
        add_base_tools=True  # 同时添加基础工具
    )
    print("[OK] Agent 创建成功")

    print("\n[运行中] 测试数学计算...")
    result = agent.run("计算: 125 的平方根乘以 7，再加 100")
    print(f"\n[结果]\n{result}")

if __name__ == "__main__":
    main()
