def glossing_machine(glossed, tags):
    align_result = alignment(glossed)
    main_type, has_alt = morph(glossed)
    word_order = detector(tags)

    align_map = {
        'Эргативная': 'Ergative',
        'Аккузативная': 'Accusative',
        'Расщеплённая эргативность': 'Unknown',
        'Не определено': 'Unknown'
    }
    align_key = align_result.split()[0]
    align = align_map.get(align_key, 'Unknown')

    # Получаем результат для основного типа
    res_main = format_guess(word_order, align, main_type)

    if not has_alt:
        if res_main is None:
            return "простите по данному отрывку невозможно определить ареал распространения языка"
        return res_main

    # Есть альтернатива: пытаемся получить результат для альтернативного типа
    alt_type = 'Fusional' if main_type == 'Agglutinative' else 'Agglutinative'
    res_alt = format_guess(word_order, align, alt_type)

    if res_alt is None:
        if res_main is None:
            return "простите по данному отрывку невозможно определить ареал распространения языка"
        return res_main + f"\n\nПримечание: возможно также {param_label(alt_type)} (но данные о таком сочетании отсутствуют)."

    # Разбираем строки
    lines_main = res_main.split('\n')
    lines_alt = res_alt.split('\n')

    # Объединяем ареалы и примеры через " / "
    areas_main = lines_main[0].split(':', 1)[1].strip()
    areas_alt = lines_alt[0].split(':', 1)[1].strip()
    combined_areas = f"Ареалы распространения: {areas_main} (возможно: {areas_alt})"

    examples_main = lines_main[1].split(':', 1)[1].strip()
    examples_alt = lines_alt[1].split(':', 1)[1].strip()
    combined_examples = f"Примеры языков: {examples_main} (возможно: {examples_alt})"

    # Порядок слов и строй языка берём из основного
    word_order_line = lines_main[2]
    alignment_line = lines_main[3]

    # Тип морфологической структуры объединённый
    morphology_line = f"Тип морфологической структуры: {param_label(main_type)}, но возможен {param_label(alt_type)}."

    result = f"{combined_areas}\n{combined_examples}\n{word_order_line}\n{alignment_line}\n{morphology_line}"
    return result
