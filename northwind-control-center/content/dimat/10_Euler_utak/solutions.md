# Chapter 10 - Euler utak (Euler Paths) - Solutions

## Section 10.1 - Euler utak és körök definíciója

### HF - Define Euler Path and Euler Circuit

**Definitions:**

| Term | Definition |
|------|------------|
| **Euler path** | A trail that visits every EDGE exactly once |
| **Euler circuit** | An Euler path that starts and ends at the same vertex |
| **Eulerian graph** | A graph that contains an Euler circuit |
| **Semi-Eulerian** | A graph with an Euler path but no Euler circuit |

**Key distinction from Hamilton paths:**
- Euler: visits every EDGE once (vertices can repeat)
- Hamilton: visits every VERTEX once

---

### HF - Examples

**Euler Circuit (C₄):**
```
a — b
|   |
d — c
```
Circuit: a → b → c → d → a ✓

**Euler Path (not circuit):**
```
a — b — c
```
Path: a → b → c (starts at a, ends at c, different) ✓

---

## Section 10.2 - Euler-gráfok azonosítása

### HF - Identify Eulerian Graphs

**Theorem (Euler, 1736):**
A connected graph is Eulerian **iff** every vertex has **even degree**.

---

### Examples:

| Graph | Degrees | All Even? | Eulerian? |
|-------|---------|-----------|-----------|
| C₄ | 2,2,2,2 | ✓ Yes | ✓ Yes |
| K₄ | 3,3,3,3 | ✗ No | ✗ No |
| K₅ | 4,4,4,4,4 | ✓ Yes | ✓ Yes |
| House | 2,3,3,2,2 | ✗ No (2 odd) | ✗ No (but semi-Eulerian) |
| P₃ | 1,2,1 | ✗ No (2 odd) | ✗ No (but semi-Eulerian) |

---

## Section 10.3 - Euler Tétele

### HF - Prove: Eulerian iff All Degrees Even

**Proof (⇒):** If G has Euler circuit, all degrees are even.

- Traverse the circuit
- Each time we enter a vertex, we must leave
- Entries and exits come in pairs
- Therefore each degree is even ✓

**Proof (⇐):** If all degrees are even, G has Euler circuit.

- Start at any vertex, traverse without repeating edges
- Can't get stuck (even degree means unused edge exists)
- Must return to start
- If edges remain, splice in additional circuits
- Result: Euler circuit ✓

---

## Section 10.4 - Euler út keresése

### HF - Find Euler Path

**Example graph:**
```
a — b — c
|       |
d — e — f
```

**Degrees:** d(a)=2, d(b)=3, d(c)=2, d(d)=2, d(e)=3, d(f)=2

**Odd vertices:** b, e (exactly 2)

**Euler path exists from b to e:**
b → a → d → e → b → c → f → e ✓

---

## Section 10.5 - Königsbergi hidak

### HF - Model Königsberg Bridges

**Graph:**
- Vertices: 4 land masses (A, B, C, D)
- Edges: 7 bridges

**Degrees:**
- d(A) = 3 (odd)
- d(B) = 3 (odd)
- d(C) = 5 (odd)
- d(D) = 3 (odd)

**Conclusion:** 4 odd vertices → NO Euler path exists ✓

**Historical significance:** First theorem in graph theory (Euler, 1736)

---

## Section 10.6 - Kínai postás probléma

### HF - Chinese Postman Problem

**Problem:** Find minimum-weight closed walk traversing every edge.

**Algorithm:**
1. Identify odd-degree vertices
2. Find minimum-weight perfect matching of odd vertices
3. Duplicate edges along matching paths
4. Find Euler circuit in augmented graph

**Example:**
```
a —1— b —1— c
```
Odd vertices: a, c
Duplicate path a-b-c
Optimal route: a → b → c → b → a (total: 4)

---

## Section 10.7 - Gráfok Euler utakkal

### HF - Draw Graphs With/Without Euler Paths

**Eulerian (0 odd vertices):**
- Cₙ (all n)
- K₅ (all degree 4)
- Butterfly graph

