
import sys, os
from dataclasses import dataclass
from math import floor

@dataclass
class Monkey:
  items:list[int]
  op:str
  oparg:int
  testdivisor:int
  true_throw_to:int
  false_throw_to:int

  inspect_times:int = 0

  def test(self, val):
    return val % self.testdivisor == 0

  def apply_op(self, old):
    argval = old if self.oparg is None else self.oparg
    if self.op == '*':
      return old * argval
    elif self.op == '+':
      return old + argval
    raise Exception(f'unknown op: {self.op}')

def parse_monkeys(inputf):
  with open(inputf, 'r') as f:
    lines = f.readlines()

  monkeys = []
  i = 0
  while 7*i < len(lines):
    chunk = lines[7*i : 7*i + 7]
    assert chunk[0].startswith('Monkey ')
    itemsline = chunk[1]
    opline = chunk[2]
    testline = chunk[3]
    trueline = chunk[4]
    falseline = chunk[5]

    items = [int(s.strip()) for s in itemsline.split(':')[1].split(',')]

    op, argstr = opline.split(' old ')[1].split(' ')
    assert op in ['+', '*']
    if argstr == 'old\n':
      argval = None
    else: 
      argval = int(argstr)

    assert 'Test: divisible by ' in testline
    testdivisor = int(testline.split(' by ')[1])

    assert 'If true: throw to monkey ' in trueline
    true_throw_to = int(trueline.split(' ')[-1])

    assert 'If false: throw to monkey ' in falseline
    false_throw_to = int(falseline.split(' ')[-1])

    mon = Monkey(items=items, op=op, oparg=argval, testdivisor=testdivisor,
      true_throw_to=true_throw_to,
      false_throw_to=false_throw_to)

    monkeys.append(mon)
    print(mon)

    i += 1

  return monkeys

def main(inputf, numrounds):
  print('------')
  monkeys:list[Monkey] = parse_monkeys(inputf)

  for i in range(numrounds):
    for mon in monkeys:
      while mon.items:
        item = mon.items.pop(0)
        item = mon.apply_op(item)
        mon.inspect_times += 1
        item = int(floor(item / 3))
        if mon.test(item):
          monkeys[mon.true_throw_to].items.append(item)
        else:
          monkeys[mon.false_throw_to].items.append(item)
  
  print(f'After {numrounds} rounds:\n{monkeys}')

  # Find top two 2 inspecting monkeys
  monkeys.sort(key=lambda m: -m.inspect_times)
  return monkeys[0].inspect_times * monkeys[1].inspect_times

assert main('d11sample.txt', 20) == 10605
assert main('d11full.txt', 1)

# main(sys.argv[1])