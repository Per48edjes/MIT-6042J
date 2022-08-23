UNIQUE_STATES = set()


def state_generator(red: int, green: int, unique_states: set) -> None:
    if (red < 0) or (green < 0):
        return
    if (red, green) not in unique_states:
        unique_states.add((red, green))
        state_generator(green, red, unique_states),
        state_generator(red - 3, green + 2, unique_states),


def longest_state_execution_check(state, unique_states) -> list:
    sequence = []
    while state in unique_states:
        sequence.extend([state, tuple(reversed(state))])
        if (state := (state[0] - 3, state[1] + 2)):
            state = tuple(reversed(state))
    return sequence


def state_check(unique_states: set) -> bool:
    return all(
        (s[1], s[0]) in unique_states and (s[0] - s[1]) % 5 in (2, 3)
        for s in unique_states
    )


def main() -> None:
    state_generator(15, 12, UNIQUE_STATES)
    if state_check(UNIQUE_STATES):
        print(f"Number of unique states: {len(UNIQUE_STATES)}")
        print(
            f"Longest sequence: "
            f"{len(longest_state_execution_check((15, 12), UNIQUE_STATES))}"
        )


if __name__ == "__main__":
    main()
