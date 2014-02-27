"""Some graph algorithms in python"""

class Digraph:
    vertexes = []
    adj_list = {}
    def __init__(self, vs, edges):
        """Build a digraph from vertices and edges

        Edges should be an array of tuples (from, to, cost)"""
        self.vertexes = vs
        for v in vs:
            self.adj_list[v] = []
        for (fr, to, cost) in edges:
            self.adj_list[fr].append( (to,cost) )
    def dfs(self, vertex):
        visited = []
        stack = [vertex]
        while stack:
            top = stack[-1]
            del stack[-1:]
            if not top in visited:
                visited.append(top)
                for (to,cost) in self.adj_list[top]:
                    stack.append(to)
        return visited
    def bfs(self, vertex):
        visited = [vertex]
        queue = [vertex]
        while queue:
            next = queue[0]
            del queue[:1]
            for (to,cost) in self.adj_list[next]:
                if not to in visited:
                    visited.append(to)
                    queue.append(to)
        return visited
    def topsort(self):
        rev_adj_lists = {}
        for v in self.vertexes:
            rev_adj_lists[v] = []
        for v in self.vertexes:
            for (to, cost) in self.adj_list[v]:
                rev_adj_lists[to].append(v)
        no_predecessors = []
        results = []
        for v in self.vertexes:
            if not rev_adj_lists[v]:
                no_predecessors.append(v)
        while no_predecessors:
            next = no_predecessors[0]
            del no_predecessors[:1]
            results.append(next)
            for (to, cost) in self.adj_list[next]:
                rev_adj_lists[to].remove(next)
                if not rev_adj_lists[to]:
                    no_predecessors.append(to)
        for v in self.vertexes:
            if rev_adj_lists[v]:
                return "The graph has a cycle"
        return results

verts = "ABCDE"
edges1 = [('A','B',2), ('A','E',1),  \
          ('B','C',3), ('B','A',2),  \
          ('C','C',1), ('C','D',2),  \
          ('D','E',0),  \
          ('E','D',1), ('E','B',2) ]
edges3 = [('A','B',2), ('A','E',1),  \
          ('B','C',3), ('A','B',3),  \
          ('C','D',2),  \
          ('E','D',1), ('E','B',2) ]


if __name__ == "__main__":
    g1 = Digraph(verts,edges1)
    dfs1 = g1.dfs('A')
    print(dfs1)
    bfs1 = g1.bfs('A')
    print(bfs1)
    ts1 = g1.topsort()
    print(ts1)

    g3 = Digraph(verts,edges3)
    dfs3 = g3.dfs('A')
    print(dfs3)
    bfs3 = g3.bfs('A')
    print(bfs3)
    ts3 = g3.topsort()
    print(ts3)
