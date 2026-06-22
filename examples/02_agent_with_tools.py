"""
Smolagents 示例 #2 - 带搜索工具
测试工具调用功能
"""
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel, DuckDuckGoSearchTool

load_dotenv("/media/lz/baba/smolagents_project/.env")

def main():
    print("=" * 50)
    print("Smolagents 工具测试")
    print("=" * 50)

    model = OpenAIServerModel(
        api_base=os.getenv("LLAMA_SERVER_URL", "http://localhost:8080/v1"),
        model_id=os.getenv("LLAMA_MODEL_ID", "Qwen3-8B-Q5_K_M"),
        api_key="dummy"  # llama server 不需要真实 key
    )
    print("[OK] 模型连接成功")

    # 创建带搜索工具的 Agent
    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        add_base_tools=True
    )
    print("[OK] Agent + 工具创建成功")

    print("\n[运行中] 发送搜索请求...")
    result = agent.run("搜索今天的热搜新闻，用中文列出前5条")
    print(f"\n[结果]\n{result}")

if __name__ == "__main__":
    main()