def detector(glosses):
    slova = glosses.strip().split()

    v_index = -1
    for i, token in enumerate(slova):
        if token == 'V':
            v_index = i
            break

    s_index = -1
    for i, token in enumerate(slova):
        if token in ('N', 'PRO'):
            s_index = i
            break

    if s_index == -1 or v_index == -1:
        return "UNKNOWN"

    o_index = -1
    for i in range(len(slova)):
        if slova[i] in ('N', 'PRO') and i != s_index:
            o_index = i
            break

    if o_index == -1:
        return "UNKNOWN"

    if s_index < v_index < o_index:
        return "SVO"
    elif s_index < o_index < v_index:
        return "SOV"
    elif v_index < s_index < o_index:
        return "VSO"
    else:
        return "UNKNOWN"


def main():
    user = input().strip()
    if user:
        result = detector(user)
        print(result)
    else:
        print("UNKNOWN")


if __name__ == "__main__":
    main()
