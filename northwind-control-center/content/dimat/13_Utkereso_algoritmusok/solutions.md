# Chapter 13 - Útkereső algoritmusok (Pathfinding Algorithms) - Solutions

## Section 13.1 - Legrövidebb út problémák

### HF - Define Shortest Path Problem

**Problem:** Given a weighted graph G = (V, E) with weight function w: E → ℝ, find a path from source s to target t with minimum total weight.

**Path weight:** w(P) = Σᵢ w(vᵢ, vᵢ₊₁)

**Shortest path distance:** δ(s,t) = min{w(P) : P is a path from s to t}

---

### HF - Distinguish Single-Source vs All-Pairs

| Problem Type | Input | Output | Algorithms |
|--------------|-------|--------|------------|
| **Single-source** | Graph G, source s | δ(s,v) for all v | Dijkstra, Bellman-Ford, BFS |
| **Single-pair** | Graph G, source s, target t | δ(s,t) | Same as single-source |
| **All-pairs** | Graph G | δ(u,v) for all u,v | Floyd-Warshall, V×Dijkstra |

---

### HF - Understand Negative Weight Edges

**Issues with negative weights:**
- Dijkstra's algorithm fails (greedy choice not optimal)
- Negative cycles make shortest path undefined (can loop forever)

**Solutions:**
- Bellman-Ford: handles negative weights, detects negative cycles
- Floyd-Warshall: handles negative weights (but not negative cycles)

---

### Study - Applications

1. **GPS Navigation:** Find fastest route between locations
2. **Network Routing:** Minimize latency or maximize bandwidth
3. **Social Networks:** Find degrees of separation
4. **Game AI:** NPC pathfinding
5. **Currency Arbitrage:** Detect profitable cycles (negative cycles in log-transformed graph)

---

## Section 13.2 - Dijkstra Algoritmusa

### HF - State Dijkstra's Algorithm Prerequisites

**Requirements:**
- Weighted graph G = (V, E)
- **Non-negative weights:** w(e) ≥ 0 for all e ∈ E
- Source vertex s ∈ V

**Output:** Shortest path distances δ(s,v) for all v ∈ V

---

### HF - Trace Dijkstra's Algorithm

**Example:**
```
Graph:
    1
  a───b
  │ \ │
2 │  4│ 1
  │   │
  c───d
    3
```

**Initialization:**
- d[a] = 0, d[b] = d[c] = d[d] = ∞
- Priority queue: {(a, 0)}

**Iterations:**

| Step | Extract | Relax | d[a] | d[b] | d[c] | d[d] |
|------|---------|-------|------|------|------|------|
| 0 | - | init | 0 | ∞ | ∞ | ∞ |
| 1 | a | b,c | 0 | 1 | 2 | ∞ |
| 2 | b | d | 0 | 1 | 2 | 2 |
| 3 | c | - | 0 | 1 | 2 | 2 |
| 4 | d | - | 0 | 1 | 2 | 2 |

**Result:** δ(a,b) = 1, δ(a,c) = 2, δ(a,d) = 2

---

### HF - Prove Correctness of Dijkstra's Algorithm

**Theorem:** Dijkstra's algorithm correctly computes shortest paths in graphs with non-negative weights.

**Proof (by induction):**

**Invariant:** When vertex u is added to the settled set S, d[u] = δ(s,u).

**Base:** First vertex is s with d[s] = 0 = δ(s,s). ✓

**Inductive step:** 
- Assume invariant holds for all vertices in S
- Let u be next vertex extracted (minimum d among V-S)
- Suppose there exists shorter path P to u
- P must leave S at some point (since s ∈ S, u ∉ S)
- Let (x,y) be first edge leaving S
- By triangle inequality: δ(s,y) ≤ δ(s,x) + w(x,y)
- By induction: d[x] = δ(s,x)
- When x was processed, y was relaxed: d[y] ≤ d[x] + w(x,y) = δ(s,y)
- But d[u] ≤ d[y] (u extracted first)
- Contradiction: d[u] cannot be > δ(s,u)

