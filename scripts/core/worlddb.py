import hashlib
import json
from typing import Any, Callable, Dict, List, Optional

class Node:
    """
    WorldDB Core Node: Represents an immutable 'world'.
    A node is content-addressed; its ID is a SHA-256 hash of its content and its children's IDs.
    """
    def __init__(self, content: Dict[str, Any], children: List[str] = None):
        self.content = content
        self.children = children or []
        self.id = self._compute_hash()

    def _compute_hash(self) -> str:
        # Create a deterministic representation for hashing
        data_to_hash = {
            "content": self.content,
            "children": self.children
        }
        # Convert to string and hash. Sort keys to ensure consistent hashing
        data_str = json.dumps(data_to_hash, sort_keys=True)
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f"Node(id={self.id[:8]}..., content={self.content}, children={self.children})"


class Edge:
    """
    WorldDB Edge: Represents a relationship between two nodes with programmable hooks.
    """
    def __init__(self, source_id: str, target_id: str, relation_type: str, on_insert: Optional[Callable] = None):
        self.source_id = source_id
        self.target_id = target_id
        self.relation_type = relation_type
        self.on_insert = on_insert

    def __repr__(self):
        return f"Edge({self.source_id[:8]} -[{self.relation_type}]-> {self.target_id[:8]})"


class MemoryGraph:
    """
    WorldDB Graph Orchestrator: Manages nodes, edges, and handles write-time reconciliation.
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
    
    def insert_node(self, content: Dict[str, Any], children: List[str] = None) -> Node:
        """
        Insert a new node into the graph. 
        Since nodes are immutable, if identical content exists, it naturally deduplicates (same ID).
        """
        node = Node(content, children)
        if node.id not in self.nodes:
            self.nodes[node.id] = node
        return node
        
    def add_edge(self, source_id: str, target_id: str, relation_type: str, on_insert: Optional[Callable] = None) -> Edge:
        """
        Add an edge and trigger the on_insert programmable hook (write-time reconciliation).
        """
        edge = Edge(source_id, target_id, relation_type, on_insert)
        self.edges.append(edge)
        
        # Trigger programmable hook if present (pure Python prototype)
        if edge.on_insert:
            edge.on_insert(self, edge)
            
        return edge

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)
        
    def update_node(self, old_node_id: str, new_content: Dict[str, Any], new_children: List[str] = None, on_supersede: Optional[Callable] = None) -> Node:
        """
        Immutability constraint: 'updating' means creating a new node and explicitly superseding the old one.
        """
        # Create new node
        new_node = self.insert_node(new_content, new_children)
        
        # We track superseded status dynamically via edges.
        self.add_edge(new_node.id, old_node_id, "SUPERSEDES", on_supersede)
        return new_node

    def cascade_update(self, parent_id: str, old_child_id: str, new_child_id: str) -> Node:
        """
        Merkle Cascade: When a child updates, the parent must also be updated (superseded) 
        because its `children` list changes, altering its hash.
        """
        parent = self.get_node(parent_id)
        if not parent:
            raise ValueError(f"Parent {parent_id} not found in graph.")
            
        new_children = [new_child_id if c == old_child_id else c for c in parent.children]
        
        # The parent is updated, which recursively could trigger its parents, but we keep it 1-level here for prototype.
        return self.update_node(parent_id, parent.content, new_children)

    def get_active_fact(self, query_key: str, query_val: Any) -> Optional[Node]:
        """
        Helper to query the graph for an active (non-superseded) node by content key/value.
        In a full WorldDB, this would use vector search.
        """
        # Find all matching nodes
        matches = []
        for node in self.nodes.values():
            if node.content.get(query_key) == query_val:
                matches.append(node)
                
        # Filter out superseded nodes (nodes that are the TARGET of a SUPERSEDES edge)
        superseded_ids = set()
        for edge in self.edges:
            if edge.relation_type == "SUPERSEDES":
                superseded_ids.add(edge.target_id)
                
        active_matches = [m for m in matches if m.id not in superseded_ids]
        return active_matches[0] if active_matches else None
