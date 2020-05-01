# networkx-query


[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/networkx-query/master.svg?label=unix)](https://travis-ci.com/geronimo-iia/networkx-query)[![Coverage Status](https://img.shields.io/coveralls/geronimo-iia/networkx-query/master.svg)](https://coveralls.io/r/geronimo-iia/networkx-query)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fe669a02b4aa46b5b1faf619ba2bf382)](https://www.codacy.com/app/geronimo-iia/networkx-query?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geronimo-iia/networkx-query&amp;utm_campaign=Badge_Grade)[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/geronimo-iia/networkx-query.svg)](https://scrutinizer-ci.com/g/geronimo-iia/networkx-query/?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/networkx-query.svg)](https://pypi.org/project/networkx-query)
[![PyPI License](https://img.shields.io/pypi/l/networkx-query.svg)](https://pypi.org/project/networkx-query)

Versions following [Semantic Versioning](https://semver.org/)

## Overview

NetworkX Query Tool (preview)

See [documentation](https://geronimo-iia.github.io/networkx-query).


## Installation

Install this library directly into an activated virtual environment:

```text
$ pip install networkx-query
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add networkx-query
```

## Usage

Searching node:

```python
import networkx as nx
from networkx_query import search_nodes, search_edges

g = nx.DiGraph()
g.add_node(1, product="chocolate")
g.add_node(2, product="milk")
g.add_node(3, product="coat")
g.add_edge(1, 2, action="shake")
g.add_edge(3, 2, action="produce")


for node_id in search_nodes(g, {"==": [("product",), "chocolate"]}):
    print(node_id)

>> 1

for edge_id in search_edges(g, {"eq": [("action",), "produce"]}):
    print(edge_id)

>> (3, 2)
```

You could do the same with edges using ```search_edges```.

## API

[search_edges](https://geronimo-iia.github.io/networkx-query/api.html#networkx_query.search_edges) and [search_nodes](https://geronimo-iia.github.io/networkx-query/api.html#networkx_query.search_nodes) are based on [prepare_query](https://geronimo-iia.github.io/networkx-query/api.html#networkx_query.prepare_query) which return an Evaluator.

Evaluator are function with this signature: (context) -> bool

Context is a dictionnary like structure (with in and [] methods, and support __contains__ or  (__iter__ and __getitem__))


## Query language

Define a json query language like [json-query-language](https://github.com/clue/json-query-language/blob/master/SYNTAX.md) 
against nodes or edges attributes.

A Path is a single string or a tuple of string which represente a path in a tree (here a dictionnary).


### Expressions

All those expression are evaluate against a context wich is a dictionnary like (as can be a NodeDataView or an EdgeDataView).

Main expression syntax turn around this:

```
{
    operator_name : parameters
}
```

### Basic matching expression

Test if a node/edge has an attribute named "my_property":
```
{
    "has" : "my_property"
}
```


Test if a node/edge has an attribute product : { "definition": { "name": xxx }} with xxx equals to "chocolate".
```
{
    "eq" : [ ("product", "definition", "name"), "chocolate"]
}
```

We support this operators:

| Name     | Alias | Parameters      | Description                                                                                   |
| -------- | :---: | --------------- | --------------------------------------------------------------------------------------------- |
| has      |       | Path            | Check if path exists in context.                                                              |
| contains |       | Path, str       | Check if an attribut (specifed with path) exists and contains specified value.                |
| eq       | `==`  | Path, Any       | Check if an attribut (specifed with path) exists and equals specified value.                  |
| neq      | `!=`  | Path, Any       | Check if an attribut (specifed with path) did not exists or not equals specified value.       |
| gt       |  `<`  | Path, Any       | Check if an attribut (specifed with path) exists and greather that specified value.           |
| lt       |  `<`  | Path, Any       | Check if an attribut (specifed with path) exists and lower that specified value.              |
| gte      | `>=`  | Path, Any       | Check if an attribut (specifed with path) exists and greather or equals that specified value. |
| lte      | `<=`  | Path, Any       | Check if an attribut (specifed with path) exists and lower or equals that specified value.    |
| in       | `:=`  | Path, List[Any] | Check if an attribut (specifed with path) exists and attribut value in specified values.      |


### Boolean composition of matching expression

We support this operators:

| Name | Alias | Parameters    | Description           |
| ---- | :---: | ------------- | --------------------- |
| and  | `&&`  | list of query | Define And operator.  |
| or   | \|\|  | list of query | Define Or operator.   |
| xor  |       | list of query | Define xor operator.  |
| nxor |       | list of query | Define nxor operator. |
| not  |  `!`  | query         | Define Not operator.  |


By default, a list of expressions is equivalent of an "AND" of this expressions.

Example:
```
{
    'not': {
        'has': ['group']
    },
    'has': 'application',
    'eq': [('_link', 'other', 'weight'), 2]
}
```
is equivalent to:

```
{
    'and': [
        {
            'not': [
                {
                    'has': ['group']
                }
            ]
        },
        {
            'has': ['application']
        },
        {
            'eq': [('_link', 'other', 'weight'), 2]
        }
    ]
}
```


## Wished Features

- add match node, edges, path specification
- add set expression on node/edges with constraints
- add path condition between node