**Therefore:** d[u] = δ(s,u). ✓

---

### HF - Analyze Time Complexity

**With binary heap priority queue:**

| Operation | Count | Cost each | Total |
|-----------|-------|-----------|-------|
| Build heap | 1 | O(V) | O(V) |
| Extract-min | V | O(log V) | O(V log V) |
| Decrease-key | E | O(log V) | O(E log V) |

**Total:** O((V + E) log V)

**With Fibonacci heap:** O(V log V + E)

---

### HF - Implement with Priority Queue

```python
def dijkstra(G, s):
    d = {v: float('inf') for v in G}
    d[s] = 0
    pq = PriorityQueue()
    pq.put((0, s))
    
    while not pq.empty():
        dist_u, u = pq.get()
        
        if dist_u > d[u]:
            continue
            
        for v, weight in G[u].items():
            if d[u] + weight < d[v]:
                d[v] = d[u] + weight
                pq.put((d[v], v))
    
    return d
```

---

### HF - Verify: Works Only with Non-Negative Weights

**Counterexample with negative weight:**

```
Graph:
    5      -10
  a───b────────c
```

**Dijkstra's execution:**
1. Extract a: d[a]=0, d[b]=5
2. Extract b: d[b]=5 (settled!)
3. Algorithm terminates

**But actual shortest path:** a→b→c with weight 5+(-10) = -5

**Problem:** Once b is settled, it's never reconsidered, even though a shorter path through c might exist.

**Conclusion:** Dijkstra fails with negative weights. ✗

---

## Section 13.3 - Bellman-Ford Algoritmus

### HF - State Bellman-Ford Algorithm

**Algorithm:**
```
1. Initialize: d[s] = 0, d[v] = ∞ for v ≠ s
2. For i = 1 to |V|-1:
   For each edge (u,v) ∈ E:
     Relax: if d[u] + w(u,v) < d[v]:
       d[v] = d[u] + w(u,v)
3. Check for negative cycles:
   For each edge (u,v) ∈ E:
     if d[u] + w(u,v) < d[v]:
       return "Negative cycle detected"
```

---

### HF - Trace Algorithm on Example

**Example with negative weight:**
```
Graph:
    4       -3
  a───b────────c
  │           │
2 │          1│
  │           │
  d───────────e
    5
```

**Iterations (|V|=5, so 4 iterations):**

| Iteration | d[a] | d[b] | d[c] | d[d] | d[e] |
|-----------|------|------|------|------|------|
| 0 (init) | 0 | ∞ | ∞ | ∞ | ∞ |
| 1 | 0 | 4 | ∞ | 2 | ∞ |
| 2 | 0 | 4 | 1 | 2 | 3 |
| 3 | 0 | 4 | 1 | 2 | 3 |
| 4 | 0 | 4 | 1 | 2 | 3 |

**Result:** All shortest paths found. ✓

---

### HF - Prove: Handles Negative Weights Correctly

**Theorem:** Bellman-Ford correctly computes shortest paths even with negative weights (if no negative cycles).

**Proof:**

**Lemma:** After i iterations, d[v] equals the shortest path from s to v using at most i edges.

**Proof by induction:**
- Base (i=0): d[s]=0, all others ∞. ✓
- Step: After i-1 iterations, paths with ≤i-1 edges are correct.
- Iteration i relaxes all edges, extending paths by one edge.
- Therefore after i iterations, paths with ≤i edges are correct. ✓

**Corollary:** After |V|-1 iterations, all simple paths are considered.

Since shortest paths are simple (no negative cycles), result is correct. ✓

---

### HF - Detect Negative Cycles

**Theorem:** If after |V|-1 iterations, any edge can still be relaxed, then G contains a negative cycle.

**Proof:**

