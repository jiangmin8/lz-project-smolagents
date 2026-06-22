#!/usr/bin/env python3
"""
测试日志功能的简单脚本
"""
import sys
sys.path.insert(0, '/media/lz/baba/smolagents_project')

# 测试导入和基本功能
from utils.logger import get_logger

# 测试日志功能
logger = get_logger('test_integration')
logger.info("测试日志功能正常工作")

print("日志功能测试完成")