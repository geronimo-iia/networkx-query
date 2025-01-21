import pytest

from networkx_query import ParserException
from networkx_query.parser import compile_ast, explain, parse

node_0 = {"application": "test"}
node_1 = {"application": "test", "weight": 3, "group": "my-group"}
node_2 = {"_link": {"provider": "aws", "resource_type": "test", "other": {"weight": 2}}}


def test_explain():
    result = explain(parse({"not": {"has": ["group"]}, "has": "application", "eq": [("_link", "other", "weight"), 2]}))
    assert result == {
        "and": [{"not": [{"has": ["group"]}]}, {"has": ["application"]}, {"eq": [("_link", "other", "weight"), 2]}]
    }


def test_compile_expression_has():
    func = compile_ast(parse({"has": "application"}))
    assert func(node_0)
    assert func(node_1)


def test_compile_expression_not_has():
    func = compile_ast(parse({"not": {"has": "group"}}))
    assert func(node_0)
    assert not func(node_1)


def test_compile_expression_contains():
    func = compile_ast(parse({"contains": ["group", "my"]}))
    assert not func(node_0)
    assert func(node_1)


def test_compile_expression_has_dict():
    func = compile_ast(parse({"has": "_link"}))
    assert not func(node_0)
    assert func(node_2)


def test_compile_expression_has_path():
    func = compile_ast(parse({"has": [("_link", "other", "weight")]}))
    assert not func(node_0)
    assert func(node_2)


def test_compile_expression_eq_path():
    func = compile_ast(parse({"eq": [("_link", "other", "weight"), 2]}))
    assert func(node_2)


def test_compile_expression_neq_path():
    func = compile_ast(parse({"neq": [("_link", "other", "weight"), 2]}))
    assert not func(node_2)
    func = compile_ast(parse({"neq": [("_link", "other", "weight"), 8]}))
    assert func(node_2)


def test_compile_expression_gt_path():
    func = compile_ast(parse({"gt": [("_link", "other", "weight"), 1]}))
    assert func(node_2)
    func = compile_ast(parse({"gt": [("_link", "other", "weight"), 2]}))
    assert not func(node_2)


def test_compile_expression_gte_path():
    func = compile_ast(parse({"gte": [("_link", "other", "weight"), 2]}))
    assert func(node_2)
    func = compile_ast(parse({"gte": [("_link", "other", "weight"), 1]}))
    assert func(node_2)


def test_compile_expression_lte_path():
    func = compile_ast(parse({"lte": [("_link", "other", "weight"), 2]}))
    assert func(node_2)
    func = compile_ast(parse({"lte": [("_link", "other", "weight"), 3]}))
    assert func(node_2)


def test_compile_expression_lt_path():
    func = compile_ast(parse({"lt": [("_link", "other", "weight"), 3]}))
    assert func(node_2)
    func = compile_ast(parse({"lt": [("_link", "other", "weight"), 2]}))
    assert not func(node_2)


def test_compile_expression_in_path():
    func = compile_ast(parse({"in": [("_link", "other", "weight"), [1, 2, 3]]}))
    assert func(node_2)


def test_compile_expression_and():
    func = compile_ast(parse({"and": [{"has": "application"}, {"in": [("weight",), [1, 2, 3]]}]}))
    assert not func(node_0)
    assert func(node_1)
    assert not func(node_2)


def test_compile_expression_or():
    func = compile_ast(parse({"or": [{"has": "application"}, {"in": [("weight",), [1, 2, 3]]}]}))
    assert func(node_0)
    assert func(node_1)
    assert not func(node_2)


def test_compile_expression_xor():
    func = compile_ast(parse({"xor": [{"has": "application"}, {"in": [("weight",), [1, 2, 3]]}]}))
    assert func(node_0)
    assert not func(node_1)
    assert not func(node_2)


def test_compile_expression_nxor():
    func = compile_ast(parse({"nxor": [{"has": "application"}, {"in": [("weight",), [1, 2, 3]]}]}))
    assert not func(node_0)
    assert func(node_1)
    assert func(node_2)


def test_parse_exception():
    with pytest.raises(ParserException):
        parse({"has": ["_link", "other", "weight"]})


def test_parse_raise_unknown_operator():
    with pytest.raises(ParserException):
        parse({"idontexistatall": ["_link", "other", "weight"]})