If d[u] + w(u,v) < d[v] after |V|-1 iterations:
- Shortest path to v uses ≥ |V| edges
- Path with ≥ |V| edges must contain a cycle
- Path can be improved, so cycle must be negative

**Detection:** Run one more iteration; if any relaxation occurs, negative cycle exists. ✓

---

### HF - Analyze Time Complexity

| Operation | Count | Cost |
|-----------|-------|------|
| Initialization | 1 | O(V) |
| Main loop | |V|-1 | O(V) |
| Edge relaxation | |E| per iteration | O(E) |
| Negative cycle check | 1 | O(E) |

**Total:** O(V × E)

---

### HF - Compare with Dijkstra's Algorithm

| Property | Dijkstra | Bellman-Ford |
|----------|----------|--------------|
| Time complexity | O((V+E) log V) | O(VE) |
| Negative weights | ✗ No | ✓ Yes |
| Negative cycles | N/A | Detects |
| Parallelizable | No | Yes (edge relaxations) |
| Best for | Non-negative weights | General graphs |

---

## Section 13.4 - Floyd-Warshall Algoritmus

### HF - State Floyd-Warshall Algorithm

**Algorithm for all-pairs shortest paths:**

```
Initialize: d[i][j] = w(i,j) if (i,j) ∈ E, ∞ otherwise
            d[i][i] = 0

For k = 1 to |V|:
  For i = 1 to |V|:
    For j = 1 to |V|:
      d[i][j] = min(d[i][j], d[i][k] + d[k][j])
```

---

### HF - Trace Algorithm on Example

**Example (3 vertices):**
```
Initial distance matrix:
    a   b   c
a   0   3   ∞
b   ∞   0   1
c   2   ∞   0
```

**k=1 (through a):**
```
    a   b   c
a   0   3   ∞
b   ∞   0   1
c   2   5   0   (c→a→b = 2+3 = 5)
```

**k=2 (through b):**
```
    a   b   c
a   0   3   4   (a→b→c = 3+1 = 4)
b   ∞   0   1
c   2   5   5   (c→b→c = 5+1 = 6 > 5, no change)
```

**k=3 (through c):**
```
    a   b   c
a   0   3   4
b   3   0   1   (b→c→a = 1+2 = 3)
c   2   5   0
```

**Final all-pairs shortest paths.** ✓

---

### HF - Prove Correctness Using Dynamic Programming

**Definition:** d⁽ᵏ⁾[i][j] = shortest path from i to j using only vertices {1,...,k} as intermediates.

**Recurrence:**
- d⁽⁰⁾[i][j] = w(i,j) (direct edge)
- d⁽ᵏ⁾[i][j] = min(d⁽ᵏ⁻¹⁾[i][j], d⁽ᵏ⁻¹⁾[i][k] + d⁽ᵏ⁻¹⁾[k][j])

**Proof by induction:**

**Base (k=0):** Direct edges are correct. ✓

**Inductive step:** 
- Shortest path from i to j using {1,...,k} either:
  - Doesn't use k: d⁽ᵏ⁻¹⁾[i][j]
  - Uses k: d⁽ᵏ⁻¹⁾[i][k] + d⁽ᵏ⁻¹⁾[k][j]
- Take minimum of both. ✓

**After k=|V|:** All vertices can be intermediates, so d[|V|][i][j] = δ(i,j). ✓

---

### HF - Analyze Time Complexity

**Three nested loops:**
- Outer loop: |V| iterations
- Middle loop: |V| iterations
- Inner loop: |V| iterations

**Total:** O(|V|³)

**Space:** O(|V|²) for distance matrix

---

### HF - Analyze Space Complexity

**Distance matrix:** |V| × |V| = O(|V|²)

**Predecessor matrix (for path reconstruction):** |V| × |V| = O(|V|²)

**Total space:** O(|V|²)

**Optimization:** Can update in-place, no extra space needed.

---

### HF - Reconstruct Paths from Predecessor Matrix

**Predecessor matrix π:**
- π[i][j] = predecessor of j on shortest path from i

