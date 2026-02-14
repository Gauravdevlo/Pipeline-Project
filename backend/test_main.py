import pytest
from fastapi.testclient import TestClient
from main import app, check_is_dag, Node, Edge

client = TestClient(app)

# Test 1: Root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Ping": "Pong"}

# Test 2: Simple valid DAG
def test_simple_dag():
    pipeline_data = {
        "nodes": [
            {"id": "node1"},
            {"id": "node2"},
            {"id": "node3"}
        ],
        "edges": [
            {"source": "node1", "target": "node2"},
            {"source": "node2", "target": "node3"}
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 3
    assert data["num_edges"] == 2
    assert data["is_dag"] == True

# Test 3: Circular dependency (not a DAG)
def test_circular_dag():
    pipeline_data = {
        "nodes": [
            {"id": "node1"},
            {"id": "node2"},
            {"id": "node3"}
        ],
        "edges": [
            {"source": "node1", "target": "node2"},
            {"source": "node2", "target": "node3"},
            {"source": "node3", "target": "node1"}  # Creates cycle
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 3
    assert data["num_edges"] == 3
    assert data["is_dag"] == False

# Test 4: Empty pipeline
def test_empty_pipeline():
    pipeline_data = {
        "nodes": [],
        "edges": []
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 0
    assert data["num_edges"] == 0
    assert data["is_dag"] == True

# Test 5: Branching DAG
def test_branching_dag():
    pipeline_data = {
        "nodes": [
            {"id": "input"},
            {"id": "llm"},
            {"id": "transform"},
            {"id": "filter"},
            {"id": "output1"},
            {"id": "output2"}
        ],
        "edges": [
            {"source": "input", "target": "llm"},
            {"source": "llm", "target": "transform"},
            {"source": "llm", "target": "filter"},
            {"source": "transform", "target": "output1"},
            {"source": "filter", "target": "output2"}
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 6
    assert data["num_edges"] == 5
    assert data["is_dag"] == True

# Test 6: Self-loop (node connects to itself)
def test_self_loop():
    pipeline_data = {
        "nodes": [
            {"id": "node1"}
        ],
        "edges": [
            {"source": "node1", "target": "node1"}  # Self loop
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 1
    assert data["num_edges"] == 1
    assert data["is_dag"] == False

# Test 7: Disconnected components
def test_disconnected_components():
    pipeline_data = {
        "nodes": [
            {"id": "a1"},
            {"id": "a2"},
            {"id": "b1"},
            {"id": "b2"}
        ],
        "edges": [
            {"source": "a1", "target": "a2"},
            {"source": "b1", "target": "b2"}
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 4
    assert data["num_edges"] == 2
    assert data["is_dag"] == True

# Test 8: Complex cycle
def test_complex_cycle():
    """
    A → B → C
    ↓       ↑
    D ──────┘
    """
    pipeline_data = {
        "nodes": [
            {"id": "A"},
            {"id": "B"},
            {"id": "C"},
            {"id": "D"}
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "A", "target": "D"},
            {"source": "D", "target": "C"}
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_dag"] == True  # This is actually a valid DAG

# Test 9: Make it a cycle by adding one edge
def test_make_cycle():
    """
    A → B → C
    ↓       ↑
    D ──────┘
    ↓
    A (back to start)
    """
    pipeline_data = {
        "nodes": [
            {"id": "A"},
            {"id": "B"},
            {"id": "C"},
            {"id": "D"}
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "A", "target": "D"},
            {"source": "D", "target": "C"},
            {"source": "C", "target": "A"}  # Creates cycle
        ]
    }
    response = client.post("/pipelines/parse", json=pipeline_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_dag"] == False