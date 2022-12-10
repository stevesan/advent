import sys

init_stack = '''\
[V]         [T]         [J]        
[Q]         [M] [P]     [Q]     [J]
[W] [B]     [N] [Q]     [C]     [T]
[M] [C]     [F] [N]     [G] [W] [G]
[B] [W] [J] [H] [L]     [R] [B] [C]
[N] [R] [R] [W] [W] [W] [D] [N] [F]
[Z] [Z] [Q] [S] [F] [P] [B] [Q] [L]
[C] [H] [F] [Z] [G] [L] [V] [Z] [H]'''
lines = init_stack.split('\n')
lines.reverse()
stacks = [[] for _ in range(9)]
for line in lines:
  for i in range(9):
    letter = line[i*4 + 1]
    if letter == ' ': continue
    stacks[i].append(letter)
stacks

with open(sys.argv[1], 'r') as f:
  for line in f:
    parts = line.split(' ')
    assert parts[0] == 'move'
    count = int(parts[1])
    source = int(parts[3]) - 1
    dest = int(parts[5]) - 1
    for _ in range(count):
      letter = stacks[source].pop()
      stacks[dest].append(letter)

  tops = ''
  for s in stacks:
    print(s)
    tops += s[-1]
  print(tops)