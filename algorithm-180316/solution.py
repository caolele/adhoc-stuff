def find_bc(a, b_list):
    tuples = []
    for b in b_list:
        for c in b_list[b_list.index(b) + 1:]:
            if b + c == -a:
                tuples.append((b, c))
    return tuples


def main(int_list):
    int_list.sort()
    triplets = []
    for a in int_list:
        bc_tuples = find_bc(a, int_list[int_list.index(a) + 1:])
        num_bc = len(bc_tuples)
        if num_bc > 0:
            a_repeat = [(a,)] * num_bc
            triplets = triplets + [(a_repeat[i] + bc_tuples[i]) for i in range(num_bc)]
    print(set(triplets))


if __name__ == "__main__":
    main([-1, 0, 1, 2, -1, -4])
