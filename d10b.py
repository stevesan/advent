input = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''

# input = '''noop
# addx 3
# addx -5'''

with open('d10a.txt', 'r') as f: input = f.read()

x = 1
cycle2x = [x]
for line in input.split('\n'):
  parts = line.split(' ')
  if parts[0] == 'noop':
    cycle2x.append(x)
  else:
    assert parts[0] == 'addx'
    cycle2x.append(x)
    cycle2x.append(x)
    x += int(parts[1])

print(len(cycle2x))
# "render"
# if x at cycle c (cycle2x[c]) is within 1 of c, draw # as position c
for row in range(6):
  rowstr = ''
  for hori in range(40):
    cycle = row * 40 + 1 + hori
    x = cycle2x[cycle]
    if abs(x - hori) < 2:
      rowstr += '#'
    else:
      rowstr += '.'
  print(rowstr)
