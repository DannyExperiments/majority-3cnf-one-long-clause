# Q75: Majority with one unrestricted clause is PP-complete

Let `ψ` be a Boolean CNF of width at most three and `L` one unrestricted clause. The language asking whether at least half of uniformly chosen assignments satisfy `ψ ∧ L` is PP-complete under polynomial-time many-one reductions. Ties count as acceptance.

This resolves the question in [Akmal, *Parameterized Relaxations for Circuits and Graphs*, Open Problem 8, printed p. 94](https://www.shyanakmal.com/publications/ShyanAkmal_PhD-Thesis.pdf#page=94), and [pinned Catalog Q75](https://github.com/10m-u/open-problems-catalog/blob/ca8d4d44ba3db527f19f28928c240168f545ecfe/problems/computer_science_ai/theory-of-computation-algorithms-part-1.md#q75). The last reduction is from the thesis, Lemma 4.11. The proof below establishes its required PP-hard source directly and also answers the thesis's Open Problem 9. No priority or peer-review claim is made.

## 1. From PP to counting independent sets above an integer threshold

Start with Majority-Circuit, the PP-complete problem of asking whether a Boolean circuit on r ≥ 1 free input bits accepts at least K = 2^(r−1) of them. For clarity about the usual strict-majority convention for PP, if a machine accepts on A out of 2^r paths and r≥1, add one leading branch bit, use the original circuit in one branch, and accept on exactly 2^(r−1)−1 r-bit strings in the other. Non-strict majority of the resulting 2^(r+1) paths holds iff A≥2^(r−1)+1. A polynomial-size circuit simulating a polynomial-time computation on its random bits, and a binary comparator for the extra branch, suffice.

Use a circuit basis AND, OR, NOT. Introduce each gate output as a new variable; assert equivalence to its inputs by the standard equivalence clauses of widths at most three, and assert the final output with a positive unit clause. For example z = x AND y yields (¬z∨x), (¬z∨y), and (z∨¬x∨¬y), with the dual clauses for OR; z = NOT x yields (z∨x) and (¬z∨¬x). Fix constants by units. Each original input assignment has exactly one extension satisfying all gate-equivalence clauses, and that extension satisfies the output clause exactly when the circuit accepts. Thus the resulting 3-CNF F has exactly A satisfying assignments, including every original free bit in its declared variable universe even if unused. The threshold K still uses r, not the number of formula variables.

Construct a graph G by making one group for each clause and one group for each declared variable. For a clause, the group contains a vertex for every assignment to its distinct variables satisfying the clause. For a variable, it contains two vertices for its two assignments. Add edges within each group and between vertices of distinct groups whenever their assignments disagree on a common variable. There are m groups, and there are no independent sets of size greater than m. Independent sets of size m select exactly one vertex per group; because of the variable groups, consistency gives a complete assignment, with exactly one choice per clause group. This is a bijection between independent sets of size m and satisfying assignments of F. If any clause has no allowed assignment this statement remains true: both counts vanish. Let a_i be the number of independent sets of size i in G, so a_m = A. Let v be the number of vertices of G.

Replace each vertex by t = v+2 mutually nonadjacent twins; between twin classes corresponding to an original edge put all possible edges. Write B for this new graph, and W = 2^t−1. Any independent set of B projects to an independent set of G by retaining classes with nonempty intersection; every chosen class has W independent, nonempty selections, regardless of the other choices. Hence, writing I for the number of independent sets including the empty set,
```
I(B) = Σ_{i=0}^m a_i W^i = A W^m + R.
```
Here 0≤R≤W^(m−1)·2^v<W^m, since there are at most 2^v subsets of the original vertices, W>2^v, and m≥1. Therefore I(B) ≥ T = K W^m iff A ≥ K.

## 2. Convert an arbitrary integer threshold to a power of two

Take b to be the smallest nonnegative integer with 2^b≥T, and set D=2^b−T+1≥1. Any positive integer D occurs as I(H) for a graph H of at most 2(floor(log₂ D)) vertices: begin with the empty graph (count 1), read the remaining digits of D after its leading binary 1, and for each digit add an isolated vertex to double the count and then, if the digit is 1, a universal vertex to increase it by 1. The latter has exactly one independent set containing the new vertex, the singleton.

Build J as the join of B and H on disjoint vertex sets. An independent set lies entirely on one side, and the empty set lies on both, giving I(J)=I(B)+D−1. Consequently I(J)≥2^b iff I(B)≥T.

Create a 2-CNF φ with one variable per vertex of J and clause (¬x_u∨¬x_v) per edge uv. To avoid any dependence on whether a formula's variable convention permits absent variables, represent each isolated vertex x_v by an extra private variable w_v and clause (¬w_v). Then also replace (¬w_v) by (x_v∨¬w_v) ∧ (¬x_v∨¬w_v), which explicitly mentions x_v and has a unique extension for each value of x_v. This change adds no satisfying assignments. Append b+1 fresh variables with negative unit clauses, again without changing the number of satisfying assignments. With N the number of occurring variables in φ, we have N≥b+1, and
```
Pr[φ] ≥ 2^(−a) iff I(J) ≥ 2^b,   where a = N−b ≥ 1.
```
This also proves PP-hardness of the dyadic 2-CNF threshold problem (thesis Open Problem 9). Membership is immediate by comparison of a #P count to the integer threshold, with thresholds below 1 assignment handled by 2-SAT.

All constructions are polynomial in the original circuit size. In particular v and m are polynomial, B has vt vertices, log₂ T=O(r+mt), H uses O(log T) vertices, and a is O(N).

## 3. Reduce the dyadic comparison to the stated majority problem

Use Akmal's Lemma 4.11. Let s,y₁,…,yₐ be distinct fresh variables. Add literal s to each clause of φ to obtain a 3-CNF ψ, and take the single long clause L=(¬s∨y₁∨⋯∨yₐ).

Condition on s. At s=0, L is true and ψ asks for φ. At s=1, ψ is true and L fails precisely when all y's are false. Thus
```
Pr[ψ ∧ L] = (Pr[φ]+1−2^(−a))/2.
```
This is at least 1/2 exactly when Pr[φ] is at least 2^(−a). The unused-variable issue does not reappear: all variables of φ occur in ψ and all y's occur in L.

Every formula equivalence is exact, including equality. Membership in PP follows by evaluating ψ ∧ L on uniformly guessed bits. If defining PP by strict majority exclusively, use one leading branch bit: the original formula is checked on one branch and on the other accept for exactly 2^(n−1)+1 strings on the same n bits. Then the resulting total strictly exceeds 2^n iff the original accepts at least 2^(n−1); a zero-variable instance is decided directly. The reduction and membership prove PP-completeness.
