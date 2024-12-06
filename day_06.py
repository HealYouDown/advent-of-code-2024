import enum
import typing as t
from dataclasses import dataclass


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def add_delta(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, tuple):
            return other[0] == self.x and other[1] == self.y
        elif isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        raise ValueError(f"Can't compare {other!r} with Point")

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Direction(enum.IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def get_movement(self) -> tuple[int, int]:
        if self == Direction.NORTH:
            return (0, -1)
        elif self == Direction.EAST:
            return (1, 0)
        elif self == Direction.SOUTH:
            return (0, 1)
        elif self == Direction.WEST:
            return (-1, 0)
        t.assert_never(self)

    def rotate_right(self) -> "Direction":
        value = self.value
        new_direction_value = (value + 1) % 4
        return Direction(new_direction_value)


@dataclass
class GuardMapInfo:
    width: int
    height: int

    obstructions: list[Point]
    guard_initial_position: Point
    guard_initial_direction: Direction


def puzzle_1(map: GuardMapInfo) -> None:
    pos = map.guard_initial_position
    direction = map.guard_initial_direction
    visited: set[Point] = set()

    in_map = (  # noqa: E731
        lambda pos: pos.x >= 0
        and pos.x < map.width
        and pos.y >= 0
        and pos.y < map.height
    )
    while in_map(pos):
        next_pos = pos.add_delta(*direction.get_movement())
        if next_pos in map.obstructions:
            direction = direction.rotate_right()
            next_pos = pos.add_delta(*direction.get_movement())

        pos = next_pos
        visited.add(pos)

    count = len(visited) - 1  # the last position outside the map is also included
    print("Puzzle 1:", count)


if __name__ == "__main__":
    with open("inputs/day_06.txt", "r") as fp:
        obstructions = []
        guard_initial_pos = None
        guard_initial_direction = Direction.NORTH  # it's always north at the start

        rows = fp.read().splitlines()
        for y, row in enumerate(rows):
            if not row:
                continue

            for x, char in enumerate(list(row)):
                if char == "#":
                    obstructions.append(Point(x, y))
                elif char == "^":
                    guard_initial_pos = Point(x, y)

        assert guard_initial_pos is not None

    guard_map_info = GuardMapInfo(
        width=len(rows[0]),
        height=len(rows),
        obstructions=obstructions,
        guard_initial_position=guard_initial_pos,
        guard_initial_direction=Direction.NORTH,
    )

    puzzle_1(guard_map_info)
