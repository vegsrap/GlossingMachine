def morph(glossed):
    dash = glossed.count('-')
    dot = glossed.count('.')
    total_words = 0
    total_morph = 0
    for i in glossed.split():
        total_words += 1
        total_morph += i.count('-')
    synthetic_index = total_morph / total_words

    tense = {'PST', 'FUT', 'PRS', 'IPFV', 'PFV'}
    person = {'1', '2', '3'}
    number = {'PL', 'SG', 'DU'}
    case = {'ERG', 'ABS', 'NOM', 'ACC', 'DAT', 'GEN'}
    found_categories = set()
    morphh = []
    for j in glossed.split():
        morphee = j.split('-')
        morphee.pop(0)
        morphh.extend(morphee)

    for o in morphh:
        m_upper = o.upper()
        if m_upper in tense:
            found_categories.add('tense')
        if m_upper in person:
            found_categories.add('person')
        if m_upper in number:
            found_categories.add('number')
        if m_upper in case:
            found_categories.add('case')

    if total_words == 0:
        return 'Не определено'

    total_signs = dash + dot
    if total_signs == 0:
        ratio = 0
    else:
        ratio = dash / total_signs

    diversity = len(found_categories)

    if synthetic_index < 1.5:
        return 'Isolating'
    elif synthetic_index > 3.5:
        return 'Polysynthetic'
    elif ratio >= 0.7:
        return 'Agglutinative'
    elif dot > dash:
        return 'Fusional'
    else:
        return 'Не определено'