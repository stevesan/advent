
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

def is_correct(left:list, right:list):
  return True

with open ('d13a-test.txt') as f:
  sum_of_correct_indices = 0
  for i, (left, right) in enumerate(enum_pairs(f)):
    left = parse_line(left)
    right = parse_line(right)
    print(i, left, right)
    if is_correct(left, right):
      index = i + 1
      sum_of_correct_indices += index
  print(sum_of_correct_indices)
