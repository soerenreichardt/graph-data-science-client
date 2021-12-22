from neo4j import GraphDatabase

from gdsclient import GraphDataScience, Neo4jQueryRunner

URI = "bolt://localhost:7687"
GRAPH_NAME = "g"
driver = GraphDatabase.driver(URI)
runner = Neo4jQueryRunner(driver)
gds = GraphDataScience(runner)


def setup_module():
    global driver
    global graph
    global runner

    driver = GraphDatabase.driver(URI)
    runner = Neo4jQueryRunner(driver)

    runner.run_query(
        """
        CREATE
        (a: Node {x: 1}),
        (b: Node {x: 2}),
        (c: Node {x: 3}),
        (a)-[:REL {y: 42.0}]->(b),
        (a)-[:REL {y: 13.37}]->(c),
        (b)-[:REL {z: 7.9}]->(c)
        """
    )

    gds = GraphDataScience(runner)
    graph = gds.graph.project(
        GRAPH_NAME, {"Node": {"properties": "x"}}, {"REL": {"properties": ["y", "z"]}}
    )


def test_graph_node_count():
    assert graph.node_count() == 3


def test_graph_relationship_count():
    assert graph.relationship_count() == 3


def test_graph_node_properties():
    assert graph.node_properties("Node") == ["x"]


def test_graph_relationship_properties():
    assert graph.relationship_properties("REL") == ["y", "z"]


def test_graph_degree_distribution():
    assert graph.degree_distribution()["mean"] == 2.0


def test_graph_density():
    assert graph.density() == 0.5


def test_graph_memory_usage():
    assert graph.memory_usage()


def test_graph_size_in_bytes():
    assert graph.size_in_bytes() > 0


def teardown_module():
    runner.run_query("MATCH (n) DETACH DELETE n")
    runner.run_query(f"CALL gds.graph.drop('{GRAPH_NAME}', false)")
    driver.close()
