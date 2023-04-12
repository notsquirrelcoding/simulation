from typing import TypedDict
import igraph as ig



class StartOptions(TypedDict):
    vul_range: tuple[float, float]
    year: int



g = ig.Graph(n=10, edges=[[0, 1], [0, 5]])

g.add_edges([(0, 1), (1, 2)])

print(g)

# List of graphs


# Things to