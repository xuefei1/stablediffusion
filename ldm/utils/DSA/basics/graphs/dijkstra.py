

def dijkstra(nodes, src2dst, cost_dict, src, dst):
    """
    Min cost between two points.
    Theta(|E| + |V|log|V|) time.
    O(|V| + |E|) space?
    """
    completed = {}
    undetermined = {n:float("inf") for n in nodes}
    undetermined[src] = 0
    while dst not in completed and len(undetermined) > 0:
        # TODO: Replace with min heap to get the optimal time complexity
        curr_src, min_cost = sorted(list(undetermined.items()), key=lambda t:t[-1])[0] # Here's the greedy part
        completed[curr_src] = min_cost
        del undetermined[curr_src]
        for n in src2dst[curr_src]:
            if n in completed: continue
            cost = cost_dict[tuple(sorted([curr_src, n]))]
            new_cost = min_cost + cost
            if new_cost < undetermined[n]:
                undetermined[n] = new_cost
    return completed[dst]


if __name__ == "__main__":
    print(dijkstra(
        nodes=["A", "B", "C", "D", "E", "F"],
        src2dst={
            "A": {"B", "D", "F"},
            "B": {"A", "C"},
            "C": {"B", "D", "E"},
            "D": {"A", "C", "E"},
            "E": {"C", "D", "F"},
            "F": {"A", "E"},
        },
        cost_dict={
            ("A", "B"): 5,
            ("A", "D"): 7,
            ("A", "F"): 6,
            ("B", "C"): 6,
            ("C", "D"): 3,
            ("C", "E"): 3,
            ("D", "E"): 2,
            ("E", "F"): 4,
        },
        src="A",
        dst="E",
    ))
