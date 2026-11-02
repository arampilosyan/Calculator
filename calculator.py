"""Safe scientific expression evaluator and unit conversion helpers."""
import ast
import math
import operator

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + math.sqrt(5)) / 2,
    "inf": math.inf,
}

FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
    "exp": math.exp, "factorial": math.factorial,
    "abs": abs, "round": round, "floor": math.floor,
    "ceil": math.ceil, "degrees": math.degrees, "radians": math.radians,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
}

BINARY = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}

class CalculatorError(ValueError):
    """Raised for invalid or unsafe calculator expressions."""

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise CalculatorError(f"Unknown name: {node.id}")
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise CalculatorError("Exponent is too large (maximum absolute exponent: 1000).")
        return BINARY[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY:
        return UNARY[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        if name not in FUNCTIONS or node.keywords:
            raise CalculatorError(f"Function not allowed: {name}")
        args = [_eval(arg) for arg in node.args]
        return FUNCTIONS[name](*args)
    raise CalculatorError("Invalid expression. Only numbers, operators, constants and approved functions are allowed.")

def evaluate_expression(expression):
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Enter an expression first.")
    if len(expression) > 300:
        raise CalculatorError("Expression is too long.")
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree)
        if isinstance(result, complex):
            raise CalculatorError("Complex results are not supported.")
        if isinstance(result, float) and not math.isfinite(result):
            raise CalculatorError("Result is not finite.")
        return result
    except CalculatorError:
        raise
    except ZeroDivisionError:
        raise CalculatorError("Cannot divide by zero.")
    except (SyntaxError, TypeError, ValueError, OverflowError) as exc:
        raise CalculatorError(f"Could not calculate expression: {exc}") from exc

UNIT_TABLES = {
    "Length": {"m": 1, "km": 1000, "cm": .01, "mm": .001, "mi": 1609.344, "ft": .3048, "in": .0254},
    "Mass": {"kg": 1, "g": .001, "mg": .000001, "lb": .45359237, "oz": .028349523125},
    "Time": {"s": 1, "min": 60, "h": 3600, "day": 86400},
    "Speed": {"m/s": 1, "km/h": 1/3.6, "mph": .44704},
}

def convert_units(value, source, target, category):
    if category == "Temperature":
        to_c = {"C": lambda x: x, "F": lambda x: (x - 32) * 5/9, "K": lambda x: x - 273.15}
        from_c = {"C": lambda x: x, "F": lambda x: x * 9/5 + 32, "K": lambda x: x + 273.15}
        if source not in to_c or target not in from_c:
            raise CalculatorError("Unsupported temperature unit.")
        return from_c[target](to_c[source](value))
    table = UNIT_TABLES.get(category)
    if not table or source not in table or target not in table:
        raise CalculatorError("Unsupported unit conversion.")
    return value * table[source] / table[target]
