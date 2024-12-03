import re

with open("inputs/day_03.txt", "r") as fp:
    memory = fp.read().strip()

mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

res_puzzle_1 = 0
for match in re.findall(mul_pattern, memory):
    a, b = int(match[0]), int(match[1])
    res_puzzle_1 += a * b
print("Puzzle 1:", res_puzzle_1)


# Parsed as ('mul(402,190)', '402', '190', 'don't', 'do')
part_2_pattern = re.compile(f"({mul_pattern.pattern})" + r"|(don't\(\))|(do\(\))")

res_puzzle_2 = 0
is_do = True
for mul, mul_a, mul_b, dont, do in re.findall(part_2_pattern, memory):
    if mul and is_do:
        a, b = int(mul_a), int(mul_b)
        res_puzzle_2 += a * b
    elif do:
        is_do = True
    elif dont:
        is_do = False

print("Puzzle 2:", res_puzzle_2)
