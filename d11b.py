
import sys, os
from dataclasses import dataclass
from math import floor, log10
import time


@dataclass
class Monkey:
  items:list[int]
  debugs:list[str]
  op:str
  oparg:int
  testdivisor:int
  true_throw_to:int
  false_throw_to:int

  inspect_times:int = 0

  def test(self, val):
    return val % self.testdivisor == 0

  def apply_op(self, old, dbg):
    argval = old if self.oparg is None else self.oparg
    if self.op == '*':
      if self.oparg is None:
        dbg = f'({dbg})**2'
      else:
        dbg = f'({dbg}) * {argval}'
      return old * argval, dbg
    elif self.op == '+':
      return old + argval, f'{dbg} + {argval}'
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

    mon = Monkey(items=items, debugs=[str(item) for item in items], \
      op=op, oparg=argval, testdivisor=testdivisor,
      true_throw_to=true_throw_to,
      false_throw_to=false_throw_to)

    monkeys.append(mon)
    # print(mon)

    i += 1

  return monkeys

def main(inputf, numrounds):
  print('------')
  monkeys:list[Monkey] = parse_monkeys(inputf)

  t0 = time.time()

  modnum = 1
  for mon in monkeys:
    modnum *= mon.testdivisor

  for i in range(numrounds):
    # print(f'--------- {i}')
    t1 = time.time()
    if t1-t0 > 1:
      print(f'doing round {i}')
      print(log10(monkeys[0].items[0]))
      t0 = t1

    # statestr = '|'.join('*' * len(mon.items) for mon in monkeys)
    # print(statestr)

    # print('--' * len(monkeys[0].items))

    # print(log10(monkeys[0].items[0]))

    for monid, mon in enumerate(monkeys):
      # print(f'   -------monkey {monid}')
      while mon.items:
        item = mon.items.pop(0)
        dbg = mon.debugs.pop(0)
        old = item
        item, dbg = mon.apply_op(item, dbg)

        item = item % modnum

        # print(f'    {old} to {item}')
        mon.inspect_times += 1
        if mon.test(item):
          nextmon = monkeys[mon.true_throw_to]
        else:
          nextmon = monkeys[mon.false_throw_to]
        nextmon.items.append(item)
        nextmon.debugs.append(dbg)
  
  if True:
    print(f'After {numrounds}')
    for mon in monkeys:
      print('===========')
      for dbg in mon.debugs:
        print(dbg)

  # Find top two 2 inspecting monkeys
  monkeys.sort(key=lambda m: -m.inspect_times)
  rv = monkeys[0].inspect_times * monkeys[1].inspect_times
  print(rv)
  return rv

# main('d11sample.txt', 10000)

main('d11full.txt', 10000)
# assert main('d11sample.txt', 10000) == 2713310158
# assert main('d11full.txt', 10000)

# import cProfile
# cProfile.run("main('d11full.txt', 160)")

# main(sys.argv[1])