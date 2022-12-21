from dataclasses import dataclass

input = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''

with open('d21real.txt', 'r') as f: input = f.read()

@dataclass
class Monkey:
  op: str
  val: int
  arg1: str
  arg2: str

  def eval(self, name2monkey:dict[str, object]):
    if self.op == 'val':
      return self.val
    elif self.op == '+':
      return name2monkey[self.arg1].eval(name2monkey) + name2monkey[self.arg2].eval(name2monkey)
    elif self.op == '-':
      return name2monkey[self.arg1].eval(name2monkey) - name2monkey[self.arg2].eval(name2monkey)
    elif self.op == '*':
      return name2monkey[self.arg1].eval(name2monkey) * name2monkey[self.arg2].eval(name2monkey)
    elif self.op == '/':
      return name2monkey[self.arg1].eval(name2monkey) / name2monkey[self.arg2].eval(name2monkey)
    else:
      assert False, f'bad op: {self.op}'

name2monkey = {}
for line in input.split('\n'):
  name, code = line.split(': ')
  codeparts = code.split(' ')
  mon = None
  if len(codeparts) == 1:
    mon = Monkey(op='val', val=int(codeparts[0]), arg1=None, arg2=None)
  else:
    assert len(codeparts) == 3
    mon = Monkey(op=codeparts[1], val=None, arg1=codeparts[0], arg2=codeparts[2])
  name2monkey[name] = mon

print(name2monkey['root'].eval(name2monkey))