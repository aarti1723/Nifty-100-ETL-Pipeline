def free_cash_flow(cfo, cfi):
    return cfo + cfi


def cfo_quality_score(cfo, pat):
    if pat == 0:
        return None

    score = cfo / pat

    if score > 1:
        return "High Quality"
    elif score >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    if sales == 0:
        return None

    return abs(investing_activity) / sales * 100


def fcf_conversion(fcf, operating_profit):
    if operating_profit == 0:
        return None

    return fcf / operating_profit * 100