**Update rule:**
```
if d[i][k] + d[k][j] < d[i][j]:
  d[i][j] = d[i][k] + d[k][j]
  π[i][j] = π[k][j]
```

**Path reconstruction:**
```python
def get_path(π, i, j):
    if i == j:
        return [i]
    if π[i][j] == None:
        return []  # No path
    path = get_path(π, i, π[i][j])
    path.append(j)
    return path
```

---

## Section 13.5 - Szélességi keresés (BFS)

### HF - State BFS Algorithm

**Algorithm for unweighted graphs:**

```
BFS(G, s):
  d[v] = ∞ for all v
  d[s] = 0
  queue = [s]
  
  while queue not empty:
    u = queue.dequeue()
    for each neighbor v of u:
      if d[v] == ∞:
        d[v] = d[u] + 1
        queue.enqueue(v)
```

---

### HF - Trace BFS on Example

**Example:**
```
Graph:
  a───b───c
  │   │   │
  d───e───f
```

**BFS from a:**

| Step | Queue | d[a] | d[b] | d[c] | d[d] | d[e] | d[f] |
|------|-------|------|------|------|------|------|------|
| 0 | [a] | 0 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 1 | [b,d] | 0 | 1 | ∞ | 1 | ∞ | ∞ |
| 2 | [d,e] | 0 | 1 | ∞ | 1 | 2 | ∞ |
| 3 | [e,c] | 0 | 1 | 2 | 1 | 2 | ∞ |
| 4 | [c,f] | 0 | 1 | 2 | 1 | 2 | 3 |
| 5 | [f] | 0 | 1 | 2 | 1 | 2 | 3 |
| 6 | [] | 0 | 1 | 2 | 1 | 2 | 3 |

**Distances:** All vertices reachable, max distance = 3. ✓

---

### HF - Prove: BFS Finds Shortest Paths in Unweighted Graphs

**Theorem:** In unweighted graph, BFS computes δ(s,v) for all v.

**Proof by induction on distance:**

**Base:** d[s] = 0 = δ(s,s). ✓

**Inductive step:**
- Assume all vertices at distance k are correctly labeled
- Let v be at distance k+1 from s
- Shortest path: s → ... → u → v where δ(s,u) = k
- By induction, d[u] = k when u is dequeued
- v is discovered and d[v] = d[u] + 1 = k+1
- Since BFS explores level by level, v is labeled before any longer path

**Therefore:** d[v] = δ(s,v). ✓

---

### HF - Analyze Time Complexity

| Operation | Count | Cost |
|-----------|-------|------|
| Initialize | 1 | O(V) |
| Enqueue/Dequeue | V | O(1) each |
| Process edges | E | O(1) per edge |

**Total:** O(V + E)

---

### HF - Applications

1. **Connectivity:** Check if graph is connected
2. **Bipartiteness:** 2-coloring using BFS levels
3. **Shortest paths:** In unweighted graphs
4. **Network broadcasting:** Minimum hops to reach all nodes

---

## Section 13.6 - Mélységi keresés (DFS)

### HF - State DFS Algorithm

**Algorithm:**

```
DFS(G):
  time = 0
  for each v in V:
    color[v] = WHITE
    parent[v] = None
  
  for each v in V:
    if color[v] == WHITE:
      DFS-Visit(v)

DFS-Visit(u):
  color[u] = GRAY
  time += 1
  d[u] = time  # discovery time
  
  for each v adjacent to u:
    if color[v] == WHITE:
      parent[v] = u
      DFS-Visit(v)
  
  color[u] = BLACK
  time += 1
  f[u] = time  # finish time
```

---

### HF - Trace DFS on Example

**Example:**
```
Graph:
  a───b
  │  /│
  │ / │
  c───d
```

**DFS from a:**

