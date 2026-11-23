"""Breadth-first traversal of a synthetic, explicitly scoped footprint tree."""
from collections import deque

TREE = {
    "name":"parent.example", "in_scope":True, "terminal":False,
    "children":[
        {"name":"portal.parent.example","in_scope":True,"terminal":True,"children":[]},
        {"name":"dept.parent.example","in_scope":True,"terminal":False,"children":[
            {"name":"hr.dept.parent.example","in_scope":True,"terminal":True,"children":[]},
            {"name":"research.dept.parent.example","in_scope":True,"terminal":False,"children":[
                {"name":"lab.research.dept.parent.example","in_scope":True,"terminal":True,"children":[]}
            ]},
            {"name":"empty.dept.parent.example","in_scope":True,"terminal":False,"has_data":False,"children":[]}
        ]},
        {"name":"vendor.example","in_scope":False,"terminal":False,"children":[
            {"name":"service.vendor.example","in_scope":False,"terminal":True,"children":[]}
        ]}
    ]
}

def traverse(root):
    queue = deque([root])
    visited = []
    while queue:
        node = queue.popleft()
        visited.append(node["name"])
        if not node.get("in_scope", False):
            print("BOUNDARY — out of scope:", node["name"])
            continue
        if node.get("terminal", False) or node.get("has_data", True) is False:
            print("BOUNDARY — terminal/empty:", node["name"])
            continue
        queue.extend(node.get("children", []))
    return visited

if __name__ == "__main__":
    nodes = traverse(TREE)
    print("\nVisited nodes:", len(nodes))
    print("\n".join(nodes))
