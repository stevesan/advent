
import sys
from dataclasses import dataclass
import time
from datetime import datetime

@dataclass
class Node:
  name: str
  nbor_names: list[str]
  rate: int
  nbors: list[object] = None

  def __hash__(self): return hash(self.name)

"""
order of opening doesn't matter
you can open at most 15 valves

one possible soln: find the 15 best valves - determine if possible to open all in time (can assume 15 minutes remaining)
hmm nah, it's not necessarily true that you need to open 15 valves for max release..maybe opening the best 10 is the best you can do under time
"""

TOTAL_TIME = 30

@dataclass
class SearchState:
  opened: set[Node]
  path: list[Node]
  actions: list[str]
  pressure_released:int = 0
  cached_time:int = None

  def cache_time(self):
    self.cached_time = self.get_time()

  def curr_node(self):
    return self.path[-1]

  def get_time(self):
    return len(self.path) - 1 + len(self.opened)

  def get_total_rate(self):
    return sum([node.rate for node in self.opened])

  def get_path_names(self):
    return [node.name for node in self.path]

  def clone(self):
    return SearchState(opened=set(self.opened), path=list(self.path), actions=list(self.actions), pressure_released=self.pressure_released)

  def release_pressure(self, minutes=1):
    self.pressure_released += self.get_total_rate() * minutes

  def __str__(self):
    return ';'.join(self.actions) + ' opened=[' + ",".join(self.opened_names()) + "] t=" + str(self.get_time()) + " p=" + str(self.pressure_released) + \
      f' r={self.get_total_rate()}'

  def opened_names(self):
    return [node.name for node in self.opened]

def state_is_worse_or_equal(a:SearchState, b:SearchState):
  """ Only returns true if a is definitely NOT better than b """

  # Can't really say which is worse if they're at different nodes
  # This is actually quite slow, surprisingly.
  # assert a.curr_node() == b.curr_node()

  return a.opened.issubset(b.opened) and a.cached_time >= b.cached_time and a.pressure_released <= b.pressure_released

@dataclass
class NodeStates:
  states: list[SearchState]

  def add(self, state:SearchState):
    self.states.insert(0, state)

def find_max_release(name2node:dict[str, Node], timing_csvf):
  init_node = name2node['AA']
  init_state = SearchState(opened=set(), path=[init_node], actions=[])
  init_state.cache_time()
  assert init_state.get_time() == 0
  states_to_explore:list[SearchState] = [init_state]

  nonzero_valve_names = [node.name for node in name2node.values() if node.rate > 0]
  max_possible_rate = sum([node.rate for node in name2node.values()])

  best_score = None
  iters = 0
  t0 = time.time()
  best_state = init_state
  while states_to_explore:
    iters += 1
    state:SearchState = states_to_explore.pop(0)

    if iters % 10000 == 0:
      elapsed = time.time() - t0
      print(f'dt={elapsed} iter={iters} stack#={len(states_to_explore)}, state={state}')

      if timing_csvf:
        timing_csvf.write(f'{elapsed},{iters}')

    # is this state even possibly better than the best, even if we assume the next step can turn on all other valves?
    score_if_idling_at_best = best_state.pressure_released + (TOTAL_TIME - best_state.cached_time) * best_state.get_total_rate()
    # Assume in 1 more step..we unlock full rate. What then?
    best_possible_score_for_current = state.pressure_released + 1*state.get_total_rate() + (TOTAL_TIME - state.cached_time - 1) * max_possible_rate
    if best_possible_score_for_current <= score_if_idling_at_best:
      # There is no way this is going to be better than best - stop exploring this way
      print(f'pruning:\n  {state} best_pos={best_possible_score_for_current}\n  compared to:\n  {best_state} if_idle={score_if_idling_at_best}') 
      continue

    best_state = state

    if state.cached_time >= TOTAL_TIME:
      # Can't explore further.
      if best_score is None or state.pressure_released > best_score:
        best_score = state.pressure_released
        print(f'  improved to {best_score}\n  end state: {state}')
      continue

    # PRUNE: If no more non-zero valves left to open, then just release pressure for remaining time
    if len(state.opened) == len(nonzero_valve_names):
      remain_minutes = TOTAL_TIME - state.cached_time
      extrapolated_pressure = state.pressure_released + state.get_total_rate() * remain_minutes
      if best_score is None or extrapolated_pressure > best_score:
        best_score = extrapolated_pressure
        print(f'  ffwd improved to {best_score} \n  end state: {state}')
      continue

    # Keep exploring from this state

    # Open this valve?
    if state.curr_node().rate > 0 and not state.curr_node() in state.opened:
      opened_state = state.clone()
      # Important to release before we open the current valve. We do not get to count the current node as open for this minute.
      opened_state.release_pressure()
      opened_state.opened.add(state.curr_node())
      opened_state.actions.append(f'open {state.curr_node().name}')
      opened_state.cache_time()
      states_to_explore.append(opened_state)

    # We could move to any nbor
    for nbor in state.curr_node().nbors:
      moved_state = state.clone()
      moved_state.release_pressure()
      moved_state.path.append(nbor)
      moved_state.actions.append(f'goto {nbor.name}')
      moved_state.cache_time()
      states_to_explore.append(moved_state)

  print(f'done in {iters}. best = {best_score} best plan = \n  {best_state}')
  return best_score

def main(inputf):
  print(f'---- doing {inputf}')
  name2node:dict[str, Node] = {}
  with open(inputf) as f:
    for line in f:
      line = line.strip()
      """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"""
      # print(line)
      parts = line.split(' ')
      assert parts[0] == 'Valve'
      name = parts[1]

      ratestr = parts[4]
      assert ratestr[-1] == ';'
      rate = int(ratestr[len('rate='):-1])
      
      assert parts[8] in ['valves', 'valve']
      tunnelstrs = parts[9:]
      nbor_names = [s.replace(',', '') for s in tunnelstrs]

      node = Node(name=name, nbor_names=nbor_names, rate=rate)
      # print(node)
      name2node[name] = node

  # hook up nbors
  for node in name2node.values():
    nbors = [name2node[name] for name in node.nbor_names]
    node.nbors = nbors

  with open(f'd16timings/{inputf}-timings-{datetime.now().isoformat()}.csv', 'w') as f:
    return find_max_release(name2node, f)

assert main('d16tiny.txt') == 29
assert main('d16-leftright.txt') == 28 + 25
assert main('d16-example-where-opening-BB-first-is-worse.txt') == 565
assert main('d16test.txt') == 1651
assert main('d16-chain.txt') == 520
assert main('d16real.txt') == 1707
if len(sys.argv) > 1:
  main(sys.argv[1])