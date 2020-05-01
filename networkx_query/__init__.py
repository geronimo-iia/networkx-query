"""networkx-query."""
from pkg_resources import DistributionNotFound, get_distribution

from .definition import Evaluator, ParserException
from .query import explain_query, prepare_query

__all__ = ['prepare_query', 'explain_query', 'ParserException', 'Evaluator']

try:
    __version__ = get_distribution('networkx_query').version
except DistributionNotFound:  # pragma: no cover
    __version__ = '(local)'
