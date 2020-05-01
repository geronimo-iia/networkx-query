"""networkx-query definition."""
from pkg_resources import get_distribution, DistributionNotFound
from .definition import Evaluator, ItemAST, ParserException
from .parser import compile_ast, explain, parse

__all__ = ['parse', 'explain', 'compile_ast', 'ItemAST', 'ParserException']

try:
    __version__ = get_distribution('networkx_query').version
except DistributionNotFound:  # pragma: no cover
    __version__ = '(local)'
