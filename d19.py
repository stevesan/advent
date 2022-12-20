from enum import Enum
from dataclasses import dataclass
import time
from math import ceil
import sys
import heapq

LOGPRE = []

MAX_MINUTES = 24

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

  def tick(self, bot_to_build:Res, bot_res2need:list[int]):
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
      self.inv[i] += self.bots[i]

    self.trace += str(minutes)

  def __lt__(self, nxt):
    return sum(self.bots) < sum(nxt.bots) \
      or sum(self.inv) < sum(nxt.inv) \
      or self.minutes < nxt.minutes

def best_num_geodes(bp:Blueprint):
  t0 = time.time()

  init_state = State(inv=[0, 0, 0, 0], bots=[1, 0, 0, 0], minutes=0, trace='O')
  Q:list[State] = []

  def push(state:State):
    # Order by number of geode bots...the number of geodes..
    heapq.heappush(Q, (MAX_MINUTES - state.bots[GEODE], MAX_MINUTES - state.inv[GEODE], state))

  def pop():
    return heapq.heappop(Q)[-1]

  push(init_state)

  best_score = 0
  iters = 0
  while Q:
    t1 = time.time()
    if t1 - t0 > 2:
      t0 = t1
      print(f'{LOGPRE} iter {iters}, |Q|={len(Q)}')

    iters += 1
    state:State = pop()

    # Assess the idle-value of this state. Ie. just idling here, how much geode would we get?
    idle_score = state.inv[GEODE] + (MAX_MINUTES-state.minutes) * state.bots[GEODE]
    if idle_score > best_score:
      best_score = idle_score
      print(f'{LOGPRE} improved to {best_score} via {state}')

    if state.minutes == MAX_MINUTES:
      continue

    # Prune: let's generously assume you can build 1 geode bot every turn for the remaining minutes..even then, would you do better than the best? if not, we can prune
    remain = MAX_MINUTES - state.minutes
    generous_addl_geodes = remain * (remain+1) / 2
    existing_bot_geodes = remain * state.bots[GEODE]
    if state.inv[GEODE] + generous_addl_geodes + existing_bot_geodes <= best_score:
      if VERBOSE: print(f'Pruned {state}')
      continue

    if VERBOSE: print(f'Expanding {state}')

    idle_actions = []
    # Favor building geode bots first..to improve potential pruning
    for bottype in [Res.GEODE, Res.OBSIDIAN, Res.CLAY, Res.ORE]:
      costs = bp.bot2costs[bottype.value]
      time_to_afford = state.time_to_afford_bot(costs)
      if time_to_afford is None:
        continue
      if time_to_afford <= 0:
        # Build it now
        assert state.can_afford(costs)
        new_state = state.clone()
        new_state.tick(bottype, costs)
        push(new_state)
      else:
        # idle to the time it takes
        idle_actions.append((bottype, time_to_afford))

    if idle_actions:
      # idle to the soonest bot
      min_time = min([t[1] for t in idle_actions])
      if min_time + state.minutes >= MAX_MINUTES:
        # Even waiting for the soonest bot exceeds max minutes - done here.
        continue
      # ONLY idle if we cannot afford some bot. Otherwise, there is never any point to idling and we should've built.
      idle_state = state.clone()
      idle_state.idle_for(min_time)
      push(idle_state)

    # If we could immediately build all bots, there's no point in idling.

  print(f'{LOGPRE} Done in {iters} iters')
  return best_score

def main(filep):
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
  for bp in blueprints:
    best = best_num_geodes(bp)
    qual = best * bp.id
    total_qual += qual
    print(f'{LOGPRE} blueprint {bp.id} can get {best} geodes')

  LOGPRE.pop(-1)
  return total_qual

if len(sys.argv) > 1:
  VERBOSE = True
  MAX_MINUTES = int(sys.argv[1])
  assert main(sys.argv[2]) == int(sys.argv[3])
else:
  assert main('d19tiny.txt') == 253
  assert main('d19tiny2.txt') == 253
  assert main('d19sample.txt') == 33