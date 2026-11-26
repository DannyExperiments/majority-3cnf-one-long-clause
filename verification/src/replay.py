"""Replay finite checks for the graph threshold reduction and Akmal's selector."""

from fractions import Fraction
from itertools import combinations, product


def independent_histogram(vertex_count, edges):
    histogram = [0] * (vertex_count + 1)
    for size in range(vertex_count + 1):
        for vertices in combinations(range(vertex_count), size):
            chosen = set(vertices)
            if all(u not in chosen or v not in chosen for u, v in edges):
                histogram[size] += 1
    return histogram


def graph_with_count(count):
    if count < 1:
        raise ValueError("The independent-set count must include the empty set.")
    vertex_count, edges = 0, []
    for bit in bin(count)[3:]:
        vertex_count += 1
        if bit == "1":
            edges.extend((u, vertex_count) for u in range(vertex_count))
            vertex_count += 1
    return vertex_count, edges


def consistency_graph(variable_count, formula):
    groups = [[{i: 0}, {i: 1}] for i in range(variable_count)]
    for clause in formula:
        variables = sorted({variable for variable, _ in clause})
        allowed = []
        for values in product((0, 1), repeat=len(variables)):
            assignment = dict(zip(variables, values))
            if any(assignment[variable] == value for variable, value in clause):
                allowed.append(assignment)
        groups.append(allowed)
    vertices = [(group, values) for group, options in enumerate(groups) for values in options]
    edges = []
    for i, j in combinations(range(len(vertices)), 2):
        left_group, left = vertices[i]
        right_group, right = vertices[j]
        if left_group == right_group or any(left[k] != right[k] for k in left.keys() & right.keys()):
            edges.append((i, j))
    return len(vertices), edges, len(groups)


def twin_edges(edges, size):
    return [(size * u + i, size * v + j) for u, v in edges
            for i, j in product(range(size), repeat=2)]


def normalized_formula(vertex_count, edges, threshold):
    b = (threshold - 1).bit_length()
    target = 1 << b
    added_count, added_edges = graph_with_count(target - threshold + 1)
    joined_count = vertex_count + added_count
    joined_edges = [
        *edges,
        *((u + vertex_count, v + vertex_count) for u, v in added_edges),
        *product(range(vertex_count), range(vertex_count, joined_count)),
    ]
    formula = [((u, 0), (v, 0)) for u, v in joined_edges]
    occurring = {v for edge in joined_edges for v in edge}
    variable_count = joined_count
    for v in sorted(set(range(joined_count)) - occurring):
        formula.extend((((v, 1), (variable_count, 0)), ((v, 0), (variable_count, 0))))
        variable_count += 1
    formula.extend(((v, 0),) for v in range(variable_count, variable_count + b + 1))
    variable_count += b + 1
    return variable_count, formula, variable_count - b


def selector(variable_count, formula, exponent):
    s = variable_count
    y_variables = range(s + 1, s + 1 + exponent)
    long_clause = ((s, 0), *((y, 1) for y in y_variables))
    return s + 1 + exponent, [(*clause, (s, 1)) for clause in formula] + [long_clause]


def count_models(variable_count, formula):
    # Each clause fails only when all its positive variables are false and
    # all its negative variables are true. The bit masks test that condition.
    masks = []
    for clause in formula:
        positive = {v for v, bit in clause if bit}
        negative = {v for v, bit in clause if not bit}
        masks.append((sum(1 << v for v in positive), sum(1 << v for v in negative)))
    return sum(all(row & pos or row & neg != neg for pos, neg in masks)
               for row in range(1 << variable_count))


def check_graph_arithmetic():
    for desired in range(1, 128):
        n, edges = graph_with_count(desired)
        assert sum(independent_histogram(n, edges)) == desired
    print("Prescribed count graphs: 127 exact counts.")

    cases = 0
    for n in range(5):
        candidate_edges = list(combinations(range(n), 2))
        for mask in range(1 << len(candidate_edges)):
            edges = [e for i, e in enumerate(candidate_edges) if mask & (1 << i)]
            histogram = independent_histogram(n, edges)
            count = sum(independent_histogram(2 * n, twin_edges(edges, 2)))
            assert count == sum(a * 3**i for i, a in enumerate(histogram))
            cases += 1
    print(f"Twin replacement: {cases} small graphs checked by enumeration.")


def check_consistency():
    pool = [((0, 0),), ((1, 1),), ((0, 1), (1, 1)), (), ((0, 0), (0, 1))]
    for mask in range(1 << len(pool)):
        formula = [clause for i, clause in enumerate(pool) if mask & (1 << i)]
        model_count = count_models(2, formula)
        n, edges, groups = consistency_graph(2, formula)
        histogram = independent_histogram(n, edges)
        assert sum(histogram[groups:]) == model_count
        assert not any(histogram[groups + 1:])
        weight = (1 << (n + 2)) - 1
        total = sum(count * weight**i for i, count in enumerate(histogram))
        assert 0 <= total - model_count * weight**groups < weight**groups
        for k in range(1, 5):
            threshold = k * weight**groups
            power = 1 << (threshold - 1).bit_length()
            desired = power - threshold + 1
            assert (total + desired - 1 >= power) == (model_count >= k)
    print("Consistency graph: 32 formulas and 128 exact threshold decisions.")


def check_selector_examples():
    cycle = list(zip(range(4), (1, 2, 3, 0)))
    diagonals = [(0, 2), (1, 3)]
    for present in (2, 1, 0):
        edges = cycle + diagonals[:present]
        source = sum(independent_histogram(4, edges))
        assert source == 7 - present
        n, phi, a = normalized_formula(4, edges, 6)
        assert (n, a) == (10, 7) and count_models(n, phi) == source + 2
        total, final = selector(n, phi, a)
        prob = Fraction(count_models(total, final), 1 << total)
        assert prob == Fraction(1025 - present, 2048)
        assert (prob >= Fraction(1, 2)) == (source >= 6)
        print(f"Graph example: I(B)={source}, I(J)={source + 2}, Pr={prob}.")
    for n_input in range(4):
        graph_count = 1 << n_input
        n, phi, a = normalized_formula(n_input, [], 1)
        assert count_models(n, phi) == graph_count
        assert len({v for c in phi for v, _ in c}) == n
        total, final = selector(n, phi, a)
        expected = Fraction(Fraction(graph_count, 1 << n) + 1 - Fraction(1, 1 << a), 2)
        assert Fraction(count_models(total, final), 1 << total) == expected
    print("Empty and isolated graphs: 4 exact endpoint checks.")


def main():
    check_graph_arithmetic()
    check_consistency()
    check_selector_examples()
    print("Q75 finite replay passed.")


if __name__ == "__main__":
    main()
