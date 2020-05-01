"""Main parser and compile function."""
from collections import deque
from typing import Dict, List, Optional

from .definition import (
    NETWORKX_OPERATORS_REGISTERY,
    Evaluator,
    ItemAST,
    OperatoryArity,
    ParserException,
    operator_factory,
)
from .operator import *  # noqa: F401,F403

__all__ = ["parse", "explain", "compile_ast"]


def _check_item_ast(item: ItemAST, stack: deque) -> ItemAST:
    (compliant, delta) = item.check_arity()
    if not compliant:
        raise ParserException(f'Invalid parameters for "{item.op.name}" operator ({delta} #parameters)', stack)
    # if not item.check_profile():
    #    raise ParserException(f'Invalid type parameters for "{item.op.name}" operator', stack)
    return item


def parse(expra: Dict, stack: Optional[deque] = None) -> ItemAST:
    """Tranform json query into Item AST."""
    result = []
    _stack = stack if stack else deque()

    _stack.append(expra)
    for (op, v) in expra.items():
        if op not in NETWORKX_OPERATORS_REGISTERY:
            raise ParserException(f'Unsupported "{op}" operator', _stack)
        operator = NETWORKX_OPERATORS_REGISTERY[op]

        if operator.combinator:
            args = []
            # shortcut List declaration as single item
            items = v if isinstance(v, List) else [v]
            for item in items:
                args.append(parse(item, _stack))
            result.append(_check_item_ast(ItemAST(op=operator, args=args), _stack))

        else:
            result.append(_check_item_ast(ItemAST(op=operator, args=[v] if not isinstance(v, List) else v), _stack))

    _stack.pop()
    return result[0] if len(result) == 1 else ItemAST(op=NETWORKX_OPERATORS_REGISTERY['and'], args=result)


def explain(ast: ItemAST) -> Dict:
    """Convert ast as dict."""
    result = {}
    if ast.op.combinator:
        result[ast.op.name] = list(map(explain, ast.args))
    else:
        result[ast.op.name] = ast.args
    return result


def compile_ast(ast: ItemAST) -> Evaluator:
    """Compile AST in an Evaluator function."""
    if ast.op.arity == OperatoryArity.UNARY:
        return operator_factory(ast.op.function)
    if ast.op.combinator:
        return operator_factory(ast.op.function, *list(map(compile_ast, ast.args)))
    return operator_factory(ast.op.function, *ast.args)
