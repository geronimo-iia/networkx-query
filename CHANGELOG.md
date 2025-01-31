# Change Log

## 2.1.3

- fix miss configuration with setuptool

## 2.1.2

- use uv tool as dependencies manager
- update github workflow
- fix few code style issue

## 2.1.1

- remove support for python 3.8

## 2.1.0


- add support for python 3.12
  
- build System:

  - update poetry declaration
  - use poe plugin (simplify makefile)
  - use pyright for analysis (remove mypi)

## 2.0.1

Security fix (dev tools)

- Removal of e-Tugra root certificate 

## 2.0.0

- add support for networkx 3.x: 
  By default, poetry will try to install the newest version of networkx (`networkx = "*"`).
- add test pipeline for python 3.9, 3.10 and 3.11

## 1.0.3

- implements `search_relationships`

## 1.0.2

- technical feat:
    - use ruff as sucessor of flake8
    - update dev dependencies
    - use mkdocs

## 1.0.1

- fix documentation syntax
- add search_direct_relationships function
- rewrote search_edges and search_nodes (avoid extra filter step)


## 1.0.0 (2020-05-02)

- complete documentation
- add little example
- add search_edges, search_nodes for quick and eazy usage
- complete coverage

## 0.1.0 (2020-05-01)

- initial project structure based on [geronimo-iia/template-python](https://github.com/geronimo-iia/template-python)
- add operator definition, compiler, and parser on node