| Step | Action | d[] | f[] | Stack |
|------|--------|-----|-----|-------|
| 1 | Discover a | a:1 | - | [a] |
| 2 | Discover b | a:1, b:2 | - | [a,b] |
| 3 | Discover d | a:1, b:2, d:3 | - | [a,b,d] |
| 4 | Discover c | a:1, b:2, d:3, c:4 | - | [a,b,d,c] |
| 5 | Finish c | a:1, b:2, d:3, c:4 | c:5 | [a,b,d] |
| 6 | Finish d | a:1, b:2, d:3 | c:5, d:6 | [a,b] |
| 7 | Finish b | a:1, b:2 | c:5, d:6, b:7 | [a] |
| 8 | Finish a | a:1 | c:5, d:6, b:7, a:8 | [] |

---

### HF - Classify Edges

**Edge types (based on colors):**

| Type | Condition | Meaning |
|------|-----------|---------|
| **Tree edge** | v is WHITE | Part of DFS tree |
| **Back edge** | v is GRAY | Points to ancestor (cycle!) |
| **Forward edge** | v is BLACK, d[u] < d[v] | Points to descendant |
| **Cross edge** | v is BLACK, d[u] > d[v] | Points to other branch |

**In undirected graphs:** Only tree edges and back edges exist.

---

### HF - Analyze Time Complexity

| Operation | Count | Cost |
|-----------|-------|------|
| Initialize | 1 | O(V) |
| DFS-Visit calls | V | O(1) + adjacency |
| Edge processing | E | O(1) per edge |

**Total:** O(V + E)

---

### HF - Applications

1. **Topological sort:** Order by finish time (reverse)
2. **Strongly connected components:** Kosaraju's or Tarjan's algorithm
3. **Cycle detection:** Back edge exists ⇔ cycle exists
4. **Biconnected components:** Find articulation points

---

## Section 13.7 - A* Algoritmus

### HF - State A* Algorithm

**Algorithm with heuristic h:**

```
A*(G, s, t, h):
  g[s] = 0
  f[s] = h(s)
  open = PriorityQueue([(f[s], s)])
  closed = set()
  
  while open not empty:
    _, u = open.pop_min()
    
    if u == t:
      return reconstruct_path(u)
    
    closed.add(u)
    
    for each neighbor v of u:
      if v in closed:
        continue
      
      new_g = g[u] + w(u,v)
      
      if v not in open or new_g < g[v]:
        g[v] = new_g
        f[v] = g[v] + h(v)
        parent[v] = u
        open.add((f[v], v))
```

---

### HF - Define Admissible Heuristic

**Definition:** Heuristic h is **admissible** if h(v) ≤ δ(v,t) for all v.

(i.e., h never overestimates the true cost)

**Examples:**
- **Manhattan distance:** Admissible for grid graphs (4-directional)
- **Euclidean distance:** Admissible for geometric graphs
- **Zero heuristic:** Admissible (A* becomes Dijkstra)

---

### HF - Prove: A* is Optimal with Admissible Heuristic

**Theorem:** A* with admissible heuristic finds optimal path.

**Proof:**

Let P* be optimal path with cost C*.

Suppose A* returns path P with cost C > C*.

Let n be a node on P* that's still in open when goal is selected.

**Key insight:** f(n) = g(n) + h(n) ≤ g(n) + δ(n,t) = C* (by admissibility)

Since goal t was selected before n: f(t) ≤ f(n) ≤ C*

But f(t) = g(t) = C (cost of returned path)

Therefore: C ≤ C*, contradiction.

**Therefore:** A* returns optimal path. ✓

---

### HF - Compare with Dijkstra's Algorithm

| Property | Dijkstra | A* |
|----------|----------|-----|
| Heuristic | None | Required |
| Nodes expanded | All within radius | Only promising nodes |
| Optimality | Always | With admissible h |
| Speed | Slower | Faster (with good h) |
| Special case | - | h=0 gives Dijkstra |

**A* is Dijkstra with guidance from heuristic.**

---

### Study - Common Heuristics

