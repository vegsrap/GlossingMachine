from alignment import alignment
from morphology import morph
from word_order import detector, main
from area import format_guess


def glossing_machine(glossed, tags):
        align = alignment(glossed)
        morphology = morph(glossed)
        word_order = detector(tags)

        align_map = {
            'Эргативная': 'Ergative',
            'Аккузативная': 'Accusative',
            'Расщеплённая эргативность': 'Unknown',
            'Не определено': 'Unknown'
        }

        # берём только первое слово из результата alignment
        align_key = align.split()[0]
        align = align_map.get(align_key, 'Unknown')
        return format_guess(word_order, align, morphology)


if __name__ == "__main__":
    text = input("Введите Ваш текст (глоссы строго через дефис, ПРИМЕР: я-ERG-1SG собака-ABS видеть-PST-PFV): ")
    vso = input("Введите теги частей речи через пробел (N – noun, V – verb, PRO – pronoun и т.д.): ")
    result = glossing_machine(text, vso)
    print(result)