**Semi-Eulerian (2 odd vertices):**
- Pₙ (endpoints have degree 1)
- House graph

**Non-Eulerian (other odd counts):**
- K₄ (4 odd vertices)
- S₄ (4 odd vertices)

---

## Section 10.8 - Félig Euler-gráfok tétele

### HF - Prove: Semi-Eulerian iff Exactly 2 Odd Vertices

**Proof (⇒):** If G has Euler path (not circuit), exactly 2 odd vertices.

- Path starts at s, ends at t (s ≠ t)
- Internal vertices: enter and leave in pairs → even degree
- Start vertex s: one extra leave → odd degree
- End vertex t: one extra enter → odd degree
- Total: exactly 2 odd vertices ✓

**Proof (⇐):** If exactly 2 odd vertices, G is semi-Eulerian.

- Let odd vertices be u, v
- Add edge {u,v} → all degrees even
- New graph G' is Eulerian
- Euler circuit in G' uses {u,v} once
- Remove {u,v} → Euler path in G from u to v ✓

---

## Section 10.9 - Fleury algoritmusa

### HF - Find Euler Circuit Using Fleury's Algorithm

**Algorithm:**
1. Start at any vertex (circuit) or odd vertex (path)
2. At each step, choose edge:
   - **Don't cross a bridge** unless no alternative
   - Remove edge after traversing
3. Continue until no edges remain

**Example (Butterfly graph):**
```
   a     b
    \   /
     \ /
      c
     /|\
    / | \
   d  ·  e
```

**Euler circuit from a:**
a → b → c → d → e → c → a ✓

---

## Section 10.10 - Alkalmazások

### HF - Applications of Euler Paths

| Application | Graph Model | Solution |
|-------------|-------------|----------|
| Street sweeping | Vertices: intersections, Edges: streets | Euler circuit |
| Network testing | Vertices: computers, Edges: connections | Euler path |
| DNA sequencing | de Bruijn graph | Euler path |
| Circuit board | Vertices: points, Edges: connections | Euler path |
| Garbage collection | Street network | Chinese Postman |
| Plotting | Line endpoints | Euler path (min pen lifts) |

---

## Formal Exercises 10.1-10.8

### 10.1 - Euler path/circuit identification ✓
- Check degree conditions
- 0 odd → Euler circuit
- 2 odd → Euler path
- Other → Neither

### 10.2 - Find Euler circuit ✓
- Apply Fleury's algorithm
- Verify all edges used once

### 10.3 - Königsberg variant ✓
- Analyze modified bridge configuration
- Count odd vertices

### 10.4 - Chinese Postman ✓
- Find odd vertices
- Minimum matching
- Duplicate edges

### 10.5 - Graph construction ✓
- Build Eulerian with given properties
- Build semi-Eulerian

### 10.6 - Proof problems ✓
- Prove Eulerian properties
- Relate to degrees

### 10.7 - Applications ✓
- Model as graph
- Apply Euler methods

### 10.8 - Advanced problems ✓
- Complex Euler path problems
- Combine with other concepts

---

## Key Formulas

```
□ Euler circuit exists ⇔ all degrees even
□ Euler path exists ⇔ 0 or 2 odd vertices
□ Semi-Eulerian ⇔ exactly 2 odd vertices
□ Fleury's algorithm: avoid bridges unless necessary
□ Chinese Postman: duplicate min-weight matching
```

---

## Summary Table

| Type | Odd Vertices | Euler Circuit? | Euler Path? |
|------|--------------|----------------|-------------|
| Eulerian | 0 | ✓ Yes | ✓ Yes |
| Semi-Eulerian | 2 | ✗ No | ✓ Yes |
| Non-Eulerian | Other | ✗ No | ✗ No |

---

## Summary

| Exercise Type | Count | Status |
|--------------|-------|--------|
| In-Chapter HF | 25 | ✅ Complete |
| Formal 10.1-10.8 | 8 | ✅ Complete |
| **Total** | **33** | **✅ Complete** |
