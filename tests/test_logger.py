"""
测试用例：验证统一日志模块
"""
import os
import sys

# 添加项目路径到sys.path
sys.path.insert(0, '/media/lz/baba/smolagents_project')

from utils.logger import get_logger


def test_logger_creation():
    """测试日志模块创建"""
    # 创建日志器
    logger = get_logger('test_module')
    
    # 验证日志器存在
    assert logger is not None
    print("✓ 日志器创建成功")


def test_logger_functionality():
    """测试日志功能"""
    logger = get_logger('test_functionality')
    
    # 测试日志输出
    logger.info("测试日志消息")
    
    print("✓ 日志功能正常")


if __name__ == "__main__":
    print("开始测试统一日志模块...")
    test_logger_creation()
    test_logger_functionality()
    print("所有测试通过！")