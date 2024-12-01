from collections import Counter

left = []
right = []
with open("inputs/day_01.txt", "r") as fp:
    for row in fp.read().splitlines():
        if not row:
            continue

        a, b = row.split(" " * 3)
        left.append(int(a))
        right.append(int(b))

left.sort()
right.sort()

diffs = [abs(a - b) for a, b in zip(left, right)]

print("Puzzle 1:", sum(diffs))

right_counter = Counter(right)
score = sum([i * right_counter.get(i, 0) for i in left])

print("Puzzle 2:", score)
