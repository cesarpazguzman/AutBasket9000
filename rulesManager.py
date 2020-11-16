def get_matches_filtered(matches):
    res = []
    for match in matches:
        if float(match['cuotaPreviaL']) < 1.3 and float(match['cuotaVivoL'])>2\
                or float(match['cuotaPreviaV']) < 1.3 and float(match['cuotaVivoV'])>2:
                res.append(match)
                break

    return res
