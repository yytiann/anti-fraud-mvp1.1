def strong_rules(row):
    reasons = []

    if row["days_policy_to_claim"] <= 30:
        reasons.append("短期投保")

    if row["claim_count_1y"] >= 3:
        reasons.append("高频报案")

    if row["was_investigated"] == 1:
        reasons.append("曾被调查")

    return reasons