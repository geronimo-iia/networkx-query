"""Define type and structure for query language."""
from enum import Enum, unique
from typing import Any, Callable, List, NamedTuple, Optional, Tuple, Type, Union

__all__ = [
    'Path',
    "Evaluator",
    "operator_factory",
    "OperatoryArity",
    "OperatorDefinition",
    "ItemAST",
    "NETWORKX_OPERATORS_REGISTERY",
    "register_operator",
]

NETWORKX_OPERATORS_REGISTERY = {}
"""Internal registry of operators."""

Path = Union[Tuple, str]
"""Node attribut path definition."""

Evaluator = Callable[[Any], bool]
"""Predicate function."""


def operator_factory(op_function: Callable, *args: Any) -> Evaluator:
    """Add context parameter to operator function.

    Arguments:
        op_function (Callable): any function with context evaluation has first parameter
        *args (Any): a list of parameter to enclose

    Returns:
        (Evaluator): evaluator function with single argument

    """
    return lambda context: op_function(context, *args)


@unique
class OperatoryArity(Enum):
    """Define operator arity constant."""

    UNARY = 1
    BINARY = 2
    TERNARY = 3
    NARY = 42

    @property
    def arity(self) -> int:
        """Returns awaiting arity of associated function."""
        return self.value if self != OperatoryArity.NARY else 1

    def is_compliant(self, parameters) -> Tuple[bool, int]:
        """Check if parameters cardinality is compliant with operator arity.

        Returns:
            (Tuple[bool, int]): (compliant, delta_paramaters)
                compliant is true if this is compliante
                delta_paramaters:
                    - 0 if compliante,
                    - < 0 if some parameters is missing,
                    - > 0 if too much parameters is given

        """
        # context parameter is ommited here
        count = len(parameters)
        if self.value == OperatoryArity.NARY.value:
            match = count > 0
            return (match, 0 if match else -1)
        match = (count + 1) == self.arity
        delta = (count + 1) - self.arity
        return (match, 0 if match else delta)


class OperatorDefinition(NamedTuple):
    """Operator definition.

    Attributes:
        name (str): operator shortname
        function (Callable): first argument must be a context to evaluate
        arity (OperatoryArity): arity of operator function
        combinator (Optional[bool]): Flag which indicate if this operator is a combination of other operator
        profile (Optional[List[Type]]): optional function profile
        alias (Optional[str]): optional alias name for this operator

    """

    name: str
    function: Callable
    arity: OperatoryArity
    combinator: Optional[bool] = False
    profile: Optional[List[Type]] = None
    alias: Optional[str] = None

    def __str__(self):
        return self.name


class ItemAST(NamedTuple):
    """Define our AST."""

    op: OperatorDefinition
    args: List[Any]

    def check_arity(self) -> Tuple[bool, int]:
        """Check arity of this item against operator definition.

        Utilities short cut to OperatorDefinition#OperatoryArity#is_compliant.

        Returns:
            (Tuple[bool, int]): (match, delta_parameters_count)

        """
        return self.op.arity.is_compliant(self.args)

    def check_profile(self) -> bool:  # pragma: no cover
        # TODO Fix: did not work with generic...
        if self.op.profile:
            if not self.op.combinator:
                # terminal operator
                for i in range(1, self.op.arity.value):  # we omit first parameters (not in args)
                    if not isinstance(self.args[i - 1], self.op.profile[i]):
                        return False
            else:
                for arg in self.args:
                    if not isinstance(arg, self.op.profile[1]):
                        return False
        return True


class ParserException(RuntimeError):
    """Define a parser exception with stack of expression."""

    def __init__(self, message, stack):
        super(RuntimeError, self).__init__(message)
        self.stack = stack


def register_operator(
    name: str,
    arity: OperatoryArity,
    combinator: Optional[bool] = False,
    profile: Optional[List[Any]] = None,
    alias: Optional[str] = None,
):
    """Register an operator."""
    global NETWORKX_OPERATORS_REGISTERY

    def decorate_function(f):
        _definition = OperatorDefinition(
            name=name, function=f, arity=arity, combinator=combinator, profile=profile, alias=alias
        )
        NETWORKX_OPERATORS_REGISTERY[_definition.name] = _definition
        if alias:
            NETWORKX_OPERATORS_REGISTERY[alias] = _definition
        return f

    return decorate_function
