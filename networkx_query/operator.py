# type: ignore
"""Define few operator."""
from typing import Any, List, Tuple

from .definition import Evaluator, OperatoryArity, Path, register_operator


def lookup_path(context: Any, sub_paths: Path) -> Tuple[bool, Any]:
    """Lookup attributs in a context like dictionary.

    Arguments:
        context (Any): a dictionnary like structure with in and [] methods
            (support __contains__ or  (__iter__ and __getitem__)).
        sub_paths (Path): a path (single string or an ordered tuple of string)

    Returns:
        (Tuple[bool, Any]): (True, attribut value ) or (False, None) if path not found

    Exceptions:
        (RuntimeError): if context did not compliant

    """
    if not context:
        return (False, None)

    if not (hasattr(context, "__contains__") or (hasattr(context, "__iter__") and hasattr(context, "__getitem__"))):
        raise RuntimeError('Context must be dictionnary like')

    if isinstance(sub_paths, Tuple):
        if sub_paths:
            # len > 0
            current = context
            i = 0
            while i < len(sub_paths):
                p = sub_paths[i]
                if not current or p not in current:
                    return (False, None)
                i += 1
                current = current[p]
            return (True, current)
        return (False, None)

    # simple string
    match = sub_paths in context
    return (match, context[sub_paths] if match else None)


@register_operator(name="has", arity=OperatoryArity.BINARY, profile=[Any, Path])
def op_has(context: Any, path: Path) -> bool:
    """Check if path exists in context."""
    (match, _) = lookup_path(context, path)
    return match


@register_operator(name="contains", arity=OperatoryArity.TERNARY, profile=[Any, Path, str])
def op_contains(context: Any, path: Path, value: str) -> bool:
    """Check if attribut (specifed with path) exists and contains specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value.find(value) != -1


@register_operator(name="eq", alias="==", arity=OperatoryArity.TERNARY, profile=[Any, Path, Any])
def op_eq(context: Any, path: Path, value: Any) -> bool:
    """Check if attribut (specifed with path) exists and equals specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value == value


@register_operator(name="neq", alias="!=", arity=OperatoryArity.TERNARY, profile=[Any, Path, Any])
def op_neq(context: Any, path: Path, value: Any) -> bool:
    """Check if attribut (specifed with path) did not exists or not equals specified value."""
    return not op_eq(context, path, value)


@register_operator(name="gt", alias=">", arity=OperatoryArity.TERNARY, profile=[Any, Path, Any])
def op_gt(context: Any, path: Path, value: Any) -> bool:
    """Check if attribut (specifed with path) exists and greather that specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value > value


@register_operator(name="lt", alias="<", arity=OperatoryArity.TERNARY, profile=[Any, Path, Any])
def op_lt(context: Any, path: Path, value: Any) -> bool:
    """Check if attribut (specifed with path) exists and lower that specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value < value


@register_operator(name="gte", alias=">=", arity=OperatoryArity.TERNARY, profile=[Any, Path, Any])
def op_gte(context: Any, path: Path, value: Any) -> bool:
    """Check if attribut (specifed with path) exists and greather or equals that specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value >= value


@register_operator(name="lte", alias="<=", arity=OperatoryArity.TERNARY, profile=[Any, Path, Any])
def op_lte(context: Any, path: Path, value: Any) -> bool:
    """Check if attribut (specifed with path) exists and lower or equals that specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value <= value


@register_operator(name="in", alias=":=", arity=OperatoryArity.TERNARY, profile=[Any, Path, List[Any]])
def op_in(context: Any, path: Path, value: List[Any]) -> bool:
    """Check if attribut (specifed with path) exists and attribut value in specified value."""
    (match, _current_value) = lookup_path(context, path)
    return match and _current_value in value


@register_operator(name="and", alias="&&", arity=OperatoryArity.NARY, combinator=True, profile=[Any, Evaluator])
def op_and(context: Any, *filters: Evaluator) -> bool:
    """Define And operator."""
    for f in filters:
        if not f(context):
            return False
    return True


@register_operator(name="or", alias="||", arity=OperatoryArity.NARY, combinator=True, profile=[Any, Evaluator])
def op_or(context: Any, *filters: Evaluator) -> bool:
    """Define Or operator."""
    for f in filters:
        if f(context):
            return True
    return False


@register_operator(name="xor", arity=OperatoryArity.NARY, combinator=True, profile=[Any, Evaluator])
def op_xor(context: Any, *filters: Evaluator) -> bool:
    """Define Xor operator."""
    is_true = False
    for f in filters:
        _test = f(context)
        is_true = (is_true and not _test) or (not is_true and _test)
    return is_true


@register_operator(name="nxor", arity=OperatoryArity.NARY, combinator=True, profile=[Any, Evaluator])
def op_nxor(context: Any, *filters: Evaluator) -> bool:
    """Define nxor operator."""
    return not op_xor(context, *filters)


@register_operator(name="not", arity=OperatoryArity.BINARY, combinator=True, profile=[Any, Evaluator], alias="!")
def op_not(context: Any, a_filter: Evaluator) -> bool:
    """Define Not operator."""
    return not a_filter(context)
