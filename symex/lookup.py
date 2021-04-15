from typing import Callable, List
from z3 import Or, And, Xor, Solver, IntVal, StringVal, BoolVal, RealVal

def get_type(t:str, env) -> Callable:
    types = {"Scalar_LNumber": int,
             "Boolean": bool,
             "Scalar_String": str,
             "Expr_Variable": env.lookup,
             "Scalar_DNumber": float}
    return types[t]


def get_const(const: str) -> List:
    "Returns a constant"
    switcher = {"True": ["Boolean", True],
                "False": ["Boolean", False]}
    return switcher[const]


def get_binop(op: str) -> Callable:
    "Returns a binary operator"
    dict = {"BooleanOr": Or,
            "BooleanAnd": And,
            "LogicalOr": Or,
            "LogicalAnd": And,
            "LogicalXor": Xor,
            "Concat": phpConcat,
            "Plus": lambda a, b: a + b,
            "Minus": lambda a, b: a - b,
            "Mul": lambda a, b: a * b,
            "Div": lambda a, b: a / b,
            "Mod": lambda a, b: a % b,
            "Equal": lambda a, b: a == b,
            "NotEqual": lambda a, b: a != b,            
            "Smaller": lambda a, b: a < b,
            "SmallerOrEqual": lambda a, b: a <= b,
            "Greater": lambda a, b: a > b,
            "GreaterOrEqual": lambda a, b: a > b}
    return(dict[op[14:]])

def phpConcat(a, b):
    if type(a) == list:
        a.append(b)
        return a
    else:
        out = [a]
        out.append(b)
        return out
