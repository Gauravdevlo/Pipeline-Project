from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from collections import defaultdict, deque

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineData):
    """
    Parse the pipeline and return:
    - num_nodes: Number of nodes in the pipeline
    - num_edges: Number of edges in the pipeline
    - is_dag: Whether the pipeline forms a Directed Acyclic Graph
    """
    try:
        num_nodes = len(pipeline.nodes)
        num_edges = len(pipeline.edges)
        
        # Check if the graph is a DAG
        is_dag = check_is_dag(pipeline.nodes, pipeline.edges)
        
        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'is_dag': is_dag
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def check_is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    """
    Check if the graph is a Directed Acyclic Graph (DAG)
    Uses Kahn's algorithm (topological sort with BFS)
    """
    if not nodes:
        return True
    
    # Build adjacency list and in-degree count
    adj_list = defaultdict(list)
    in_degree = {node.id: 0 for node in nodes}
    
    # Build the graph
    for edge in edges:
        adj_list[edge.source].append(edge.target)
        if edge.target in in_degree:
            in_degree[edge.target] += 1
        else:
            # Edge points to a node not in the nodes list
            in_degree[edge.target] = 1
    
    # Find all nodes with no incoming edges
    queue = deque([node_id for node_id, degree in in_degree.items() if degree == 0])
    processed_count = 0
    
    # Process nodes in topological order
    while queue:
        node = queue.popleft()
        processed_count += 1
        
        # Reduce in-degree for neighboring nodes
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we processed all nodes, it's a DAG
    # If there are unprocessed nodes, there's a cycle
    return processed_count == len(in_degree)

# Alternative implementation using DFS (Depth-First Search)
def check_is_dag_dfs(nodes: List[Node], edges: List[Edge]) -> bool:
    """
    Alternative DAG check using DFS and cycle detection
    """
    if not nodes:
        return True
    
    # Build adjacency list
    adj_list = defaultdict(list)
    for edge in edges:
        adj_list[edge.source].append(edge.target)
    
    # Track visit states: 0 = unvisited, 1 = visiting, 2 = visited
    visit_state = {node.id: 0 for node in nodes}
    
    def has_cycle(node_id: str) -> bool:
        """DFS to detect cycles"""
        if visit_state.get(node_id, 0) == 1:
            # Currently visiting this node - cycle detected
            return True
        if visit_state.get(node_id, 0) == 2:
            # Already visited - no cycle from this node
            return False
        
        # Mark as visiting
        visit_state[node_id] = 1
        
        # Visit all neighbors
        for neighbor in adj_list[node_id]:
            if has_cycle(neighbor):
                return True
        
        # Mark as visited
        visit_state[node_id] = 2
        return False
    
    # Check for cycles starting from each unvisited node
    for node in nodes:
        if visit_state[node.id] == 0:
            if has_cycle(node.id):
                return False
    
    return True