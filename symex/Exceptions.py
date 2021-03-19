from typing import Dict
from .Environment import Environment

class SError(Exception):
    """Base class for symbolic execution errors"""
    pass

class ExpressionError(SError):
    def __init__(self, ast: Dict, env: Environment):
        print(f"Failed expression: {ast}")
        print(f"Environment: {str(env)}")
