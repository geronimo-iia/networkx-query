from typing import Callable

from networkx_query.definition import (
    NETWORKX_OPERATORS_REGISTERY,
    OperatorDefinition,
    OperatoryArity,
    register_operator,
)


def test_operator_definition():
    definition = OperatorDefinition(name="test", function=lambda a: a, arity=OperatoryArity.UNARY, alias="alias_test")
    assert definition.name == "test"
    assert definition.arity == OperatoryArity.UNARY
    assert definition.alias == "alias_test"
    assert not definition.combinator
    assert not definition.profile
    assert isinstance(definition.function, Callable)

    assert str(definition) == definition.name


def test_register_operator_register_alias():
    register_operator(name="test", arity=OperatoryArity.UNARY, alias="alias_test")(lambda a: a)
    assert "test" in NETWORKX_OPERATORS_REGISTERY
    assert "alias_test" in NETWORKX_OPERATORS_REGISTERY


def test_register_operator_register_all_parameters():
    register_operator(name="test2", arity=OperatoryArity.UNARY)(lambda a: a)

    definition = NETWORKX_OPERATORS_REGISTERY["test2"]
    assert definition.name == "test2"
    assert definition.arity == OperatoryArity.UNARY
    assert not definition.alias
    assert not definition.combinator
    assert not definition.profile
    assert isinstance(definition.function, Callable)

    register_operator(name="test3", arity=OperatoryArity.UNARY, combinator=True)(lambda a: a)
    definition = NETWORKX_OPERATORS_REGISTERY["test3"]
    assert definition.combinator
