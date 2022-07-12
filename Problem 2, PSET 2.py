from __future__ import annotations

import copy

import numpy as np


class Classroom:

    OFFSETS = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    TEST_GRID = np.array(
        [
            [1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    TEST_GRID_n = len(TEST_GRID)
    TEST_GRID_m = np.sum(TEST_GRID)

    def __init__(self, n: int = 0, m: int = 0, is_print: bool = False):
        if is_print:
            print(f"\nNEW {n} x {n} class with {m} infected students initially\n")

        self.n = Classroom.TEST_GRID_n if not n else n
        self.m = Classroom.TEST_GRID_m if not m else m
        self.is_print = is_print

        # Random placement of infected students initially if `m`, `n` provided
        random_seat_grid = np.zeros(n**2)
        initial_infected_idx = np.random.choice(n**2, m, replace=False)
        random_seat_grid[initial_infected_idx] = 1

        self.seat_grid = (
            Classroom.TEST_GRID if not (m or n) else random_seat_grid.reshape(n, n)
        )

        self.boundary_length = self._measure_boundary()

        if self.is_print:
            print("\n", np.array2string(self.seat_grid, prefix=" "), "\n")
            print(f"Boundary length: {self.boundary_length}\n")

    def _update_grid(self) -> int:
        new_grid = copy.copy(self.seat_grid)
        for i in range(self.n):
            for j in range(self.n):
                if self.seat_grid[i, j] == 0:
                    adj_infected = 0
                    for x, y in Classroom.OFFSETS:
                        if not (
                            i + x < 0 or j + y < 0 or i + x >= self.n or j + y >= self.n
                        ):
                            adj_infected += (
                                1 if self.seat_grid[i + x, j + y] == 1 else 0
                            )
                            if adj_infected >= 2:
                                new_grid[i, j] = 1

        self.seat_grid = new_grid
        self.boundary_length = self._measure_boundary()
        return np.sum(self.seat_grid)

    def _measure_boundary(self) -> int:
        boundary_length = 0
        for i in range(self.n):
            for j in range(self.n):
                adj_not_infected = 0
                if self.seat_grid[i, j] == 1:
                    if i == 0 or i == self.n - 1:
                        adj_not_infected += 1
                    if j == 0 or j == self.n - 1:
                        adj_not_infected += 1
                    for x, y in Classroom.OFFSETS:
                        if not (
                            i + x < 0 or j + y < 0 or i + x >= self.n or j + y >= self.n
                        ):
                            adj_not_infected += (
                                1 if self.seat_grid[i + x, j + y] == 0 else 0
                            )
                boundary_length += adj_not_infected
        return boundary_length

    def play(self) -> None:
        last_total = self.m
        while True:
            last_boundary_length = self.boundary_length
            current_total = self._update_grid()
            if last_total == current_total:
                break
            last_total = current_total
            if self.is_print:
                print("\n", np.array2string(self.seat_grid, prefix=" "), "\n")
                print(f"Boundary Length Δ: {self.boundary_length - last_boundary_length}")
                print(f"Boundary Length: {self.boundary_length}\n")
        if self.is_print and np.sum(self.seat_grid) == self.n**2:
            print("All students infected!")


def main():
    import os
    import sys

    g = 1
    if len(sys.argv) == 4:
        n, m, g = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    elif len(sys.argv) == 3:
        n, m = int(sys.argv[1]), int(sys.argv[2])
    else:
        print(
            f"Usage: {os.path.basename(__file__)} n m g; defaulting to 1 manual grid!"
        )
        n = m = 0

    is_print = input("Print outputs? ('Y', 'y') ") in ("Y", "y")
    print("\n")

    for _ in range(g):
        c = Classroom(n, m, is_print)
        c.play()
        del c


if __name__ == "__main__":
    main()
