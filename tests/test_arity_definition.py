from networkx_query.definition import OperatoryArity


def test_operator_arity_definition():
    assert OperatoryArity.UNARY.arity == 1
    assert OperatoryArity.BINARY.arity == 2
    assert OperatoryArity.TERNARY.arity == 3
    assert OperatoryArity.NARY.arity == 1


def test_operator_arity_unary_is_compliant():
    t = OperatoryArity.UNARY.is_compliant([])
    assert t == (True, 0)
    t = OperatoryArity.UNARY.is_compliant([True])
    assert t == (False, 1)


def test_operator_arity_binary_is_compliant():
    t = OperatoryArity.BINARY.is_compliant([])
    assert t == (False, -1)
    t = OperatoryArity.BINARY.is_compliant([True])
    assert t == (True, 0)
    t = OperatoryArity.BINARY.is_compliant([True, True])
    assert t == (False, 1)
    t = OperatoryArity.BINARY.is_compliant([True, True, True])
    assert t == (False, 2)


def test_operator_arity_ternary_is_compliant():
    t = OperatoryArity.TERNARY.is_compliant([])
    assert t == (False, -2)
    t = OperatoryArity.TERNARY.is_compliant([True])
    assert t == (False, -1)
    t = OperatoryArity.TERNARY.is_compliant([True, True])
    assert t == (True, 0)
    t = OperatoryArity.TERNARY.is_compliant([True, True, True])
    assert t == (False, 1)
    t = OperatoryArity.TERNARY.is_compliant([True, True, True, True])
    assert t == (False, 2)


def test_operator_arity_nary_is_compliant():
    t = OperatoryArity.NARY.is_compliant([])
    assert t == (False, -1)
    t = OperatoryArity.NARY.is_compliant([True])
    assert t == (True, 0)
    t = OperatoryArity.NARY.is_compliant([True, True])
    assert t == (True, 0)
    t = OperatoryArity.NARY.is_compliant([True, True, True])
    assert t == (True, 0)
    t = OperatoryArity.NARY.is_compliant([True, True, True, True])
    assert t == (True, 0)
