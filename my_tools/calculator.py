"""
自定义工具：计算器
安全执行数学运算（带日志）
"""
import os
import logging
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
logger = logging.getLogger('CalculatorTool')

class CalculatorTool(Tool):
    name = "calculator"
    description = """
    使用计算器进行数学运算。
    支持: 加减乘除、幂运算、开方、取模等。
    """
    inputs = {
        "expression": {
            "type": "string",
            "description": "数学表达式，如 '2+3*4'、'sqrt(16)'、'10%3'"
        }
    }
    output_type = "string"

    def forward(self, expression: str) -> str:
        start_time = datetime.now()
        logger.info(f"[Calculator] 输入表达式: {expression}")

        try:
            # 安全评估（只允许数学运算）
            import ast
            import operator
            import math

            # 限制支持的运算符和函数
            allowed_ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.USub: operator.neg,
            }

            allowed_names = {
                'sqrt': math.sqrt,
                'abs': abs,
                'round': round,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'pi': math.pi,
                'e': math.e,
            }

            def safe_eval(node):
                if isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                        return node.value
                    raise ValueError(f"不支持的常量: {node.value}")
                elif isinstance(node, ast.Name):
                    if node.id in allowed_names:
                        return allowed_names[node.id]
                    raise ValueError(f"不支持的函数/常量: {node.id}")
                elif isinstance(node, ast.BinOp):
                    left = safe_eval(node.left)
                    right = safe_eval(node.right)
                    return allowed_ops[type(node.op)](left, right)
                elif isinstance(node, ast.UnaryOp):
                    return allowed_ops[type(node.op)](safe_eval(node.operand))
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in allowed_names:
                        args = [safe_eval(arg) for arg in node.args]
                        return allowed_names[node.func.id](*args)
                raise ValueError(f"不支持的操作: {ast.dump(node)}")

            tree = ast.parse(expression, mode='eval')
            result = safe_eval(tree.body)

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"[Calculator] 结果: {result} | 耗时: {duration:.3f}s")

            return str(result)

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[Calculator] 错误: {str(e)} | 耗时: {duration:.3f}s")
            return f"计算错误: {str(e)}"
