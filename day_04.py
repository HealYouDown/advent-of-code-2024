import typing as t
from dataclasses import dataclass

T_PUZZLE = list[list[str]]


@dataclass
class WordPuzzle:
    rows: list[list[str]]

    @classmethod
    def load(cls, fpath: str) -> t.Self:
        rows = []
        with open(fpath, "r") as fp:
            for line in fp.read().splitlines():
                if not line:
                    continue

                rows.append(list(line))

        return cls(rows=rows)

    @property
    def width(self) -> int:
        return len(self.rows[0])

    @property
    def height(self) -> int:
        return len(self.rows)

    def _get_values_for_positions(self, positions: list[tuple[int, int]]) -> list[str]:
        return [
            self.rows[y][x]
            for x, y in positions
            if 0 <= y < self.height and 0 <= x < self.width
        ]

    def _get_left_to_right(self, x: int, y: int, len: int) -> list[str]:
        pos = [(i, y) for i in range(x, x + len)]
        return self._get_values_for_positions(pos)

    def _get_right_to_left(self, x: int, y: int, len: int) -> list[str]:
        pos = [(i, y) for i in range(x, x - len, -1)]
        return self._get_values_for_positions(pos)

    def _get_top_to_bottom(self, x: int, y: int, len: int) -> list[str]:
        pos = [(x, i) for i in range(y, y + len)]
        return self._get_values_for_positions(pos)

    def _get_bottom_to_top(self, x: int, y: int, len: int) -> list[str]:
        pos = [(x, i) for i in range(y, y - len, -1)]
        return self._get_values_for_positions(pos)

    def _get_top_left_to_bottom_right(self, x: int, y: int, len: int) -> list[str]:
        pos = [(x + i, y + i) for i in range(len)]
        return self._get_values_for_positions(pos)

    def _get_top_right_to_bottom_left(self, x: int, y: int, len: int) -> list[str]:
        pos = [(x - i, y + i) for i in range(len)]
        return self._get_values_for_positions(pos)

    def _get_bottom_left_to_top_right(self, x: int, y: int, len: int) -> list[str]:
        pos = [(x + i, y - i) for i in range(len)]
        return self._get_values_for_positions(pos)

    def _get_bottom_right_to_top_left(self, x: int, y: int, len: int) -> list[str]:
        pos = [(x - i, y - i) for i in range(len)]
        return self._get_values_for_positions(pos)

    def count_word_at_position(self, x: int, y: int, word: str = "XMAS") -> int:
        direction_checks: list[t.Callable[[int, int, int], list[str]]] = [
            self._get_left_to_right,
            self._get_right_to_left,
            self._get_top_to_bottom,
            self._get_bottom_to_top,
            self._get_top_left_to_bottom_right,
            self._get_top_right_to_bottom_left,
            # Could prob just reverse tl-br and tr-bl
            self._get_bottom_left_to_top_right,
            self._get_bottom_right_to_top_left,
        ]

        count = 0
        for check in direction_checks:
            if check(x, y, len(word)) == list(word):
                count += 1

        return count

    def is_x_mas_cross(self, x: int, y: int) -> bool:
        # Our center location has to be an "A" for it to be a valid x-mas
        start_letter = self.rows[y][x]
        if start_letter != "A":
            return False

        to_find = ["M", "A", "S"]

        # Check top left to bottom right diagonal
        tl_to_br = self._get_top_left_to_bottom_right(x - 1, y - 1, 3)
        br_to_tl = self._get_bottom_right_to_top_left(x + 1, y + 1, 3)
        if not (tl_to_br == to_find or br_to_tl == to_find):
            return False

        # Check top right to bottom left diagonal
        tr_to_bl = self._get_top_right_to_bottom_left(x + 1, y - 1, 3)
        bl_to_tr = self._get_bottom_left_to_top_right(x - 1, y + 1, 3)
        if not (tr_to_bl == to_find or bl_to_tr == to_find):
            return False

        return True


if __name__ == "__main__":
    puzzle = WordPuzzle.load("./inputs/day_04.txt")
    count_p1 = sum(
        puzzle.count_word_at_position(x, y)
        for x in range(puzzle.width)
        for y in range(puzzle.height)
    )
    print("Puzzle 1:", count_p1)

    count_p2 = sum(
        puzzle.is_x_mas_cross(x, y)
        for x in range(puzzle.width)
        for y in range(puzzle.height)
    )
    print("Puzzle 2:", count_p2)
