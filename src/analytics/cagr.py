def calculate_cagr(start, end, years):
    if years <= 0:
        return None

    if start == 0:
        return None

    if start < 0 and end < 0:
        return None

    if start < 0 and end > 0:
        return None

    if start > 0 and end < 0:
        return None

    return ((end / start) ** (1 / years) - 1) * 100

def revenue_cagr(start_sales, end_sales, years):
    return calculate_cagr(start_sales, end_sales, years)


def pat_cagr(start_pat, end_pat, years):
    return calculate_cagr(start_pat, end_pat, years)


def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)