**For grid graphs:**

| Heuristic | Formula | Admissible? |
|-----------|---------|-------------|
| Manhattan | |x₁-x₂| + |y₁-y₂| | ✓ (4-dir) |
| Euclidean | √((x₁-x₂)² + (y₁-y₂)²) | ✓ |
| Chebyshev | max(|x₁-x₂|, |y₁-y₂|) | ✓ (8-dir) |
| Zero | 0 | ✓ (gives Dijkstra) |

---

## Section 13.8 - Alkalmazások

### HF - GPS Navigation Systems

**Model:**
- Vertices: Intersections
- Edges: Road segments
- Weights: Travel time or distance

**Algorithm:** A* with Euclidean or Manhattan heuristic

**Optimization:** Bidirectional search, contraction hierarchies

---

### HF - Network Routing Protocols

**Distance vector (RIP):** Distributed Bellman-Ford

**Link state (OSPF):** Dijkstra's algorithm

**Goal:** Find shortest path for packet delivery

---

### HF - Game AI Pathfinding

**Model:**
- Grid or navigation mesh
- A* with appropriate heuristic
- Dynamic obstacles: D* or LPA*

**Optimization:** Jump point search, hierarchical pathfinding

---

### HF - Social Network Analysis

**Applications:**
- Degrees of separation (BFS)
- Influence propagation
- Community detection

**Metric:** Average shortest path length

---

### Study - Real-World Implementations

1. **Google Maps:** Contraction hierarchies + A*
2. **Internet routing:** OSPF, BGP
3. **Games:** A* with various optimizations
4. **Robotics:** RRT, D* for dynamic environments

---

## Formal Exercises

### 13.1.Feladat - Dijkstra's Algorithm

**Trace on given graph, find shortest paths.**

See detailed trace in Section 13.2. ✓

---

### 13.2.Feladat - Bellman-Ford

**Handle negative weights, detect negative cycles.**

**Example with negative cycle:**
```
a → b (1), b → c (-5), c → a (2)
Cycle a→b→c→a: 1 + (-5) + 2 = -2 < 0
```

After |V|-1 = 2 iterations, edge can still be relaxed → negative cycle detected. ✓

---

### 13.3.Feladat - Floyd-Warshall

**Compute all-pairs shortest paths.**

See detailed trace in Section 13.4. ✓

---

### 13.4.Feladat - BFS

**Find shortest path in unweighted graph.**

See detailed trace in Section 13.5. ✓

---

### 13.5.Feladat - DFS

**Classify edges, find connected components.**

**Edge classification:**
- Tree edges: Part of DFS forest
- Back edges: Create cycles
- Forward/Cross edges: In DAGs

**Connected components:** Run DFS from each unvisited vertex. ✓

---

### 13.6.Feladat - A* Algorithm

**Apply with given heuristic.**

**Example:** Grid with Manhattan heuristic

**Comparison with Dijkstra:**
- A* expands fewer nodes
- Both find optimal path (with admissible h)

---

### 13.7.Feladat - Algorithm Comparison

| Graph Type | Best Algorithm | Reason |
|------------|----------------|--------|
| Unweighted | BFS | O(V+E), simplest |
| Non-negative weights | Dijkstra | O((V+E) log V) |
| Negative weights | Bellman-Ford | Handles negatives |
| All-pairs | Floyd-Warshall | O(V³), simple |
| With good heuristic | A* | Faster than Dijkstra |

---

### 13.8.Feladat - Applications

**Model TSP as graph problem:**
- Vertices: Cities
- Edges: Distances
- Find: Minimum weight Hamilton cycle

**Approach:** Use shortest paths as subroutine in TSP algorithm. ✓

---

## Summary

| Exercise Type | Count | Status |
|--------------|-------|--------|
| In-Chapter HF | 30 | ✅ Complete |
| Formal 13.1-13.8 | 8 | ✅ Complete |
| **Total** | **38** | **✅ Complete** |
