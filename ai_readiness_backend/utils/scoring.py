def compute_scores(data):
    # Example logic for each readiness section
    use_case = data['use_case']
    data_readiness = data['data_readiness']
    tech_infra = data['tech_infra']
    team = data['team_readiness']

    use_case_score = (use_case['value'] + use_case['feasibility'] + use_case['priority']) / 3
    data_score = (data_readiness['data_availability'] + data_readiness['data_quality'] + data_readiness['integration_level']) / 3
    tech_score = (tech_infra['compute_power_score'] + tech_infra['tools_stack_maturity']) / 2 + (20 if tech_infra['cloud_ready'] else 0) + (20 if tech_infra['apis_ready'] else 0)
    tech_score = min(tech_score, 100)
    team_score = (team['ai_skills_level'] + team['leadership_support']) / 2

    total_score = (use_case_score + data_score + tech_score + team_score) / 4

    return {
        'use_case': round(use_case_score, 2),
        'data': round(data_score, 2),
        'tech': round(tech_score, 2),
        'team': round(team_score, 2),
        'total': round(total_score, 2)
    }
