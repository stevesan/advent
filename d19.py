from enum import Enum
from dataclasses import dataclass

class Res(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3

@dataclass
class Blueprint:
  id: int
  bot2costs: list[list[int]]

  def get_cost(self, bot:Res, resource:Res):
    assert resource != Res.GEODE
    return self.bot2costs[bot.value][resource.value]

@dataclass
class State:
  res2count:list[int]
  bot2count:list[int]
  minutes:int
  def clone(self):
    return State(res2count=list(self.res2count), \
      bot2count=list(self.bot2count), \
      minutes=self.minutes)

  def can_afford(self, res2need:list[int]):
    assert len(res2need) == 3
    assert len(self.res2count) == 4
    for i in range(len(res2need)):
      if res2need[i] > self.res2count[i]:
        return False
    return True

  def tick(self, bot_to_build:Res, bot_res2need:list[int]):
    # We can only build bots we can afford at start of frame
    if bot_to_build is not None:
      assert self.can_afford(bot_res2need)

    # Time advances
    self.minutes += 1

    # Current bots collect
    for i in range(len(self.bot2count)):
      self.res2count[i] += self.bot2count[i]

    if bot_to_build is not None:
      # Spend resources to build
      for i in range(3):
        self.res2count[i] -= bot_res2need[i]
      # Build it
      self.bot2count[bot_to_build.value] += 1


def best_num_geodes(bp:Blueprint):
  MAX_MINUTES = 24
  init_state = State(res2count=[0, 0, 0, 0], bot2count=[1, 0, 0, 0], minutes=0)
  stack:list[State] = [init_state]
  best_score = 0
  iters = 0
  while stack:
    print(iters)
    iters += 1
    state = stack.pop(0)

    if state.minutes == MAX_MINUTES:
      if state.res2count[Res.GEODE] > best_score:
        best_score = state.res2count[Res.GEODE]
      continue

    # We can always just idle
    idle_state = state.clone()
    idle_state.tick(None, None)
    stack.append(idle_state)

    # We can also build bots we can afford..
    for bottype in Res:
      if state.can_afford(bp.bot2costs[bottype.value]):
        print(f'building {bottype}')
        new_state = state.clone()
        new_state.tick(bottype, bp.bot2costs[bottype.value])
        stack.append(new_state)

  return best_score

def main(filep):
  blueprints: list[Blueprint] = []
  with open(filep, 'r') as f:
    for line in f:
      header, costs = line.split(':')
      bp, idstr = header.split(' ')
      assert bp == 'Blueprint'
      id = int(idstr)
      botcost_strs = costs.split('.')

      bot2costs: list[list[int]] = [None] * 4
      for s in botcost_strs:
        if s.strip() == '': continue
        bottypestr, res_costs = s.split('costs')
        _, eachstr, bottype, robotstr, _ = bottypestr.split(' ')
        assert eachstr == 'Each'
        botres = Res[bottype.upper()]
        costs = [0] * 3
        for res_cost in res_costs.split(' and '):
          print(res_cost)
          count, resstr = res_cost.strip().split(' ')
          count = int(count)
          res = Res[resstr.upper()]
          assert res != Res.GEODE
          costs[res.value] = count
        bot2costs[botres.value] = costs

      bp = Blueprint(id, bot2costs)
      blueprints.append(bp)

  total_qual = 0
  for bp in blueprints:
    best = best_num_geodes(bp)
    qual = best * bp.id
    total_qual += qual

  return total_qual

assert main('d19tiny.txt') == 276
assert main('d19sample.txt') == 33