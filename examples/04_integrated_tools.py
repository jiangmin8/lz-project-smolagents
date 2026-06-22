"""
Smolagents 示例 #4 - 综合工具测试
测试笔记创建和文件搜索
"""
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, '/media/lz/baba/smolagents_project')

from smolagents import CodeAgent, OpenAIServerModel, DuckDuckGoSearchTool
from my_tools import get_all_tools

load_dotenv("/media/lz/baba/smolagents_project/.env")

def main():
    print("=" * 50)
    print("Smolagents 综合工具测试")
    print("=" * 50)

    model = OpenAIServerModel(
        api_base=os.getenv("LLAMA_SERVER_URL", "http://localhost:8080/v1"),
        model_id=os.getenv("LLAMA_MODEL_ID", "Qwen3-8B-Q5_K_M"),
        api_key="dummy"
    )

    # 合并所有工具
    all_tools = get_all_tools()
    all_tools.append(DuckDuckGoSearchTool())

    agent = CodeAgent(
        tools=all_tools,
        model=model,
        add_base_tools=False  # 我们已经手动添加了需要的工具
    )
    print(f"[OK] Agent 创建成功，共 {len(all_tools)} 个工具")

    # 测试任务
    task = """完成以下任务：
    1. 用计算器验证：2^10 等于多少
    2. 在当前目录下搜索所有 .py 文件
    3. 创建一个名为 'test_note' 的笔记，内容是 '这是测试笔记'
    """
    print(f"\n[运行中] 执行任务...")
    result = agent.run(task)
    print(f"\n[结果]\n{result}")

if __name__ == "__main__":
    main()
