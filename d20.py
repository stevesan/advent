

input = '''1
2
-3
3
-2
0
4'''


with open('d20real.txt', 'r') as f: input = f.read()

entries = [(pos, int(line)) for pos, line in enumerate(input.split('\n'))]
N = len(entries)
print(entries)

for orig_pos in range(N):
  # find it
  curr_pos = None
  for i in range(N):
    if entries[i][0] == orig_pos:
      curr_pos = i
      break

  entry = entries[curr_pos]
  move = entry[1]
  print(f'-- {move} moves..')
  new_pos = (curr_pos + move) % (N-1)
  # Take the entry out
  entries = entries[0:curr_pos] + entries[curr_pos+1:]
  # print('removed: ' + str([e[1] for e in entries]))
  # print(new_pos)
  # Insert into new pos
  entries.insert(new_pos, entry)

  # print([e[1] for e in entries])

curr_pos = None
for i in range(N):
  if entries[i][1] == 0:
    total = 0
    for j in [1000, 2000, 3000]:
      print(entries[(i+j)%N])
      total += entries[(i+j)%N][1]
    print(total)
    break