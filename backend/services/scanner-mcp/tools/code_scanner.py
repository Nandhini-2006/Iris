import ast


class VariableChecker(ast.NodeVisitor):

    def __init__(self):
        self.defined = set()
        self.used = set()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined.add(target.id)

        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

        self.generic_visit(node)


def scan_python_code(code: str) -> dict:

    try:
        tree = ast.parse(code)

    except SyntaxError as error:

        return {
            "valid_syntax": False,
            "issues": [
                {
                    "type": "SyntaxError",
                    "line": error.lineno,
                    "message": error.msg
                }
            ],
            "message": "Syntax error detected."
        }

    checker = VariableChecker()
    checker.visit(tree)

    builtin_names = {
        "print",
        "len",
        "str",
        "int",
        "float",
        "list",
        "dict",
        "set",
        "tuple",
        "range",
        "sum",
        "min",
        "max",
        "abs",
        "bool",
        "input"
    }

    undefined_variables = (
        checker.used
        - checker.defined
        - builtin_names
    )

    issues = []

    for variable in undefined_variables:
        issues.append({
            "type": "UndefinedVariable",
            "variable": variable,
            "message": f"Variable '{variable}' is used before being defined."
        })

    return {
        "valid_syntax": True,
        "issues": issues,
        "message": (
            "Undefined variables detected."
            if issues
            else "No obvious variable issues detected."
        )
    }