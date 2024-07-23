import itertools as it


def generate_sample_space(die: list[int]) -> list[tuple[int, ...]]:
    return list(it.product(die, repeat=2))


def calculate_my_win_probability(me: list[int], you: list[int]) -> float:
    my_sample_space = generate_sample_space(me)
    your_sample_space = generate_sample_space(you)

    times_I_win = possible_outcomes = 0
    for my_roll, your_roll in it.product(my_sample_space, your_sample_space):
        possible_outcomes += 1
        if sum(my_roll) > sum(your_roll):
            times_I_win += 1

    return times_I_win / possible_outcomes


if __name__ == "__main__":
    A = [2, 2, 6, 6, 7, 7]
    B = [1, 1, 5, 5, 9, 9]
    C = [3, 3, 4, 4, 8, 8]

    c_b = calculate_my_win_probability(C, B)
    a_c = calculate_my_win_probability(A, C)
    b_a = calculate_my_win_probability(B, A)

    print(f"C vs. B: C wins with probability {c_b}.")
    print(f"A vs. C: A wins with probability {a_c}.")
    print(f"B vs. A: B wins with probability {b_a}.")
