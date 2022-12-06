letter2index = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y':1, 'Z': 2}

total = 0

with open('d2input.txt') as f:
  for line in f:
    line = line.strip()
    left, right = line.split(' ')
    li = letter2index[left]
    ri = letter2index[right]
    if (li + 1) % 3 == ri:
      print(f'{right} beats {left}')
      total += ri + 6 + 1
    elif (ri + 1) % 3 == li:
      print(f'{left} beats {right}')
      total += ri + 0 + 1
    else:
      assert ri == li
      print(f'{left} == {right}')
      total += ri + 1 + 3

print(total)