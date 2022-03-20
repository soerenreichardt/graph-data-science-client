from typing import Any, Dict, List

import neo4j

from ..error.illegal_attr_checker import IllegalAttrChecker
from ..error.uncallable_namespace import UncallableNamespace
from ..graph.graph_object import Graph
from ..query_runner.query_runner import QueryRunner


class UtilProcRunner(UncallableNamespace, IllegalAttrChecker):
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    def asNode(self, node_id: int) -> Any:
        self._namespace += ".asNode"
        result = self._query_runner.run_query(f"RETURN {self._namespace}({node_id}) AS node")

        return result["node"].squeeze()  # type: ignore

    def asNodes(self, node_ids: List[int]) -> List[Any]:
        self._namespace += ".asNodes"
        result = self._query_runner.run_query(f"RETURN {self._namespace}({node_ids}) AS nodes")

        print(result)
        return result["nodes"].squeeze()  # type: ignore

    def nodeProperty(self, G: Graph, node_id: int, property_key: str, node_label: str = "*") -> Any:
        self._namespace += ".nodeProperty"

        query = f"RETURN {self._namespace}($graph_name, $node_id, $property_key, $node_label) as property"
        params = {
            "graph_name": G.name(),
            "node_id": node_id,
            "property_key": property_key,
            "node_label": node_label,
        }
        result = self._query_runner.run_query(query, params)

        return result["property"].squeeze()
