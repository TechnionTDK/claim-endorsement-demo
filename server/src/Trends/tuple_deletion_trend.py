
# tuple deletion generic algorithm

class TupleDeletionSolver(object):
    def __init__(self):
        pass

    def set_of_values(self, db, attr):
        return []

    def solve_for_single_group(self, group, lower, upper):
        # return the solution and its cost
        pass

    def solve_up_to_i(self, groups, upper):
        if len(groups) == 1:
            return self.solve_for_single_group(groups[0], min(self.set_of_values()), upper)

        solutions = []
        best_cost = sum([len(g) for g in groups])  # worst case scenario - remove all items
        best_sol = None
        for b in self.set_of_values():
            subgroup_i, cost_i = self.solve_for_single_group(groups[-1], b, upper)
            subgroups, cost = self.solve_up_to_i(groups[:-1], b)
            total_cost = cost + cost_i
            total_subgroups = subgroups + [subgroup_i]
            solutions.append((total_cost, total_subgroups))
            if total_cost < best_cost:
                best_cost = total_cost
                best_sol = total_subgroups
        return best_sol