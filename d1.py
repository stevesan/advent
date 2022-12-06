groups = []
group = []
with open('d1input.txt') as f:
  for line in f:
    line = line.strip()
    if line == '':
      groups.append(group)
      group = []
    else:
      group.append(int(line))
groups.append(group)

print(len(groups))

print('Day 1 answer: ' + str(max([sum(g) for g in groups])))

totals = [sum(g) for g in groups]
totals.sort()

print('Day 2 answer: ' + str(sum(totals[-3:])))