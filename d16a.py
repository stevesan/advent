
import sys
from dataclasses import dataclass

@dataclass
class Node:
  name: str
  nbor_names: list[str]
  rate: int
  nbors: list[object] = None

"""
order of opening doesn't matter
you can open at most 15 valves

one possible soln: find the 15 best valves - determine if possible to open all in time (can assume 15 minutes remaining)
hmm nah, it's not necessarily true that you need to open 15 valves for max release..maybe opening the best 10 is the best you can do under time
"""

@dataclass
class SearchState:
  opened: list[Node]
  path: list[Node]
  actions: list[str]
  pressure_released:int = 0

  def curr_node(self):
    return self.path[-1]

  def get_time(self):
    return len(self.path) - 1 + len(self.opened)

  def get_total_rate(self):
    return sum([node.rate for node in self.opened])

  def get_path_names(self):
    return [node.name for node in self.path]

  def clone(self):
    return SearchState(opened=list(self.opened), path=list(self.path), actions=list(self.actions), pressure_released=self.pressure_released)

  def release_pressure(self, minutes=1):
    self.pressure_released += self.get_total_rate() * minutes

def find_max_release(name2node:dict[str, Node]):
  print(' -----------')
  init_node = name2node['AA']
  init_state = SearchState(opened=[], path=[init_node], actions=[])
  assert init_state.get_time() == 0
  states_to_explore:list[SearchState] = [init_state]

  nonzero_valve_names = [node.name for node in name2node.values() if node.rate > 0]

  indep_state_to_best_time = {}
  indep_state_to_best_pressure = {}

  best_score = None
  iters = 0
  while states_to_explore:
    iters += 1
    state:SearchState = states_to_explore.pop(0)
    opened_valve_names = [node.name for node in state.opened]
    opened_valve_names.sort()
    indep_key = (state.curr_node().name, tuple(opened_valve_names))

    print(f'doing {indep_key}, time = {state.get_time()}, pres = {state.pressure_released}')

    # PRUNE: If we have been at this node before with the same opened valves, and we did it in less time before AND more pressure right now, we do not need to explore further!
    # Be very conservative about pruning..
    prev_time = indep_state_to_best_time.get(indep_key, None)
    prev_pressure = indep_state_to_best_pressure.get(indep_key, None)
    if prev_time is None:
      assert prev_pressure is None
      print(f'  adding {indep_key}, time = {state.get_time()}, pres = {state.pressure_released}')
      indep_state_to_best_time[indep_key] = state.get_time()
      indep_state_to_best_pressure[indep_key] = state.pressure_released
    else:
      print(f'  comparing to t={prev_time} p={prev_time} ')
      if (state.get_time() >= prev_time and state.pressure_released <= prev_pressure):
        # The current state is worse or equiv. Do not bother checking its score or exploring further
        print(f'pruned, strictly worse than prior. t={state.get_time()} p={state.pressure_released}.\n  actions = {state.actions}')
        continue
      elif (state.get_time() < prev_time and state.pressure_released > prev_pressure):
        # Current state is strictly better. Make this the new watermark.
        print(f'  adding {indep_key}, time = {state.get_time()}, pres = {state.pressure_released}')
        indep_state_to_best_time[indep_key] = state.get_time()
        indep_state_to_best_pressure[indep_key] = state.pressure_released

    if state.get_time() >= 30:
      # Can't explore further.
      if best_score is None or state.pressure_released > best_score:
        best_score = state.pressure_released
        print(f'  improved to {best_score}. end state: {indep_key}')
      continue

    # PRUNE: If no more non-zero valves left to open, then just release pressure for remaining time
    if len(state.opened) == len(nonzero_valve_names):
      remain_minutes = 30 - state.get_time()
      state.release_pressure(remain_minutes)
      if best_score is None or state.pressure_released > best_score:
        best_score = state.pressure_released
        print(f'  ffwd improved to {best_score}. end state: {indep_key}. idled for {remain_minutes} minutes\n  actions: {state.actions}')
      continue

    # Keep exploring from this state

    # Open this valve?
    if state.curr_node().rate > 0 and not state.curr_node() in state.opened:
      opened_state = state.clone()
      # Important to release before we open the current valve. We do not get to count the current node as open for this minute.
      opened_state.release_pressure()
      opened_state.opened.append(state.curr_node())
      opened_state.actions.append(f'open {state.curr_node().name}')
      states_to_explore.append(opened_state)

    # We could move to any nbor
    for nbor in state.curr_node().nbors:
      moved_state = state.clone()
      moved_state.release_pressure()
      moved_state.path.append(nbor)
      moved_state.actions.append(f'goto {nbor.name}')
      states_to_explore.append(moved_state)

  print(f'done in {iters}. best = {best_score}')
  return best_score

def main(inputf):
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

  return find_max_release(name2node)

assert main('d16tiny.txt') == 29
if len(sys.argv) > 1:
  main(sys.argv[1])