REPORT = list[int]

reports: list[REPORT] = []
with open("inputs/day_02.txt", "r") as fp:
    for row in fp.read().splitlines():
        if not row:
            continue

        report = [int(j) for j in row.split()]
        reports.append(report)


def is_safe(report: REPORT) -> bool:
    level_diffs = [j - k for k, j in zip(report, report[1:])]
    all_levels_valid = all(1 <= abs(i) <= 3 for i in level_diffs)
    all_decreasing = all(i < 0 for i in level_diffs)
    all_increasing = all(i > 0 for i in level_diffs)

    return all_levels_valid and (all_decreasing or all_increasing)


safe_reports_1 = sum(is_safe(report) for report in reports)
print("Puzzle 1:", safe_reports_1)

safe_reports_2 = 0
for report in reports:
    if is_safe(report):
        safe_reports_2 += 1
    else:
        for k in range(len(report)):
            report_without_level_k = [j for i, j in enumerate(report) if i != k]
            if is_safe(report_without_level_k):
                safe_reports_2 += 1
                break

print("Puzzle 2:", safe_reports_2)
