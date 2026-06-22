"""
Smolagents 基础示例 #1 - 最小化运行
无工具版本，测试模型连接是否正常
"""
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel

# 加载 .env 文件
load_dotenv("/media/lz/baba/smolagents_project/.env")

def main():
    print("=" * 50)
    print("Smolagents 基础测试")
    print("=" * 50)

    # 连接到你的 llama server
    model = OpenAIServerModel(
        api_base=os.getenv("LLAMA_SERVER_URL", "http://localhost:8080/v1"),
        model_id=os.getenv("LLAMA_MODEL_ID", "Qwen3-8B-Q5_K_M"),
        api_key="dummy"  # llama server 不需要真实 key
    )
    print(f"[OK] 模型连接: {os.getenv('LLAMA_SERVER_URL')}")

    # 创建 Agent（无工具，纯测试）
    agent = CodeAgent(tools=[], model=model)
    print("[OK] Agent 创建成功")

    # 运行测试
    print("\n[运行中] 发送测试请求...")
    result = agent.run("请用中文回复：1+1等于几？")
    print(f"\n[结果]\n{result}")

if __name__ == "__main__":
    main()