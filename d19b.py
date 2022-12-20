from enum import Enum
from dataclasses import dataclass
import time
from math import ceil
import sys
import heapq

LOGPRE = []

MAX_MINUTES = 32

VERBOSE = False

class Res(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3
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
  inv:list[int]
  bots:list[int]
  minutes:int
  trace:str

  def clone(self):
    return State(inv=list(self.inv), \
      bots=list(self.bots), \
      minutes=self.minutes, \
      trace=self.trace)

  def can_afford(self, costs:list[int]):
    assert len(costs) == 3
    assert len(self.inv) == 4
    return costs[0] <= self.inv[0] and costs[1] <= self.inv[1] and costs[2] <= self.inv[2]

  def time_to_afford_bot(self, costs:list[int]):
    max_time = 0
    for i in range(3):
      if costs[i] == 0: continue
      if self.bots[i] == 0 and costs[i] > 0:
        # Can never afford just idling
        return None
      time = ceil((costs[i] - self.inv[i]) / self.bots[i])
      max_time = max(max_time, time)
    return max_time

  def build_bot(self, bot_to_build:Res, bot_res2need:list[int]):
    assert bot_to_build is not None

    # Time advances
    self.minutes += 1

    # Spend resources to start building
    for i in range(3):
      self.inv[i] -= bot_res2need[i]
      assert self.inv[i] >= 0

    # Current bots collect
    for i in range(len(self.bots)):
      self.inv[i] += self.bots[i]

    # Done building bot
    # Do NOT do this before the above collection step - the newly built bot doesn't get to collect this minute!
    self.bots[bot_to_build.value] += 1

    self.trace += str(bot_to_build)[4:5]

  def idle_for(self, minutes:int):
    self.minutes += minutes
    for i in range(len(self.bots)):
      self.inv[i] += self.bots[i] * minutes
    self.trace += str(minutes)

  def __lt__(self, nxt):
    return False

def best_num_geodes(bp:Blueprint):
  t0 = time.time()
  last_log_time = time.time()

  init_state = State(inv=[0, 0, 0, 0], bots=[1, 0, 0, 0], minutes=0, trace='O')
  Q:list[State] = []

  def push(state:State):
    # Order by number of geode bots...the number of geodes..
    heapq.heappush(Q, (-state.bots[GEODE], -state.inv[GEODE], state))

  def pop():
    return heapq.heappop(Q)[-1]

  push(init_state)
  aprunes = 0
  best_score = 0
  iters = 0
  while Q:
    t1 = time.time()
    if t1 - last_log_time > 2:
      last_log_time = t1
      elapsed = t1 - t0
      print(f'{LOGPRE} {elapsed:.2f}s, iter {iters:,}, |Q|={len(Q)}, best={best_score}, Ap={aprunes:,}')

    iters += 1
    state:State = pop()

    if VERBOSE: print(f'Visiting {state}')

    # Assess the idle-value of this state. Ie. just idling here, how much geode would we get?
    idle_score = state.inv[GEODE] + (MAX_MINUTES-state.minutes) * state.bots[GEODE]
    if idle_score > best_score:
      best_score = idle_score
      print(f'{LOGPRE} improved to {best_score} via {state}')

    if (MAX_MINUTES - state.minutes) < 2:
      # Need at least 2 minutes to build a new bot and mine. So, anything less, the idle score is the best we can do
      continue

    # A Prune: let's generously assume you can build 1 geode bot every turn for the remaining minutes..even then, would you do better than the best? if not, we can prune
    # This helps a lot. Even with tiny2!!
    remain = MAX_MINUTES - state.minutes
    generous_addl_geodes = remain * (remain+1) / 2
    existing_bot_geodes = remain * state.bots[GEODE]
    if state.inv[GEODE] + generous_addl_geodes + existing_bot_geodes <= best_score:
      if VERBOSE: print(f'A-pruned {state}')
      aprunes += 1
      continue

    # fast forward to..which bot should we build next?
    # Favor building geode bots first..to improve potential pruning
    for bottype in [Res.GEODE, Res.OBSIDIAN, Res.CLAY, Res.ORE]:
      costs = bp.bot2costs[bottype.value]
      time_to_afford = state.time_to_afford_bot(costs)
      if time_to_afford is None or state.minutes + time_to_afford + 1 >= MAX_MINUTES:
        continue
      # idle for time to afford, then build it
      new_state = state.clone()
      if time_to_afford > 0:
        new_state.idle_for(time_to_afford)
      new_state.build_bot(bottype, costs)
      push(new_state)

    # If we could immediately build all bots, there's no point in idling.

  dt = time.time() - t0
  print(f'{LOGPRE} Done in {iters:,} iters, {dt:.2f}s, best = {best_score}')
  return best_score

def main(filep, first=None, last=None):
  blueprints: list[Blueprint] = []
  LOGPRE.append(filep)
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
          count, resstr = res_cost.strip().split(' ')
          count = int(count)
          res = Res[resstr.upper()]
          assert res != Res.GEODE
          costs[res.value] = count
        bot2costs[botres.value] = costs

      bp = Blueprint(id, bot2costs)
      blueprints.append(bp)

  total_qual = 0
  todo = blueprints
  if first is not None:
    todo = blueprints[first-1:last-1+1]
  for bp in todo:
    LOGPRE.append(bp.id)
    print(f'doing {bp.id}')
    best = best_num_geodes(bp)
    qual = best * bp.id
    total_qual += qual
    print(f'{LOGPRE} blueprint {bp.id} can get {best} geodes')
    LOGPRE.pop(-1)

  LOGPRE.pop(-1)
  return total_qual

if len(sys.argv) > 1:
  if sys.argv[1] == 'split':
    f = 'd19full.txt'
    first = int(sys.argv[2])
    last = int(sys.argv[3])
    main(f, first, last)
  else:
    VERBOSE = True
    MAX_MINUTES = int(sys.argv[1])
    assert main(sys.argv[2]) == int(sys.argv[3])
else:
  assert main('d19tiny.txt') == 465
  assert main('d19tiny2.txt') == 465
  assert main('d19b-lastminute.txt') == 0
  assert main('d19b-lastminute1.txt') == 1
  assert main('d19sample-bp1only.txt') == 56
  assert main('d19sample-bp2only.txt') == 62
  # main('d19full.txt')