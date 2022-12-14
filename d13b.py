
import functools

def enum_pairs(f):
  while True:
    try:
      yield [next(f).strip(), next(f).strip()]
      assert next(f).strip() == ''
    except StopIteration: return

def parse_line(line:str):
  stack = [[]]
  number_str = ''

  def maybe_finish_number():
    nonlocal number_str
    if number_str:
      stack[-1].append(int(number_str))
      number_str = ''

  for letter in line:
    if letter == '[':
      stack.append([])
    elif letter == ']':
      maybe_finish_number()
      done_list = stack.pop(-1)
      stack[-1].append(done_list)
    elif letter == ',':
      maybe_finish_number()
    else:
      assert type(int(letter)) == int
      number_str += letter
  return stack[0][0]

def do_compare(lefts:list, rights:list):
  """ return 1 if right, -1 if wrong, 0 if inconclusive"""
  # print(left, right)
  i = 0
  while True:
    if i >= len(lefts) and i < len(rights): return 1
    if i >= len(rights) and i < len(lefts): return -1
    if i >= len(lefts) and i >= len(rights): return 0
    left = lefts[i]
    right = rights[i]
    if type(left) == int and type(right) == int:
      if left < right: return 1
      elif left > right: return -1
    elif type(left) == list and type(right) == list:
      result = do_compare(left, right)
      if result != 0: return result
    else:
      if type(left) == int: left = [left]
      if type(right) == int: right = [right]
      result = do_compare(left, right)
      if result != 0: return result
    i += 1
      
  return 0

with open ('d13a-input.txt') as f:
  sum_of_correct_indices = 0
  packets = []
  for i, (left, right) in enumerate(enum_pairs(f)):
    left = parse_line(left)
    right = parse_line(right)
    packets.append(left)
    packets.append(right)

  # Add divibers
  div1 = [[2]]
  div2 = [[6]]
  packets.append(div1)
  packets.append(div2)

  packets.sort(key=functools.cmp_to_key(do_compare), reverse=True)
  print('\n'.join([str(p) for p in packets]))

  decoderkey = 1
  for i in range(len(packets)):
    if packets[i] == div1:
      decoderkey *= i+1
    elif packets[i] == div2:
      decoderkey *= i+1

  print(decoderkey)