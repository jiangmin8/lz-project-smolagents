"""
测试用例：验证配置环境变量功能
"""
import os
import sys
from unittest.mock import patch

# 添加项目路径到sys.path
sys.path.insert(0, '/media/lz/baba/smolagents_project')

from config.settings import config


def test_local_model_path_with_env_var():
    """测试LOCAL_MODEL_PATH环境变量设置"""
    # 设置环境变量
    with patch.dict(os.environ, {'LOCAL_MODEL_PATH': '/custom/model/path.gguf'}):
        # 重新导入配置以确保环境变量生效
        import importlib
        import config.settings
        importlib.reload(config.settings)
        from config.settings import config
        
        # 验证环境变量被正确读取
        assert config.LOCAL_MODEL_PATH == '/custom/model/path.gguf'
        print("✓ LOCAL_MODEL_PATH 环境变量设置正确")


def test_local_model_path_fallback():
    """测试LOCAL_MODEL_PATH默认值回退"""
    # 清除环境变量
    with patch.dict(os.environ, {}, clear=True):
        # 重新导入配置以确保环境变量生效
        import importlib
        import config.settings
        importlib.reload(config.settings)
        from config.settings import config
        
        # 验证默认值被正确使用
        assert config.LOCAL_MODEL_PATH == '/media/lz/baba/model/Qwen3-8B-Q5_K_M.gguf'
        print("✓ LOCAL_MODEL_PATH 默认值回退正确")


def test_other_env_vars():
    """测试其他环境变量是否正常工作"""
    # 测试LLAMA_SERVER_URL环境变量
    with patch.dict(os.environ, {'LLAMA_SERVER_URL': 'http://custom-server:8080/v1'}):
        import importlib
        import config.settings
        importlib.reload(config.settings)
        from config.settings import config
        
        assert config.LLAMA_SERVER_URL == 'http://custom-server:8080/v1'
        print("✓ LLAMA_SERVER_URL 环境变量设置正确")


if __name__ == "__main__":
    print("开始测试配置环境变量功能...")
    test_local_model_path_with_env_var()
    test_local_model_path_fallback()
    test_other_env_vars()
    print("所有测试通过！")