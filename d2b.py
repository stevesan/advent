letter2index = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y':1, 'Z': 2}

total = 0

with open('d2input.txt') as f:
  for line in f:
    line = line.strip()
    left, right = line.split(' ')
    li = letter2index[left]

    if right == 'X':
      # lose
      ri = (li - 1) % 3
      total += ri + 1 + 0
    elif right == 'Y':
      # draw
      ri = li
      total += ri + 1 + 3
    else:
      # win
      ri = (li + 1) % 3
      total += ri + 1 + 6

print(total)