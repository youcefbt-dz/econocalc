def build_initial_simplex_tableau(objective, constraints, rhs_vals, signs, maximize=True):
    return {
        "tableau": [],
        "objective": [],
        "header": [],
        "basic_vars": []
    }

def pivot_simplex_step(tableau, objective, basic_vars, header):
    return {
        "tableau": tableau,
        "objective": objective,
        "header": header,
        "basic_vars": basic_vars
    }
