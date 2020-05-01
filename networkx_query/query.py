"""networkx-query public interace definition."""
from typing import Dict

from .definition import Evaluator, ParserException
from .parser import compile_ast, explain, parse

__all__ = ['prepare_query', 'explain_query', 'ParserException']


def prepare_query(expra: Dict) -> Evaluator:
    return compile_ast(parse(expra=expra))


def explain_query(expra: Dict) -> Dict:
    return explain(parse(expra=expra))
