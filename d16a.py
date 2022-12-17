
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
  pressure_released:int = 0

  def curr_node(self):
    return self.path[-1]

  def get_time(self):
    return len(self.path) - 1 + len(self.opened)

  def get_total_rate(self):
    return sum([node.rate for node in self.opened])

  def clone(self):
    return SearchState(opened=list(self.opened), path=list(self.path), pressure_released=self.pressure_released)

  def release_pressure_for_one_minute(self):
    self.pressure_released += self.get_total_rate()

def find_max_release(name2node:dict[str, Node]):
  init_node = name2node['AA']
  init_state = SearchState(opened=[], path=[init_node])
  assert init_state.get_time() == 0
  states_to_explore:list[SearchState] = [init_state]

  best_score = None
  while states_to_explore:
    state:SearchState = states_to_explore.pop(-1)
    if state.get_time() >= 30:
      # Can't explore further.
      if best_score is None or state.pressure_released > best_score:
        best_score = state.pressure_released
        print(f'improved to {best_score}')
      continue

    # Keep exploring from this state
    if not state.curr_node() in state.opened:
      # We could open this valve
      opened_state = state.clone()
      # Important to release before we open the current valve. We do not get to count the current node as open for this minute.
      opened_state.release_pressure_for_one_minute()
      opened_state.opened.append(state.curr_node())
      states_to_explore.append(opened_state)

    # We could move to any nbor
    # Note we need to allow moving to previously visited nodes. For the dead-end case.
    for nbor in state.curr_node().nbors:
      moved_state = state.clone()
      moved_state.release_pressure_for_one_minute()
      moved_state.path.append(nbor)
      states_to_explore.append(moved_state)

  print(best_score)


def main():
  name2node:dict[str, Node] = {}
  with open(sys.argv[1]) as f:
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

  find_max_release(name2node)

main()