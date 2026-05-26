def alignment(glossed):
    s = []
    for i in glossed.split():
        parts = i.split('-')
        s.extend(parts)

    erg_count = s.count("ERG")
    abs_count = s.count("ABS")
    nom_count = s.count("NOM")
    acc_count = s.count("ACC")

    erg_score = erg_count + abs_count
    acc_score = nom_count + acc_count
    total = erg_score + acc_score

    if total < 2:
        return "Не определено"

    erg_ratio = erg_score / total
    acc_ratio = acc_score / total

    if erg_ratio >= 0.2 and acc_ratio >= 0.2:
        return f"Расщеплённая эргативность (эрг: {erg_ratio:.0%}, акк: {acc_ratio:.0%})"
    if erg_ratio > acc_ratio:
        return f"Эргативная ({erg_ratio:.0%} маркеров)"
    elif acc_ratio > erg_ratio:
        return f"Аккузативная ({acc_ratio:.0%} маркеров)"
    else:
        return "Не определено"